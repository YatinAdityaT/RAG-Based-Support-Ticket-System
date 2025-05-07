import faiss
import numpy as np
from typing import List, Dict, Optional, Any
from config import OS_SYNONYMS, exact_match_boost

class RAGSearchIndex:
    def __init__(
        self,
        tickets: List[Dict[str, Any]],
        embed_func,
        prepare_text_func,
        normalize_filters: bool = True,
    ):
        self.tickets = tickets
        self.embed = embed_func
        self.prepare_text = prepare_text_func
        self.normalize_filters = normalize_filters

        # Precompute embeddings and index
        self.texts = self.prepare_text(self.tickets)
        self.embeddings = self.embed(self.texts).astype("float32")
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def _apply_metadata_filter(self, candidates: List[int], filters: Dict[str, str]) -> List[int]:
        if not filters:
            return candidates
        out = []
        for idx in candidates:
            ticket = self.tickets[idx]
            ok = True
            for key, val in filters.items():
                if val.lower() == "all" and self.normalize_filters:
                    continue
                tv = str(ticket.get(key, "")).lower()
                if key == "browser":
                    if val.lower() not in tv:
                        ok = False
                elif key == "os":
                    filter_os = val.lower()
                    ticket_os_group = next(
                        (k for k, syns in OS_SYNONYMS.items() if any(tv.startswith(s) for s in syns)),
                        ""
                    )
                    if not ticket_os_group.startswith(filter_os):
                        ok = False
                else:
                    if tv != val.lower():
                        ok = False
                if not ok:
                    break
            if ok:
                out.append(idx)
        return out

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, str]] = None,
        top_k: int = 5,
        boost_terms: Optional[Dict[str, List[str]]] = exact_match_boost,
        base_threshold: float = 0.15,
        rerank_weights: Dict[str, float] = {"sim": 0.6, "overlap": 0.4},
    ) -> List[Dict[str, Any]]:
        # Embed query with boosting
        q_vec = self.embed([query])[0]
        if boost_terms:
            boosts = [
                self.embed([term])[0]
                for group in boost_terms.values()
                for term in group
                if term in query.lower()
            ]
            if len(boosts) >= 2:
                boost_mean = np.mean(boosts, axis=0)
                q_vec = 0.7 * q_vec + 0.3 * boost_mean

        # Semantic search
        fetch_k = min(len(self.texts), top_k * 5)
        sims, idxs = self.index.search(np.array([q_vec], dtype="float32"), fetch_k)
        sims, idxs = sims[0], idxs[0].tolist()

        # Fallback to semantic rerank if no filters or low confidence
        if not filters or (sims.size > 0 and sims[0] < base_threshold):
            sem_cand = [(i, s) for i, s in zip(idxs, sims) if s >= base_threshold]
            if not sem_cand:
                sem_cand = list(zip(idxs, sims))[:top_k]
            q_tokens = set(query.lower().split())
            reranked = []
            for i, s in sem_cand:
                tokens = set(self.texts[i].lower().split())
                overlap = len(q_tokens & tokens) / max(len(q_tokens), 1)
                score = rerank_weights["sim"] * s + rerank_weights["overlap"] * overlap
                reranked.append((i, score))
            reranked.sort(key=lambda x: x[1], reverse=True)
            final_idxs = [i for i, _ in reranked[:top_k]]
        else:
            # Apply metadata filters
            filt_idxs = self._apply_metadata_filter(idxs, filters)
            if not filt_idxs:
                final_idxs = idxs[:top_k]
            else:
                cand = [(i, s) for i, s in zip(filt_idxs, sims[: len(filt_idxs)]) if s >= base_threshold]
                if not cand:
                    final_idxs = idxs[:top_k]
                else:
                    q_tokens = set(query.lower().split())
                    reranked = []
                    for i, s in cand:
                        tokens = set(self.texts[i].lower().split())
                        overlap = len(q_tokens & tokens) / max(len(q_tokens), 1)
                        score = rerank_weights["sim"] * s + rerank_weights["overlap"] * overlap
                        reranked.append((i, score))
                    reranked.sort(key=lambda x: x[1], reverse=True)
                    final_idxs = [i for i, _ in reranked[:top_k]]

        # Deduplicate by issue
        seen, results = set(), []
        for idx in final_idxs:
            ticket = self.tickets[idx]
            issue = ticket.get("issue")
            if issue in seen:
                continue
            seen.add(issue)
            results.append(ticket)

        return results