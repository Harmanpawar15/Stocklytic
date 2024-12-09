import streamlit as st
import os
import dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

dotenv.load_dotenv()

namespace = "stock-descriptions"

sectors = [
    "Consumer Defensive",
    "Communication Services",
    "Real Estate",
    "Healthcare",
    "Basic Materials",
    "Utilities",
    "Energy",
    "Industrials",
    "Consumer Cyclical",
    "Financial Services",
    "Technology",
]

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index("stocks")


def truncate_text(text, max_length=135):
    return text[:max_length] + '...' if len(text) > max_length else text


st.set_page_config(page_title="Stock Finder", page_icon="📈", layout="wide")

# Title and header
st.markdown("""
<style>
    .title-header {
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        font-weight: bold;
        font-size: 3em;
        margin-bottom: 0.2em;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
        color: #888;
    }
</style>
<div class="title-header">Stocklytic 📈</div>
<div class="sub-header">Discover the best stocks tailored to your needs</div>
""", unsafe_allow_html=True)

query = st.text_input(
    "What kind of stock are you looking for?",
    placeholder="Cryptocurrency, EV, Tech, etc.",
    label_visibility="collapsed",
)

if query:
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embedded_query = model.encode([query]).tolist()

col1, col2 = st.columns(2)

with col1:
    number_filter = st.number_input(
        "Number of results",
        1,
        25,
        10,
        help="Specify the number of stock results to display."
    )

    sector_filter = st.selectbox(
        "Sector",
        ["Any Sector"] + sectors,
        help="Select a specific sector or 'Any Sector' for all sectors."
    )
    if sector_filter == "Any Sector":
        sector_filter = None

with col2:
    market_cap_filter = st.slider(
        "Market Cap Filter (in billions USD)",
        0.0,
        3670.0,  # Max market cap for Apple in billions
        (0.0, 3670.0),
        format="$%.1fB",
        help="Filter stocks by market capitalization range."
    )
    
    volume_filter = st.slider(
        "Volume Filter (in millions)",
        0,
        648,  # Max volume for HMBL in millions
        (0, 648),
        format="%d M",
        help="Filter stocks by trading volume range."
    )

searching = st.button("Search", use_container_width=True)
if searching:
    result = None
    with st.spinner('Searching...'):
        if sector_filter:
            result = pinecone_index.query(
                namespace=namespace,
                vector=embedded_query,
                top_k=number_filter,
                filter={
                    "Market Cap": {"$gte": market_cap_filter[0] * 1e9, "$lte": market_cap_filter[1] * 1e9},
                    "Volume": {"$gte": volume_filter[0] * 1e6, "$lte": volume_filter[1] * 1e6},
                    "Sector": {"$eq": sector_filter},
                    "Ticker": {"$ne": "N/A"},
                },
                include_metadata=True,
            )
        else:
            result = pinecone_index.query(
                namespace=namespace,
                vector=embedded_query,
                top_k=number_filter,
                filter={
                    "Market Cap": {"$gte": market_cap_filter[0] * 1e9, "$lte": market_cap_filter[1] * 1e9},
                    "Volume": {"$gte": volume_filter[0] * 1e6, "$lte": volume_filter[1] * 1e6},
                    "Ticker": {"$ne": "N/A"},
                },
                include_metadata=True,
            )

    if len(result.matches) == 0:
        st.warning("No results found. Please try a different search.")
    else:
        st.markdown("""
        <style>
            .stock-container {
                display: flex;
                flex-wrap: wrap; /* Allow cards to wrap into a new line */
                justify-content: space-between; /* Space cards out evenly */
                margin-top: 20px;
            }
            .stock-card {
                background: #1e1e2f;
                border-radius: 10px;
                padding: 20px;
                width: calc(50% - 20px); /* Adjust for two cards per row with space */
                color: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                margin: 10px; /* Adds space between cards */
            }
            .stock-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            }
            .stock-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .stock-metrics {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 10px;
            }
            .metric {
                text-align: center;
            }
            .metric-label {
                font-size: 0.8em;
                color: #bbb;
            }
            .metric-value {
                font-size: 1.2em;
                font-weight: bold;
            }
            .positive {
                color: #4caf50;
            }
            .negative {
                color: #f44336;
            }
            .stock-link {
                text-decoration: none;
                color: #3ea6ff;
                font-weight: bold;
                display: block;
                margin-top: 10px;
                text-align: center;
            }
        </style>
        <div class="stock-container">
        """, unsafe_allow_html=True)

        for obj in result.matches:
            metadata = obj.metadata
            name = truncate_text(metadata.get('Name', 'N/A'), max_length=25)
            ticker = metadata.get('Ticker', 'N/A')
            description = truncate_text(metadata.get('text', 'No description available.'))
            sector = metadata.get('Sector', 'Sector Unknown')

            earnings_growth = metadata.get('Earnings_Growth', 0.0)
            earnings_growth = f"{earnings_growth*100:.2f}%"

            revenue_growth = metadata.get('Revenue_Growth', 0.0)
            revenue_growth = f"{revenue_growth*100:.2f}%"

            website = metadata.get('website', f"https://www.finviz.com/quote.ashx?t={ticker}")

            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-title">{name} ({ticker})</div>
                <div>{sector}</div>
                <div>{description}</div>
                <div class="stock-metrics">
                    <div class="metric">
                        <div class="metric-label">Earnings Growth</div>
                        <div class="metric-value {'positive' if float(earnings_growth.strip('%')) > 0 else 'negative'}">{earnings_growth}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Revenue Growth</div>
                        <div class="metric-value {'positive' if float(revenue_growth.strip('%')) > 0 else 'negative'}">{revenue_growth}</div>
                    </div>
                </div>
                <a href="{website}" class="stock-link" target="_blank">View More</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
