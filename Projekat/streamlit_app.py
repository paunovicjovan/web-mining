import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# --- Page Configuration ---
st.set_page_config(
    page_title="Phone Review Insights",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling (Premium Look) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
        padding: 0.5rem 2rem;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    header {
        visibility: visible;
    }

    .stApp {
        background: transparent;
    }

    h1 {
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: None;
        padding: 0.6rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
    }

    /* Result styling */
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border-left: 5px solid #38bdf8;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .cluster-title {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .sentiment-positive { color: #4ade80; }
    .sentiment-negative { color: #f87171; }
    .sentiment-neutral { color: #94a3b8; }
    
    </style>
""", unsafe_allow_html=True)

# --- API HELPER FUNCTIONS ---

@st.cache_data(ttl=600)  # Cache brands for 10 minutes
def get_brands():
    try:
        response = requests.get(f"{BACKEND_URL}/brands", timeout=5)
        if response.status_code == 200:
            return response.json().get("brands", [])
        return []
    except Exception as e:
        st.error(f"Error fetching brands: {e}")
        return []

@st.cache_data(ttl=300)  # Cache models for 5 minutes
def get_models(brand):
    if not brand:
        return []
    try:
        response = requests.get(f"{BACKEND_URL}/models?brand={brand}", timeout=5)
        if response.status_code == 200:
            return response.json().get("models", [])
        return []
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return []

def run_analysis(brand, model):
    try:
        payload = {"brand": brand, "model": model, "top_n": 50}
        response = requests.post(f"{BACKEND_URL}/analyze", json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning(f"No reviews found for {brand} {model}.")
        else:
            st.error(f"Analysis failed: {response.text}")
        return None
    except Exception as e:
        st.error(f"API Connection error: {e}")
        return None

# --- UI LAYOUT ---

st.markdown("<h1>Phone Review Insights</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analyze customer sentiment and extracted aspects for any mobile phone model.</p>", unsafe_allow_html=True)

# User Selection Container
with st.container():
    col1, col2 = st.columns(2)
    
    brands = get_brands()
    
    with col1:
        selected_brand = st.selectbox(
            "Select Brand",
            options=brands,
            index=None,
            placeholder="Search brand...",
            help="Type to search for a phone brand"
        )
    
    with col2:
        model_options = get_models(selected_brand) if selected_brand else []
        selected_model = st.selectbox(
            "Select Model",
            options=model_options,
            index=None,
            placeholder="Search model...",
            disabled=not selected_brand,
            help="Type to search for a specific model"
        )
    
    analyze_btn = st.button("Generate Insights")

# --- RESULTS AREA ---
if analyze_btn:
    if not selected_brand or not selected_model:
        st.warning("Please select both a brand and a model.")
    else:
        with st.spinner(f"Extracting and clustering insights for {selected_brand} {selected_model}... This may take a moment."):
            results = run_analysis(selected_brand, selected_model)
            
            if results:
                st.write("---")
                st.subheader(f"Analysis Results: {selected_brand} {selected_model}")
                st.info(f"Analyzed {results.get('review_count', 0)} reviews.")
                
                clusters = results.get("clusters", [])
                if not clusters:
                    st.write("No distinct aspects found in reviews.")
                else:
                    for cluster in clusters:
                        name = cluster.get("representative_name", "Unknown Aspect")
                        sentiment_summary = cluster.get("sentiment_summary", {})
                        
                        # Get breakdown
                        pos = sentiment_summary.get("positive", 0)
                        neu = sentiment_summary.get("neutral", 0)
                        neg = sentiment_summary.get("negative", 0)
                        
                        # Get dominant sentiment for styling the main tag
                        if sentiment_summary:
                            dominant_sentiment = max(sentiment_summary, key=sentiment_summary.get)
                        else:
                            dominant_sentiment = "neutral"
                        
                        count = cluster.get("total_mentions", 0)
                        terms = ", ".join(cluster.get("original_mentions", []))
                        
                        sentiment_class = f"sentiment-{dominant_sentiment.lower()}"
                        
                        st.markdown(f"""
                            <div class="result-card">
                                <div class="cluster-title">{name} <span class="{sentiment_class}">({dominant_sentiment.capitalize()})</span></div>
                                <div style="display: flex; gap: 15px; margin-bottom: 0.8rem; font-size: 0.9rem; font-weight: 600;">
                                    <span class="sentiment-positive">Positive: {pos}</span>
                                    <span class="sentiment-neutral">Neutral: {neu}</span>
                                    <span class="sentiment-negative">Negative: {neg}</span>
                                </div>
                                <div style="color: #94a3b8; font-size: 0.85rem;">
                                    <b>Total Mentions:</b> {count} | <b>Refers to:</b> {terms}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Results will appear here after analysis.")
