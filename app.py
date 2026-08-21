import os
import json
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from google import genai
from openpyxl import Workbook

from database import (
    create_database,
    save_report,
    get_reports,
    delete_report,
)

from utils import (
    extract_business_description,
    extract_summary,
    extract_top_risks,
    calculate_risk_score,
    risk_level,
    extract_recommendations,
    extract_conclusion,
    clean_markdown,
)

from charts import (
    risk_gauge,
    risk_pie,
    risk_bar,
    risk_trend,
)

from report import create_pdf

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Risk Manager",
    page_icon="🛡️",
    layout="wide",
)

# =====================================================
# LOAD ENVIRONMENT
# =====================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=api_key)

# =====================================================
# DATABASE
# =====================================================

create_database()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🛡️ AI Risk Manager")

    st.markdown("---")

    reports = get_reports()

    total_reports = len(reports)

    if reports:
        avg_score = round(
            sum(r[2] for r in reports) / total_reports,
            1,
        )
        latest = reports[0][0]
    else:
        avg_score = 0
        latest = "-"

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Reports", total_reports)

    with c2:
        st.metric("Average", avg_score)

    with c3:
        st.metric("Latest", latest)

    st.markdown("---")

    st.success("🟢 Gemini Connected")

    st.caption("Version 4.0")

# =====================================================
# HEADER
# =====================================================

st.title("🛡️ AI Enterprise Risk Assessment")

st.write(
    "Analyze enterprise risks using Google Gemini AI and generate professional reports."
)

st.divider()

# =====================================================
# INPUTS
# =====================================================

left, right = st.columns(2)

with left:

    company = st.text_input("🏢 Company Name")

with right:

    industry = st.selectbox(
        "🏭 Industry",
        [
            "FinTech",
            "Healthcare",
            "Manufacturing",
            "E-Commerce",
            "Cyber Security",
            "EdTech",
            "Logistics",
            "Real Estate",
            "Retail",
            "Other",
        ],
    )

description = st.text_area(
    "📝 Business Description",
    height=180,
    placeholder="Describe your business, products, operations and challenges...",
)

st.divider()

# =====================================================
# ANALYZE BUTTON
# =====================================================

analyze = st.button(
    "🚀 Analyze Risk",
    use_container_width=True,
)
# =====================================================
# ANALYSIS
# =====================================================

if analyze:

    if company.strip() == "" or description.strip() == "":
        st.warning("⚠ Please enter Company Name and Business Description.")
        st.stop()

    prompt = f"""
You are a Senior Enterprise Risk Consultant
Analyze the following company and return the report EXACTLY in this format.

# Business Description

Rewrite the business description professionally.

# Executive Summary

Write a concise executive summary.

# Top 5 Risks

- Risk 1
- Risk 2
- Risk 3
- Risk 4
- Risk 5

# Risk Score

Mention only one score between 0 and 100.

# Severity

Low / Medium / High / Critical

# Recommendations

- Recommendation 1
- Recommendation 2
- Recommendation 3
- Recommendation 4
- Recommendation 5

# Final Conclusion

Company:
{company}

Industry:
{industry}

Business Description:
{description}
"""

    try:

        with st.spinner("🤖 Gemini AI is analyzing..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            analysis = response.text

        # ==========================================
        # Extract Information
        # ==========================================

        business_description = extract_business_description(analysis)

        summary = extract_summary(analysis)

        risks = extract_top_risks(analysis)

        recommendations = extract_recommendations(analysis)

        conclusion = extract_conclusion(analysis)

        score = calculate_risk_score(analysis)

        level = risk_level(score)

        # ==========================================
        # Save Report
        # ==========================================

        save_report(
            company,
            industry,
            score,
            level,
            analysis,
        )

        st.success("✅ Analysis Completed Successfully")

        st.divider()
        # =====================================================
        # KPI CARDS
        # =====================================================

        k1, k2, k3 = st.columns(3)

        with k1:
            st.metric(
                "📈 Risk Score",
                f"{score}/100",
            )

        with k2:
            st.metric(
                "⚠ Risk Level",
                level,
            )

        with k3:
            st.metric(
                "🏢 Company",
                company,
            )

        st.divider()

        # =====================================================
        # RISK GAUGE
        # =====================================================

        st.subheader("📊 Overall Risk Score")

        st.plotly_chart(
            risk_gauge(score),
            use_container_width=True,
        )

        st.divider()

        # =====================================================
        # CHARTS
        # =====================================================

        st.subheader("📈 Risk Insights")

        chart1, chart2 = st.columns(2)

        with chart1:

            st.plotly_chart(
                risk_pie(),
                use_container_width=True,
            )

        with chart2:

            st.plotly_chart(
                risk_bar(),
                use_container_width=True,
            )

        st.plotly_chart(
            risk_trend(),
            use_container_width=True,
        )

        st.divider()

        # =====================================================
        # BUSINESS DESCRIPTION
        # =====================================================

        st.subheader("🏢 Business Description")

        st.info(business_description)

        st.divider()

        # =====================================================
        # EXECUTIVE SUMMARY
        # =====================================================

        st.subheader("📋 Executive Summary")

        st.success(summary)

        st.divider()

        # =====================================================
        # TOP RISKS
        # =====================================================

        st.subheader("🚨 Top 5 Risks")

        if risks:

            for risk in risks:
                st.markdown(f"- {risk}")

        else:

            st.info("No risks detected.")

        st.divider()

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        st.subheader("✅ Recommendations")

        if recommendations:

            for rec in recommendations:
                st.markdown(f"- {rec}")

        else:

            st.info("No recommendations found.")

        st.divider()

        # =====================================================
        # FINAL CONCLUSION
        # =====================================================

        st.subheader("📍 Final Conclusion")

        st.success(conclusion)

        st.divider()
        # =====================================================
        # AI REPORT
        # =====================================================

        st.subheader("📋 Complete AI Report")

        tab1, tab2 = st.tabs(
            [
                "📄 Formatted Report",
                "💻 Raw Response",
            ]
        )

        with tab1:
            st.markdown(analysis)

        with tab2:
            st.code(
                analysis,
                language="markdown",
            )

        st.divider()

        # =====================================================
        # PDF EXPORT
        # =====================================================

        pdf_path = create_pdf(
            company,
            industry,
            analysis,
        )

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                use_container_width=True,
            )

        st.divider()

        # =====================================================
        # JSON EXPORT
        # =====================================================

        json_data = {
            "company": company,
            "industry": industry,
            "risk_score": score,
            "risk_level": level,
            "business_description": business_description,
            "summary": summary,
            "top_risks": risks,
            "recommendations": recommendations,
            "conclusion": conclusion,
            "analysis": analysis,
        }

        st.download_button(
            label="📥 Download JSON Report",
            data=json.dumps(json_data, indent=4),
            file_name=f"{company}_risk_report.json",
            mime="application/json",
            use_container_width=True,
        )

        st.divider()

        # =====================================================
        # EXCEL EXPORT
        # =====================================================

        workbook = Workbook()

        sheet = workbook.active
        sheet.title = "Risk Report"

        sheet.append(["Field", "Value"])
        sheet.append(["Company", company])
        sheet.append(["Industry", industry])
        sheet.append(["Risk Score", score])
        sheet.append(["Risk Level", level])

        sheet.append([])
        sheet.append(["Business Description"])
        sheet.append([business_description])

        sheet.append([])
        sheet.append(["Executive Summary"])
        sheet.append([summary])

        sheet.append([])
        sheet.append(["Top Risks"])

        for risk in risks:
            sheet.append([risk])

        sheet.append([])
        sheet.append(["Recommendations"])

        for rec in recommendations:
            sheet.append([rec])

        sheet.append([])
        sheet.append(["Final Conclusion"])
        sheet.append([conclusion])

        sheet.append([])
        sheet.append(["Complete AI Report"])

        for line in analysis.splitlines():
            sheet.append([line])

        excel_buffer = BytesIO()

        workbook.save(excel_buffer)

        excel_buffer.seek(0)

        st.download_button(
            label="📊 Download Excel Report",
            data=excel_buffer,
            file_name=f"{company}_risk_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.divider()


    except Exception as e:

        st.error("❌ Something went wrong while generating the report.")

        st.exception(e)

# =====================================================
# REPORT HISTORY
# =====================================================

st.divider()

st.subheader("📂 Report History")

reports = get_reports()

if reports:

    for report in reports[:10]:

        with st.expander(f"🏢 {report[0]}  |  {report[2]}/100  |  {report[3]}"):

            st.write(f"**Industry:** {report[1]}")
            st.write(f"**Risk Score:** {report[2]}")
            st.write(f"**Risk Level:** {report[3]}")
            st.write(f"**Created On:** {report[4]}")

            col1, col2 = st.columns([4, 1])

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{report[0]}_{report[4]}",
                ):

                    delete_report(report[0])

                    st.success("✅ Report Deleted")

                    st.rerun()

else:

    st.info("No reports found.")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption("🛡️ AI Enterprise Risk Assessment System | Powered by Google Gemini")
