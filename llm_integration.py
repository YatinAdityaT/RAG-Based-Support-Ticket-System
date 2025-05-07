from typing import List, Dict, Any
from huggingface_hub import InferenceClient
from config import LLM_MODEL, HF_API_TOKEN

client = InferenceClient(model=LLM_MODEL, token=HF_API_TOKEN)

def generate_response(query: str, tickets: List[Dict[str, Any]]) -> str:
    """Generate response with explicit resolution extraction"""
    if not tickets:
        return "No relevant solutions found. Please consult a senior support engineer."

    # Extract resolutions from tickets
    resolutions = [ticket['resolution'] for ticket in tickets]

    prompt = f"""<s>[INST] <<SYS>>
    You are a technical support expert. Use these resolutions:
    {chr(10).join(resolutions)}
    
    Format your response as:
    1. Problem summary
    2. Prioritized solutions with exact steps from resolutions
    3. Browser-specific instructions
    
    Do NOT mention ticket numbers. Use only the provided resolutions.
    <</SYS>>
    
    Query: {query}
    [/INST]"""
    
    try:
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=400,
            temperature=0.1,
            stop=["</s>"]
        )
        # Handle response safely
        if "[/INST]" in response:
            return response.split("[/INST]")[-1].strip()
        else:
            return response.strip()
    except Exception as e:
        return f"Response error: {str(e)}"