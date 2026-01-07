import pandas as pd
from datetime import datetime
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

CSV_PATH = r"D:\Download\PythonProject\student_scores.csv"

SUBJECTS = ["DSA", "DVP", "DDCO", "OS", "OOPs with java"]


# -------------------- LOAD DATA --------------------
def load_student_data():
    df = pd.read_csv(CSV_PATH)

    df.rename(columns={
        "student_id": "Student_ID",
        "student_name": "Student_Name",
        "Subject": "Subject",
        "Score": "Score"
    }, inplace=True)

    # add timestamp if missing
    if "Timestamp" not in df.columns:
        df["Timestamp"] = datetime.now()

    return df


# -------------------- DASH APP --------------------
app = Dash(__name__)
app.title = "Real-Time Student Dashboard"


# -------------------- UI LAYOUT --------------------
app.layout = html.Div(

    style={
        "padding": "25px",
        "background": "linear-gradient(135deg, #eef2ff, #e6f7ff)",
        "minHeight": "100vh"
    },

    children=[

        # HEADER
        html.Div([
            html.H2("📊 Real-Time Interactive Student Performance Dashboard",
                    id="main_heading",
                    style={"textAlign": "center"}),

            html.P("Dashboard visualizing real-time CSV-based student performance data",
                   style={"textAlign": "center"})
        ], style={
            "background": "white",
            "padding": "18px",
            "borderRadius": "12px",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.15)",
            "marginBottom": "18px"
        }),

        # CONTROL PANEL
        html.Div([

            html.H4("⚙ Dashboard Controls"),

            html.Div(style={"display": "flex", "gap": "30px"}, children=[

                # SUBJECT FILTER
                html.Div([
                    html.Label("Select Subject"),
                    dcc.Dropdown(
                        id="subject_filter",
                        options=[{"label": s, "value": s} for s in SUBJECTS],
                        value="DSA",
                        clearable=False
                    )
                ]),

                # SCORE SLIDER
                html.Div([
                    html.Label("Filter Score Range"),
                    dcc.Slider(
                        id="score_slider",
                        min=40, max=100, step=5,
                        value=50,
                        marks={i: str(i) for i in range(40, 105, 10)}
                    )
                ]),

                # CHART TYPE SELECTOR
                html.Div([
                    html.Label("Select Chart Type"),
                    dcc.Dropdown(
                        id="chart_type",
                        value="bar",
                        clearable=False,
                        options=[
                            {"label": "Bar Chart", "value": "bar"},
                            {"label": "Line Chart", "value": "line"},
                            {"label": "Stacked Bar", "value": "stack"},
                            {"label": "Pie Chart", "value": "pie"},
                            {"label": "Heat-Map View", "value": "map"},
                            {"label": "3D Plot", "value": "3d"},
                            {"label": "Time-Series Plot", "value": "ts"},
                        ]
                    )
                ])
            ])

        ], style={
            "background": "white",
            "padding": "18px",
            "borderRadius": "12px",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.12)",
            "marginBottom": "18px"
        }),

        # FONT SETTINGS
        html.Div([

            html.H4("📝 Customize Heading Style"),

            html.Div(style={"display": "flex", "gap": "40px"}, children=[

                html.Div([
                    html.Label("Adjust Heading Font Size"),
                    dcc.Slider(
                        id="font_slider",
                        min=20, max=60, step=2,
                        value=30,
                        marks={i: str(i) for i in range(20, 65, 10)}
                    )
                ], style={"width": "50%"}),

                html.Div([
                    html.Label("Select Heading Font Style"),
                    dcc.Dropdown(
                        id="font_style",
                        value="Arial",
                        clearable=False,
                        options=[
                            {"label": "Arial", "value": "Arial"},
                            {"label": "Times New Roman", "value": "Times New Roman"},
                            {"label": "Courier New", "value": "Courier New"},
                            {"label": "Verdana", "value": "Verdana"},
                        ]
                    )
                ], style={"width": "40%"})
            ])
        ], style={
            "background": "white",
            "padding": "18px",
            "borderRadius": "12px",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.12)",
            "marginBottom": "18px"
        }),

        # GRAPH
        html.Div([
            dcc.Graph(id="live_score_graph")
        ], style={
            "background": "white",
            "padding": "15px",
            "borderRadius": "12px",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.12)",
            "marginBottom": "18px"
        }),

        # DATA TABLE
        html.Div([
            html.H3("📄 Current Student Data"),
            html.Div(id="data_table")
        ], style={
            "background": "white",
            "padding": "15px",
            "borderRadius": "12px",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.12)",
        }),

        dcc.Interval(id="update_interval", interval=3000, n_intervals=0)
    ]
)


# -------------------- GRAPH + TABLE CALLBACK --------------------
@app.callback(
    Output("live_score_graph", "figure"),
    Output("data_table", "children"),
    Input("update_interval", "n_intervals"),
    Input("subject_filter", "value"),
    Input("score_slider", "value"),
    Input("chart_type", "value")
)
def update_dashboard(_, subject, min_score, chart_type):

    df = load_student_data()

    filtered = df[
        (df["Subject"] == subject) &
        (df["Score"] >= min_score)
    ]

    # ---------- CHART TYPES ----------

    # Standard Line Chart
    if chart_type == "line":

        # sort by student id to keep order
        filtered = filtered.sort_values("Student_ID")

        # ensure readable axis values
        filtered["Student_ID"] = filtered["Student_ID"].astype(str)

        fig = px.line(
            filtered,
            x="Student_ID",  # ⬅ bottom axis
            y="Score",  # ⬅ left axis
            markers=True,
            title=f"Student Score Line Chart — {subject}",
        )

        fig.update_traces(mode="lines+markers")

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Student ID",
            yaxis_title="Score",
            margin=dict(l=40, r=20, t=50, b=40)
        )

        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True, zeroline=False)

    # Stacked Bar
    elif chart_type == "stack":
        fig = px.bar(
            filtered,
            x="Student_ID",
            y="Score",
            color="Subject",
            barmode="stack",
            title=f"Stacked Score View — {subject}"
        )

    # Pie Chart
    elif chart_type == "pie":
        fig = px.pie(
            filtered,
            names="Student_ID",
            values="Score",
            title=f"Score Distribution — {subject}"
        )

    # Heat Map
    elif chart_type == "map":
        fig = px.density_heatmap(
            filtered,
            x="Student_ID",
            y="Score",
            title=f"Score Heat-Map — {subject}"
        )

    # 3D Plot
    elif chart_type == "3d":

        filtered["Student_ID"] = filtered["Student_ID"].astype(str)

        # create attempt / test index per student
        filtered["Attempt_No"] = (
                filtered.groupby("Student_ID").cumcount() + 1
        )

        fig = px.scatter_3d(
            filtered,
            x="Student_ID",
            y="Score",
            z="Attempt_No",
            color="Student_Name",
            title=f"3D Performance Visualization — {subject}"
        )

        fig.update_traces(marker=dict(size=6))

        fig.update_layout(
            scene=dict(
                xaxis_title="Student ID",
                yaxis_title="Score",
                zaxis_title="Attempt Number",
                aspectmode="cube"
            ),
            margin=dict(l=10, r=10, t=50, b=10)
        )

    # ---------------- TIME-SERIES PLOT (Like Your Image) ----------------
    elif chart_type == "ts":
        filtered["Student_ID"] = filtered["Student_ID"].astype(str)

        filtered = filtered.sort_values("Student_ID")

        fig = px.line(
            filtered,
            x="Student_ID",
            y="Score",
            markers=True,
            title=f"Student Score Trend — {subject}",
        )

        fig.update_traces(mode="lines+markers")

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Student ID",
            yaxis_title="Score",
            margin=dict(l=40, r=20, t=50, b=40)
        )

        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True, zeroline=False)

        # monthly time ticks
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b %Y",
            rangeslider_visible=False,
            showgrid=True
        )

        fig.update_yaxes(showgrid=True, zeroline=False)

        # smooth single-line style
        fig.update_traces(mode="lines", line_shape="spline")

        # matching clean minimal look
        fig.update_layout(
            template="plotly_white",
            showlegend=False,
            margin=dict(l=40, r=20, t=50, b=40),
            yaxis_title="Score",
            xaxis_title="Student_id"
        )

        # monthly ticks
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b %Y",
            rangeslider_visible=False,
            showgrid=True
        )

        fig.update_yaxes(showgrid=True, zeroline=False)

    # Default Bar Chart
    else:
        fig = px.bar(
            filtered,
            x="Student_ID",
            y="Score",
            color="Student_ID",
            barmode="group",
            title=f"Student Scores — {subject}"
        )

    fig.update_layout(template="plotly_white")

    # ---------- DATA TABLE ----------
    table = html.Table([
        html.Thead(html.Tr([html.Th(c) for c in filtered.columns])),
        html.Tbody([
            html.Tr([html.Td(str(row[c])) for c in filtered.columns])
            for _, row in filtered.iterrows()
        ])
    ])

    return fig, table


# -------------------- HEADING STYLE --------------------
@app.callback(
    Output("main_heading", "style"),
    Input("font_slider", "value"),
    Input("font_style", "value")
)
def update_heading_style(font_size, font_family):
    return {
        "textAlign": "center",
        "fontSize": f"{font_size}px",
        "fontFamily": font_family,
        "fontWeight": "bold",
        "color": "#1f2e2e"
    }


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True)
