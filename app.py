import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from utils import calculate_risk_score, risk_level
from charts import risk_gauge
from report import create_pdf

# Load .env
load_dotenv()

# API Key
api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Config
st.set_page_config(
    page_title="AI Risk Manager",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ AI Risk Manager")
st.write("Analyze business risks using Google Gemini AI")

# Check API Key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# Gemini Client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to create Gemini Client:\n{e}")
    st.stop()

# Inputs
company = st.text_input("Company Name")

industry = st.selectbox(
    "Industry",
    [
        "FinTech",
        "Healthcare",
        "E-Commerce",
        "EdTech",
        "Manufacturing",
        "Other"
    ]
)

description = st.text_area("Business Description")

# Analyze Button
if st.button("Analyze Risk"):

    if not company or not description:
        st.warning("Please fill all fields.")
        st.stop()

    prompt = f"""
You are a Senior AI Risk Management Consultant.

Analyze the following company.

Company Name:
{company}

Industry:
{industry}

Business Description:
{description}

Generate a professional report with the following sections:

# Executive Summary

# Top 5 Business Risks
Explain each risk briefly.

# Overall Risk Score (0-100)

# Risk Severity
(Low / Medium / High)

# Recommendations
Give at least 5 recommendations.

# Final Conclusion

Format everything using proper markdown headings and bullet points.
"""

    with st.spinner("Analyzing Risk..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            analysis = response.text

            st.success("✅ Analysis Completed")

            st.markdown("## 📊 AI Risk Analysis")

            st.markdown(analysis)

            # -----------------------------
            # Risk Score
            # -----------------------------
            score = calculate_risk_score(industry)
            level = risk_level(score)

            st.divider()

            st.subheader("📈 Overall Risk Score")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Risk Score", f"{score}/100")

            with col2:
                st.metric("Risk Level", level)

            st.plotly_chart(
                risk_gauge(score),
                use_container_width=True
            )

            # -----------------------------
            # PDF Report
            # -----------------------------
            pdf_path = create_pdf(
                company,
                industry,
                analysis
            )

            with open(pdf_path, "rb") as pdf_file:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name=f"{company}_Risk_Report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ Gemini Error:\n{e}")