import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database import get_risk_trend


# ==========================
# Gauge Chart
# ==========================

def risk_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={
                "text": "Overall Risk Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": "#1565C0"
                },

                "steps": [

                    {
                        "range": [0, 35],
                        "color": "#43A047"
                    },

                    {
                        "range": [35, 70],
                        "color": "#FB8C00"
                    },

                    {
                        "range": [70, 100],
                        "color": "#E53935"
                    }

                ],

                "threshold": {

                    "line": {
                        "color": "black",
                        "width": 5
                    },

                    "value": score

                }

            }

        )
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig


# ==========================
# Pie Chart
# ==========================

def risk_pie():

    labels = [

        "Financial",
        "Operational",
        "Cyber",
        "Compliance",
        "Market"

    ]

    values = [

        30,
        25,
        20,
        15,
        10

    ]

    fig = px.pie(

        names=labels,

        values=values,

        hole=0.45,

        title="Risk Distribution"

    )

    fig.update_layout(

        height=380,

        legend_title="Category"

    )

    return fig


# ==========================
# Bar Chart
# ==========================

def risk_bar():

    df = pd.DataFrame({

        "Risk": [

            "Financial",

            "Operational",

            "Cyber",

            "Compliance",

            "Market"

        ],

        "Severity": [

            85,

            70,

            90,

            55,

            60

        ]

    })

    fig = px.bar(

        df,

        x="Risk",

        y="Severity",

        text="Severity",

        title="Risk Severity"

    )

    fig.update_traces(

        textposition="outside"

    )

    fig.update_layout(

        height=380,

        yaxis_range=[0, 100]

    )

    return fig


# ==========================
# Trend Chart
# ==========================

def risk_trend():

    records = get_risk_trend()

    if not records:

        fig = go.Figure()

        fig.update_layout(
            title="Risk Trend",
            height=350
        )

        return fig

    companies = []

    scores = []

    for row in records:

        companies.append(row[0])

        scores.append(row[1])

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=companies,

            y=scores,

            mode="lines+markers",

            name="Risk Score"

        )

    )

    fig.update_layout(

        title="Historical Risk Trend",

        xaxis_title="Company",

        yaxis_title="Risk Score",

        yaxis=dict(range=[0,100]),

        height=400

    )

    return fig