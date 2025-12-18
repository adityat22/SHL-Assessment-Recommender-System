import streamlit as st
import sys
import os
import re
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.rag.engine import AssessmentRecommendationEngine

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff3333;
        color: white;
        border: none;
    }
    .stButton > button:active {
        background-color: #cc0000;
        color: white;
        border: none;
    }
    
    .assessment-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .assessment-title {
        font-size: 20px;
        font-weight: bold;
        color: #4da6ff;
        text-decoration: none;
    }
    .assessment-title:hover {
        text-decoration: underline;
    }
    .meta-info {
        font-size: 14px;
        color: #cccccc;
        margin-bottom: 5px;
    }
    .description {
        font-size: 14px;
        color: #e0e0e0;
        margin-top: 10px;
        line-height: 1.5;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        background-color: #333;
        color: #fff;
        font-size: 12px;
        margin-right: 5px;
    }
    h1 {
        font-size: 3rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 SHL Assessment Recommender 🔗")

st.markdown("""
This AI-powered tool helps you find the perfect SHL assessment for your hiring needs. Simply describe the role, skills, or job level you are looking for.
""")

@st.cache_resource
def get_engine():
    try:
        return AssessmentRecommendationEngine()
    except Exception as e:
        st.error(f"Failed to initialize the engine: {e}")
        return None

engine = get_engine()

@st.cache_data
def load_links_data():
    links_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'shl_links.json')
    if os.path.exists(links_path):
        try:
            with open(links_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {item.get('name', '').strip(): item for item in data}
        except:
            return {}
    return {}

links_data = load_links_data()

def parse_assessment_content(content, url_slug, title):
    duration_match = re.search(r"Approximate Completion Time in minutes = (?:max )?(\d+)", content)
    duration = f"{duration_match.group(1)} minutes" if duration_match else "N/A"
    
    type_match = re.search(r"Test Type: ([\w\s]+?)(?:Remote|Product)", content)
    test_type = type_match.group(1).strip() if type_match else "N/A"
    
    remote_match = re.search(r"Remote Testing: ([\w\s]+)", content)
    remote = remote_match.group(1).strip() if remote_match else "N/A"
    
    desc_start = content.find("Description")
    desc_end = content.find("Job levels")
    if desc_start != -1 and desc_end != -1:
        description = content[desc_start + 11:desc_end].strip()
    else:
        description = content[:300] + "..."

    url = f"https://www.shl.com/solutions/products/product-catalog/view/{url_slug}/"
    
    clean_title = title.replace(" | SHL", "").strip()
    link_info = links_data.get(clean_title)
    
    adaptive = "No"
    
    if link_info:
        if link_info.get('adaptive_irt'):
            adaptive = link_info.get('adaptive_irt')
        
        if link_info.get('url'):
            url = link_info.get('url')
            
        if link_info.get('test_type') and link_info.get('test_type') != "N/A":
            test_type = link_info.get('test_type')
            
        if link_info.get('remote_testing') and link_info.get('remote_testing') != "N/A":
            remote = link_info.get('remote_testing')
            
        if link_info.get('duration') and link_info.get('duration') != "N/A":
            duration = link_info.get('duration')
    
    return {
        "duration": duration,
        "test_type": test_type,
        "remote": remote,
        "description": description,
        "url": url,
        "adaptive": adaptive
    }

st.markdown("**Describe your requirements:**")
query = st.text_area("Describe your requirements:", label_visibility="collapsed", placeholder="Example: I need a python coding test for a senior backend developer with SQL skills...", height=100)

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please enter a job description.")
    elif not engine:
        st.error("Engine is not initialized.")
    else:
        st.markdown("### Recommended Assessments")
        
        with st.spinner("Searching..."):
            docs = engine.search(query, k=5)
            
            for i, doc in enumerate(docs, 1):
                title = doc.metadata.get('title', 'Unknown Assessment')
                meta = parse_assessment_content(doc.page_content, doc.metadata.get('url_slug', ''), title)
                
                with st.container():
                    st.markdown(f"""
                    <div class="assessment-card">
                        <a href="{meta['url']}" target="_blank" class="assessment-title">{i}. {title}</a>
                        <div class="meta-info" style="margin-top: 10px;">
                            <span class="badge">&#x23F1; {meta['duration']}</span>
                            <span class="badge">&#x1F4DD; {meta['test_type']}</span>
                            <span class="badge">&#x1F3E0; Remote: {meta['remote']}</span>
                        </div>
                        <div class="description">
                            {meta['description']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("Powered by SHL Product Catalog & Google Gemini")
