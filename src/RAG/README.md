# RAG Directory

This directory contains the Retrieval-Augmented Generation (RAG) notebook for personalized recommendations and itinerary planning using AI and vector search.

## Contents

- **RAG.ipynb**
  - Main notebook implementing RAG for Egyptian monuments and tourist sites.
  - Loads and processes data from museums, monuments, archaeological sites, and sunken monuments.
  - Uses LangChain, ChromaDB, HuggingFace, DeepSeek, and Google Generative AI for embeddings and retrieval.
  - Extracts user intent, retrieves relevant attractions, and filters results for itinerary planning.

## How to Use

1. Open `RAG.ipynb` in Jupyter or VS Code.
2. Install required packages (see first cell in notebook):
   - `langchain`, `langchain_community`, `tiktoken`, `langchain-openai`, `langchainhub`, `chromadb`, `langchain-deepseek`, `langchain-tavily`, `python-dotenv`, `langchain_google_genai`
3. Set up API keys as needed (see notebook cells for details).
4. Run the notebook cells to:
   - Load and embed data
   - Extract user preferences
   - Retrieve and filter attractions
   - Prepare input for itinerary planning agents

## Notes

- The notebook demonstrates advanced RAG techniques for travel recommendations.
- Data files should be available and paths updated as needed.
- API keys are required for some models and services.

---
