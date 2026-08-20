import plotly.graph_objects as go

def risk_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={"text": "Overall Risk Score"},

            gauge={
                "axis": {"range": [0,100]},

                "bar":{"color":"red"},

                "steps":[
                    {"range":[0,40],"color":"green"},
                    {"range":[40,70],"color":"yellow"},
                    {"range":[70,100],"color":"red"},
                ]
            }
        )
    )

    fig.update_layout(height=350)

    return fig