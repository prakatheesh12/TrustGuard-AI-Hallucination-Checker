# TrustGuard – AI Hallucination Checker

## Overview
TrustGuard is an AI-powered system designed to detect hallucinations in AI-generated content.  
It verifies factual claims using a hybrid approach combining rule-based validation, semantic similarity, and knowledge retrieval.

---

## Problem Statement
AI models sometimes generate incorrect or fabricated information (hallucinations).  
Users currently lack an easy way to quickly verify the reliability of AI-generated text.

---

## Solution
TrustGuard analyzes AI-generated content and:
- Splits text into individual claims
- Verifies each claim using trusted knowledge sources
- Calculates a Trust Score (0–100)
- Displays supporting evidence for verification

---

## Features
- Claim-level verification
- Trust score calculation
- Evidence from knowledge sources
- Hybrid verification approach:
  - Rule-based fact checking
  - Semantic similarity using embeddings
  - Wikipedia-based retrieval

---

## Tech Stack
- Python
- Streamlit
- Sentence Transformers
- NLTK
- Wikipedia API

---

## Installation

Clone the repository:
```bash
git clone https://github.com/prakatheesh12/TrustGuard-AI-Hallucination-Checker.git
cd TrustGuard-AI-Hallucination-Checker
