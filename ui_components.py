import streamlit as st
import pandas as pd
from typing import List, Tuple

def load_styles():
    """Apply glassmorphism + modern dark theme"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            padding: 2rem;
        }
        
        .trust-title {
            font-family: 'Inter', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        }
        
        .trust-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.3rem;
            color: #a0a0cc;
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 2.5rem;
            box-shadow: 0 25px 45px rgba(0,0,0,0.3);
            margin-bottom: 2rem;
        }
        
        .metric-container {
            background: rgba(102, 126, 234, 0.2);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(102, 126, 234, 0.3);
            text-align: center;
        }
        
        .stMetric > label {
            color: #a0a0cc !important;
            font-size: 1.1rem !important;
        }
        
        .stMetric > div > div {
            color: #ffffff !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
        }
        
        .analyze-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 15px;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 600;
            color: white;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .analyze-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }
        
        .sidebar .sidebar-content {
            background: rgba(20, 20, 40, 0.95) !important;
            backdrop-filter: blur(20px);
        }
        
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: white !important;
        }
        
        .stDataFrame {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def sidebar_info():
    """Professional sidebar"""
    with st.sidebar:
        st.markdown("""
        # 🔍 TrustGuard
        **AI-generated content verifier**
        
        **✨ Features:**
        • Automatic claim extraction
        • Wikipedia cross-verification  
        • Smart trust scoring
        • Color-coded reliability
        
        **🎯 AMD Slingshot Prototype**
        Team: SHADOWS | Leader: PRAKATHEESH S
        """)

def main_header():
    """Animated gradient title"""
    st.markdown('<h1 class="trust-title">🔍 TrustGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="trust-subtitle">Verify AI content reliability instantly</p>', unsafe_allow_html=True)

def input_section():
    """Enhanced input with settings"""
    col1, col2 = st.columns([3, 1])
    with col1:
        user_text = st.text_area(
            "📝 Paste AI-generated content", 
            height=200,
            placeholder="Paste ChatGPT, Gemini, or any AI response here...",
            help="System auto-splits into claims & verifies each against Wikipedia"
        )
    with col2:
        st.markdown("### ⚙️ Settings")
        max_sentences = st.slider("Wikipedia sentences", 1, 4, 2)
    return user_text, max_sentences

def analyze_button():
    """Animated analyze button"""
    return st.button("🚀 Analyze Trust Score", key="analyze", help="Verify all claims")

def display_results(df: pd.DataFrame):
    """Fancy results with metrics + table"""
    overall_trust = df["Trust Score"].str.rstrip('%').astype(float).mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Overall Trust Score", f"{overall_trust:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card" style="opacity: 0.8;">', unsafe_allow_html=True)
        st.info("💡 Word overlap similarity scoring")
        st.markdown('</div>', unsafe_allow_html=True)
    
    

    st.markdown("## 📊 Claim Analysis")
    st.dataframe(
        df, 
        column_config={
            "Status": st.column_config.Column("Status", width="medium"),
            "Trust Score": st.column_config.Column("Trust Score", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )
    
    
    st.markdown("### 📈 Summary")
    col1, col2, col3 = st.columns(3)
    green_count = len(df[df["Status"].str.contains("🟢")])
    yellow_count = len(df[df["Status"].str.contains("🟡")])
    red_count = len(df[df["Status"].str.contains("🔴")])
    
    with col1: st.metric("✅ Verified", green_count)
    with col2: st.metric("🟡 Review", yellow_count)
    with col3: st.metric("🔴 Questionable", red_count)
