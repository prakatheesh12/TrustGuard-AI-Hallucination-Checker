import re
from typing import List, Tuple
import pandas as pd
import streamlit as st
import wikipedia

# Import UI components
from ui_components import (
    load_styles, sidebar_info, main_header, 
    input_section, analyze_button, display_results
)

# Core logic functions
def clean_text(text: str) -> str:
    """Clean text for comparison"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_claims(text: str) -> List[str]:
    """Split text into claims"""
    raw_sentences = re.split(r"(?<=[\.\!\?])\s+", text.strip())
    claims = [s.strip() for s in raw_sentences if len(s.strip()) > 10]
    return claims

def get_wikipedia_snippet(claim: str, max_sentences: int = 2) -> Tuple[str, str]:
    """Get Wikipedia reference"""
    try:
        short_query = " ".join(claim.split()[:8])
        search_results = wikipedia.search(short_query)
        if not search_results:
            return "No result", "No relevant Wikipedia article found."
        page_title = search_results[0]
        summary = wikipedia.summary(page_title, sentences=max_sentences)
        return page_title, summary
    except Exception as e:
        return "Error", f"Wikipedia fetch failed: {e}"

def compute_similarity_and_label(claim: str, reference: str) -> Tuple[float, str]:
    """Calculate similarity score and label"""
    if not reference or "No relevant" in reference or "failed" in reference:
        return 0.0, "No Reference"
    
    claim_clean = clean_text(claim)
    ref_clean = clean_text(reference)
    
    claim_words = set(claim_clean.split())
    ref_words = set(ref_clean.split())
    
    if not claim_words:
        return 0.0, "No Reference"
    
    common = claim_words.intersection(ref_words)
    similarity = len(common) / len(claim_words)
    
    if similarity >= 0.6:
        label = "🟢 Likely True"
    elif similarity >= 0.3:
        label = "🟡 Unclear / Needs Review"
    else:
        label = "🔴 Likely False"
    
    return similarity, label

def main():
    """Main TrustGuard app"""
    st.set_page_config(
        page_title="TrustGuard - AI Trust Checker", 
        page_icon="🔍",
        layout="wide"
    )
    
    # Load beautiful UI
    load_styles()
    sidebar_info()
    main_header()
    
    # Get user input
    user_text, max_sentences = input_section()
    
    # Analyze button
    if analyze_button():
        if not user_text.strip():
            st.warning("👋 Please paste AI-generated text first!")
            st.stop()
        
        with st.spinner("🔍 Analyzing claims against Wikipedia..."):
            claims = extract_claims(user_text)
            
            if not claims:
                st.error("❌ No valid claims found. Use complete sentences.")
                st.stop()
            
            # Process each claim
            rows = []
            for idx, claim in enumerate(claims, start=1):
                title, snippet = get_wikipedia_snippet(claim, max_sentences)
                similarity, label = compute_similarity_and_label(claim, snippet)
                trust_score = round(similarity * 100, 1)
                
                rows.append({
                    "#": idx,
                    "Claim": claim,
                    "Wikipedia Source": title,
                    "Reference": snippet[:200] + "..." if len(snippet) > 200 else snippet,
                    "Similarity": f"{similarity:.1%}",
                    "Trust Score": f"{trust_score}%",
                    "Status": label,
                })
            
            df = pd.DataFrame(rows)
            display_results(df)

if __name__ == "__main__":
    main()
