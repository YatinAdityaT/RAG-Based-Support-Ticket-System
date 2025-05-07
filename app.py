import streamlit as st
from data_loader import load_dataset, load_tickets, prepare_corpus
from embedding_utils import embed_texts, build_faiss_index
from filter_extractor import extract_filters
from search_index import RAGSearchIndex
from dump.llm_integration_old import generate_response
from feedback import save_feedback

# Load and cache data
@st.cache_data
def initialize():
    data = load_dataset()
    tickets = load_tickets(data)
    return tickets

tickets = initialize()
searcher = RAGSearchIndex(tickets, embed_texts, prepare_corpus)

# Streamlit interface
st.title("Support Ticket RAG System")
st.write("Enter a query to retrieve relevant tickets and generate a response.")

query = st.text_input("Query", "SSO redirect failure on Safari 16.3 macOS Ventura Enterprise")
top_k = st.slider("Number of tickets to retrieve", 1, 10, 5)

if st.button("Search") and query:
    # Retrieve tickets
    filters = extract_filters(query)
    results = searcher.search(query, filters, top_k=top_k)

    # Generate response
    response = generate_response(query, results)

    # Display generated response
    st.subheader("Generated Response")
    st.write(response)

    # Display relevant tickets
    st.subheader("Relevant Tickets")
    for ticket in results:
        st.write(f"**ID:** {ticket['id']}")
        st.write(f"**Title:** {ticket['title']}")
        st.write(f"**Issue:** {ticket['issue']}")
        st.write(f"**Resolution:** {ticket['resolution']}")
        st.write(f"**Browser:** {ticket['browser']}, **OS:** {ticket['os']}, **Customer:** {ticket['customer_type']}")
        st.write("---")

        feedback_key = f"feedback_{ticket['id']}"
        submit_key = f"submit_{ticket['id']}"

        # Track feedback using session state
        if feedback_key not in st.session_state:
            st.session_state[feedback_key] = "Yes"

        feedback = st.radio(
            f"Was this ticket (ID: {ticket['id']}) relevant?",
            ("Yes", "No"),
            key=feedback_key
        )

        if st.button(f"Submit Feedback for Ticket {ticket['id']}", key=submit_key):
            ticket_text = f"Title: {ticket['title']}, Issue: {ticket['issue']}"
            save_feedback(query, ticket_text, feedback)
            st.success(f"Feedback submitted for Ticket {ticket['id']}")

elif not query:
    st.warning("Please enter a query.")

st.write("Feedback is saved to 'feedback.csv' for relevance analysis.")


# import streamlit as st
# from data_loader import load_dataset, load_tickets, prepare_corpus
# from embedding_utils import embed_texts, build_faiss_index
# from filter_extractor import extract_filters
# from search_index import RAGSearchIndex
# from llm_integration import generate_response
# from feedback import save_feedback

# # Initialize session state for feedback
# if 'feedback_submitted' not in st.session_state:
#     st.session_state.feedback_submitted = {}

# # Initialize the system
# data = load_dataset()
# tickets = load_tickets(data)
# searcher = RAGSearchIndex(tickets, embed_texts, prepare_corpus)

# # Streamlit interface
# st.title("Support Ticket RAG System")
# st.write("Enter a query to retrieve relevant tickets and generate a response.")

# query = st.text_input("Query", "Example: 'Chrome login issues on Windows 10'")
# top_k = st.slider("Number of tickets to retrieve", 1, 10, 5)

# if st.button("Search"):
#     if query:
#         # Retrieve tickets
#         filters = extract_filters(query)
#         results = searcher.search(query, filters, top_k=top_k)
        
#         # Generate response
#         response = generate_response(query, results)
        
#         # Display results
#         st.subheader("Generated Response")
#         st.write(response)
        
#         st.subheader("Relevant Tickets")
#         for ticket in results:
#             st.write(f"**ID:** {ticket['id']}")
#             st.write(f"**Title:** {ticket['title']}")
#             st.write(f"**Issue:** {ticket['issue']}")
#             st.write(f"**Resolution:** {ticket['resolution']}")
#             st.write(f"**Browser:** {ticket['browser']}, **OS:** {ticket['os']}, **Customer:** {ticket['customer_type']}")
#             st.write("---")
            
#             # Feedback mechanism with yes/no buttons
#             st.write("Was this ticket helpful?")
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("Yes", key=f"yes_{ticket['id']}"):
#                     save_feedback(query, ticket['id'], "Yes")
#                     st.session_state.feedback_submitted[ticket['id']] = "Yes"
#             with col2:
#                 if st.button("No", key=f"no_{ticket['id']}"):
#                     save_feedback(query, ticket['id'], "No")
#                     st.session_state.feedback_submitted[ticket['id']] = "No"
            
#             # Display feedback submission status
#             if ticket['id'] in st.session_state.feedback_submitted:
#                 st.success(f"Feedback submitted for Ticket {ticket['id']}: {st.session_state.feedback_submitted[ticket['id']]}")
#     else:
#         st.warning("Please enter a query.")

# st.write("Feedback is saved to 'feedback.csv' for relevance analysis.")