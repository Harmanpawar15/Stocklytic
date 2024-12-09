# 🧑‍💻 **StockLit: Automated Financial Analysis**

StockLit is an interactive stock financial analysis application that leverages advanced technologies like Pinecone-powered vector databases and OpenAI's language models to provide users with detailed stock insights. With features like custom filters, vector search, and augmented analysis, StockLit helps users easily explore financial data and make informed investment decisions.

---

## 🚀 **Features**

- **Interactive UI**: Built with Streamlit, providing a seamless user interface to query and filter stocks based on various criteria.
- **Vector Search**: Powered by Pinecone to search through a vector database for relevant stock information based on metadata and embeddings.
- **RAG-based Analysis**: Uses OpenAI LLMs to provide context-aware responses by combining query context and retrieved stock information.
- **Custom Filters**: Filter stocks by key metrics such as market cap, volume, and recommendation ratings.
- **Financial Visualizations**: Display key metrics like revenue growth, gross margins, market cap, and valuation in an intuitive format.

---

## 🛠️ **Tech Stack**

- **Python**: Core programming language for backend and data processing.
- **Hugging Face Transformers**: For generating high-dimensional vector embeddings using `sentence-transformers/all-mpnet-base-v2`.
- **Pinecone**: A vector database for managing and querying stock information.
- **Streamlit**: Frontend framework for building an interactive, user-friendly interface.
- **OpenAI LLMs**: For generating accurate and context-aware responses based on user queries.
- **YFinance**: For fetching real-time stock market data.

---

## ⚙️ **How it Works**

### 1. **Fetching Stock Data Using Yahoo Finance API**

Stock data is collected from Yahoo Finance through parallel processing and stored in Pinecone for efficient retrieval.

### 2. **User Query Input**

Users interact with the app via the Streamlit UI, where they describe the type of stocks they are looking for in natural language. Optional filters like Market Cap, Volume, and Recommendation Keys can be applied to refine the search.

### 3. **Generating Embeddings**

The user query is converted into a high-dimensional vector using HuggingFace's Sentence-Transformers, capturing the semantic meaning of the input for better matching.

### 4. **Vector Search with Pinecone**

The generated embedding is sent to Pinecone, where it searches through the vector database for relevant stock data. Filters are applied to narrow the search results, ensuring only the most relevant stocks are returned.

### 5. **Retrieval-Augmented Generation (RAG)**

The retrieved stock data is formatted into a context block, which is combined with the original user query and sent to OpenAI’s language model to generate a detailed, context-aware response.

### 6. **Displaying Results**

The top stock matches, along with their key financial metrics (e.g., Revenue Growth, Gross Margins, Market Cap, etc.), are displayed in an interactive format. Missing or malformed data is handled gracefully to ensure a smooth user experience.

---

## 📋 **Setup Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/StockLit
cd stocklit
