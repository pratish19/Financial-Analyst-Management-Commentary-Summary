import streamlit as st
import json
import os
import tempfile
import time
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="Analyst AI: Earnings Analyzer (OCR Version)", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get a Free Key Here](https://aistudio.google.com/app/apikey)")
    st.divider()
   

# --- HELPER: UPLOAD TO GEMINI ---
def upload_to_gemini(uploaded_file, key):
    """
    Saves the Streamlit file to a temp path, uploads it to Gemini, 
    and returns the file handle.
    """
    try:
        genai.configure(api_key=key)
        
        # 1. Save uploaded file to a temporary file on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # 2. Upload to Google GenAI
        gemini_file = genai.upload_file(tmp_path, mime_type="application/pdf")
        
        # 3. Wait for processing (usually instant for small PDFs)
        while gemini_file.state.name == "PROCESSING":
            time.sleep(1)
            gemini_file = genai.get_file(gemini_file.name)

        return gemini_file

    except Exception as e:
        st.error(f"❌ Upload Error: {e}")
        return None

# --- ANALYST ENGINE ---
def analyze_pdf_directly(gemini_file):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = """
    You are a senior financial analyst. Analyze the attached PDF document.
    
    CRITICAL INSTRUCTION: Return valid JSON only. No Markdown.
    
    EXTRACT THESE FIELDS:
    1. Meta: Company Name, Quarter/Period.
    2. Sentiment: Tone (Optimistic/Cautious/etc), Confidence Score, and Rationale.
    3. Key Takeaways: List of 3-5 Positives and 3-5 Concerns.
    4. Guidance: Revenue, Margin, and Capex outlooks.
    5. Operational: Capacity Utilization and New Growth Initiatives.
    """
    
    try:
        # Pass the FILE object + PROMPT text
        response = model.generate_content([gemini_file, prompt])
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
    except Exception as e:
        st.error(f"❌ Analysis Error: {e}")
        return None

# --- MOCK DATA ---
def get_mock_data():
    return {
        "meta": {"company": "Test Corp (Scanned PDF Mode)", "quarter": "Q1 2026"},
        "sentiment_analysis": {"tone": "Neutral", "confidence": "Medium", "rationale": "Mock data loaded successfully."},
        "key_takeaways": {"positives": ["OCR Bypassed", "File Upload Worked"], "concerns": ["None"]},
        "forward_guidance": {"revenue_outlook": "N/A", "margin_outlook": "N/A", "capex_outlook": "N/A"}
    }

# --- MAIN UI ---
st.title("📊 Financial Analyst : Management Commentary Summary")
st.info("ℹ️ Using Gemini Vision to read scanned documents.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Upload Document")
    uploaded_file = st.file_uploader("Scanned PDF", type=["pdf"])
    
    if uploaded_file:
        if st.button("Run Analysis", type="primary"):
            
            
            if not api_key:
                st.error("⚠️ Please enter an API Key.")
            
            else:
                with st.spinner("Uploading to Gemini & Reading Scanned Text..."):
                    # 1. Upload File
                    g_file = upload_to_gemini(uploaded_file, api_key)
                    
                    if g_file:
                        # 2. Analyze File
                        data = analyze_pdf_directly(g_file)
                        if data:
                            st.session_state['result'] = data
                            st.success("Analysis Complete!")

with col2:
    st.subheader("Summary Dashboard")
    
    if 'result' in st.session_state:
        data = st.session_state['result']

        # --- TILE 1: META DATA ---
        with st.container(border=True):
            meta = data.get("Meta", {})
            st.markdown(f"### 🏢 {meta.get('Company Name', 'N/A')}")
            st.caption(f"**Period:** {meta.get('Quarter/Period', 'N/A')}")

        # --- TILE 2: SENTIMENT ANALYSIS ---
        with st.container(border=True):
            st.markdown("### 🧠 Sentiment Analysis")
            sent = data.get("Sentiment", {})
            
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Tone", sent.get("Tone", "N/A"))
                st.metric("Confidence", sent.get("Confidence Score", "N/A"))
            with c2:
                st.info(f"**Rationale:** {sent.get('Rationale', 'N/A')}")

        # --- TILE 3: KEY TAKEAWAYS ---
        with st.container(border=True):
            st.markdown("### 🔑 Key Takeaways")
            tk = data.get("Key Takeaways", {})
            
            col_pos, col_neg = st.columns(2)
            
            with col_pos:
                st.success("##### ✅ Positives")
                for item in tk.get('Positives', []):
                    st.markdown(f"- {item}")
            
            with col_neg:
                st.error("##### ⚠️ Concerns")
                for item in tk.get('Concerns', []):
                    st.markdown(f"- {item}")

        # --- TILE 4: GUIDANCE & OUTLOOK ---
        with st.container(border=True):
            st.markdown("### 🔮 Guidance & Outlook")
            guide = data.get("Guidance", {})
            
            # Using markdown for a cleaner list look inside the tile
            st.markdown(f"**💰 Revenue:** {guide.get('Revenue', 'N/A')}")
            st.markdown(f"**📉 Margin:** {guide.get('Margin', 'N/A')}")
            st.markdown(f"**🏗️ Capex:** {guide.get('Capex', 'N/A')}")

        # --- TILE 5: OPERATIONAL ---
        with st.container(border=True):
            st.markdown("### ⚙️ Operational Updates")
            ops = data.get("Operational", {})
            
            st.markdown(f"**🏭 Capacity Utilization:** {ops.get('Capacity Utilization', 'N/A')}")
            st.divider()
            st.markdown(f"**🚀 New Growth Initiatives:** {ops.get('New Growth Initiatives', 'N/A')}")

    else:
        st.info("AI Insights.")