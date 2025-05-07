import streamlit as st
from data_loader import load_dataset, load_tickets, prepare_corpus
from embedding_utils import embed_texts, build_faiss_index
from filter_extractor import extract_filters
from search_index import RAGSearchIndex
from dump.llm_integration_old import generate_response
from feedback import save_feedback

# Initialize the system
data = load_dataset()
tickets = load_tickets(data)
searcher = RAGSearchIndex(tickets, embed_texts, prepare_corpus)

# Streamlit interface
st.title("Support Ticket RAG System")
st.write("Enter a query to retrieve relevant tickets and generate a response.")

query = st.text_input("Query", "Example: 'Chrome login issues on Windows 10'")
top_k = st.slider("Number of tickets to retrieve", 1, 10, 5)

if st.button("Search"):
    if query:
        # Retrieve tickets
        filters = extract_filters(query)
        results = searcher.search(query, filters, top_k=top_k)
        
        # Generate response
        response = generate_response(query, results)
        
        # Display results
        st.subheader("Generated Response")
        st.write(response)
        
        st.subheader("Relevant Tickets")
        for ticket in results:
            st.write(f"**ID:** {ticket['id']}")
            st.write(f"**Title:** {ticket['title']}")
            st.write(f"**Issue:** {ticket['issue']}")
            st.write(f"**Resolution:** {ticket['resolution']}")
            st.write(f"**Browser:** {ticket['browser']}, **OS:** {ticket['os']}, **Customer:** {ticket['customer_type']}")
            st.write("---")
            
            # Feedback mechanism
            feedback = st.radio(
                f"Was this ticket (ID: {ticket['id']}) relevant?",
                ("Yes", "No"),
                key=ticket['id']
            )
            if st.button(f"Submit Feedback for Ticket {ticket['id']}", key=f"btn_{ticket['id']}"):
                ticket_text = f"Title: {ticket['title']}, Issue: {ticket['issue']}"
                save_feedback(query, ticket_text, feedback)
                st.success(f"Feedback submitted for Ticket {ticket['id']}")
    else:
        st.warning("Please enter a query.")

st.write("Feedback is saved to 'feedback.csv' for relevance analysis.")