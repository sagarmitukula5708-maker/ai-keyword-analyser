import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="AI Overview Keyword Analyzer", layout="wide")

st.title("🔑 AI Overview Keyword Analyzer")

# User API Key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file with keywords", type=["csv"])

if uploaded_file is not None and api_key:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Keywords:", df.head())
    
   openai.api_key = "AIzaSyBktncfXblCucdOqXI_PEM9WK2CQsktxUo"

    
    # Function to analyze a single keyword
    def analyze_keyword(keyword):
        prompt = f"""
        Analyze the keyword: '{keyword}'.

        1. Classify its **Search Intent** (Informational, Navigational, Transactional, Commercial).
        2. Predict whether this keyword is **likely to trigger AI Overviews** in Google Search.
        3. Provide a short explanation.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an SEO assistant specializing in Google AI Overviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=180
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return str(e)
    
    # Run Analysis
    if st.button("Analyze Keywords"):
        results = []
        for kw in df.iloc[:, 0]:
            results.append(analyze_keyword(kw))
        
        df['AI Overview Analysis'] = results
        st.write(df)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "ai_overview_analysis.csv", "text/csv")
