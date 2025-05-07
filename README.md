# Support Ticket RAG System

This project implements a Retrieval-Augmented Generation (RAG) system for support tickets. It retrieves relevant support tickets based on user queries and generates helpful responses using a Large Language Model (LLM). The system is built with modularity in mind, making it easy to maintain and extend.

- **Understand Semantic Context**: Uses the `sentence-transformers/all-MiniLM-L6-v2` text encoder to capture the semantic meaning of support queries and tickets.
- **Retrieve Relevant Tickets**: Employs FAISS for fast vector search and a retrieval strategy combining semantic search, metadata filtering, and reranking based on similarity and token overlap.
- **Generate Contextual Suggestions**: Leverages `mistralai/Mixtral-8x7B-Instruct-v0.1` LLM to produce coherent summaries or suggestions from retrieved tickets.
- **Code Implementation**: Written in Python using Streamlit for a simple query interface.
- **Model Choices**:
  - **Text Encoder**: `sentence-transformers/all-MiniLM-L6-v2` for efficient text-to-vector conversion.
  - **Vector Store**: FAISS for fast similarity search.
  - **LLM**: `mistralai/Mixtral-8x7B-Instruct-v0.1` for response generation.
- **Retrieval Strategy**: Top-k retrieval with semantic search and reranking.
- **Vector Search**: Implemented using FAISS.
- **Sample Tickets**: Embedded and searchable within the system.
- **Query Interface**: Streamlit-based web interface.
- **Output**: Displays relevant tickets and a generated answer.
- **Feedback Mechanism**: Users can rate ticket relevance, saved to a CSV file.
- **Pre-trained LLM**: Integrated for final response generation.

## Project Structure
- `config.py`: Configuration settings and synonym maps.
- `data_loader.py`: Loads and prepares the dataset.
- `embedding_utils.py`: Manages text embedding and FAISS index creation.
- `filter_extractor.py`: Extracts metadata filters from queries.
- `search_index.py`: Defines the `RAGSearchIndex` class for retrieval.
- `feedback.py`: Manages the feedback mechanism.
- `llm_integration.py`: Handles LLM response generation.
- `app.py`: Streamlit application integrating all components.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Hugging Face API token (set as `HF_API_TOKEN` environment variable)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd support-ticket-rag-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Login with & set your Hugging Face API token:
   ```bash
   huggingface-cli login
   export HF_API_TOKEN="your_huggingface_token"
   ```

### Running the Application
1. Start the Streamlit app:
   ```bash
   streamlit run app.py --server.fileWatcherType none
   ```

2. Open your browser to `http://localhost:8501` and enter a query to retrieve tickets and generate a response.

### Using Jupyter Notebook
You can also run the system components in a Jupyter notebook for experimentation:
1. Install Jupyter if not already installed:
   ```bash
   pip install jupyter
   ```

2. Launch Jupyter notebook:
   ```bash
   jupyter notebook
   ```

3. Create a new notebook and import necessary modules to test individual components.

## Dataset
The system uses a JSON dataset (`support_tickets_dataset.json`) containing support tickets with fields like `title`, `issue`, `resolution`, `browser`, `os`, and `customer_type`.

## Feedback
User feedback on ticket relevance is saved to `feedback.csv` for further analysis.

## License
This project is licensed under the MIT License.