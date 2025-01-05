# csv-rag
 
## Retrieval-Augmented Generation (RAG) Model

This project implements a **Retrieval-Augmented Generation (RAG)** model that leverages a CSV file as the data source for knowledge retrieval. The model enhances natural language generation by grounding its responses in real-world data.

### Key Features
- **CSV-Based Knowledge Retrieval**: The model extracts relevant information from a CSV file to provide accurate and data-driven responses.
- **Seamless Integration with LangChain**: Built using LangChain’s powerful toolkits to handle prompts, agents, and retrieval.
- **Streamlit-Powered Interface**: A user-friendly web interface for querying and interacting with the RAG model.

### How It Works
1. **Data Loading**: A CSV file is loaded as the knowledge base.
2. **Prompt Handling**: User queries are processed with context retrieved from the CSV file.
3. **Response Generation**: The model combines retrieved data with natural language generation techniques to provide an answer.
