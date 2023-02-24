"""Layout for the app."""
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from config import settings


def get_layout(app):
    # create navbar
    navbar = _create_navbar(app)

    # max total funding on slider
    max_funding = 100000000

    # create layout
    layout = html.Div(
        [
            navbar,
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # metric selection
                                html.Br(),
                                html.H3("Selected metrics"),
                                dcc.Dropdown(
                                    id="metric-dropdown",
                                    options=[
                                        metric for metric in settings.GROWTH_METRICS
                                    ],
                                    placeholder="Select a metric",
                                    multi=True,
                                    value=[
                                        metric for metric in settings.GROWTH_METRICS
                                    ],
                                ),
                                # slider for total funding selection
                                html.Br(),
                                html.H3("Select a total funding range"),
                                dcc.RangeSlider(
                                    id="total-funding-slider",
                                    min=0,
                                    max=max_funding,
                                    step=1000000,
                                    value=[0, settings.DEFAULT_FUNDING_FILTER],
                                    marks={
                                        0: "0",
                                        10000000: "10M",
                                        20000000: "20M",
                                        30000000: "30M",
                                        40000000: "40M",
                                        50000000: "50M",
                                        60000000: "60M",
                                        70000000: "70M",
                                        80000000: "80M",
                                        90000000: "90M",
                                        100000000: "100M",
                                    },
                                ),
                                # show selection of slider below
                                html.Br(),
                                html.Div(id="total-funding-slider-output"),
                                # metric for figure
                                html.Br(),
                                html.H3("Select a metric for the figure"),
                                dcc.Dropdown(
                                    id="figure-metric-dropdown", value="employees"
                                ),
                                # TODO: add metric weighting option
                                # refresh button
                                html.Br(),
                                html.Br(),
                                html.A(
                                    dbc.Button(
                                        "Refresh",
                                        id="refresh-button",
                                        color="primary",
                                    ),
                                    href="/",
                                ),
                            ],
                            width={
                                "size": 3,
                            },
                            style={
                                "padding-right": "20px",
                                "border-right": "1px solid #ccc",
                            },
                        ),
                        dbc.Col(
                            [
                                # spinner
                                dbc.Spinner(
                                    [
                                        # growth plot
                                        html.Br(),
                                        html.H3("Metric growth over time"),
                                        dcc.Graph(id="growth-plot"),
                                        # table
                                        html.H3("Output table - top 500"),
                                        dash_table.DataTable(
                                            id="growth-table",
                                            style_table={
                                                "overflowY": "scroll",
                                                "overflowX": "scroll",
                                                "height": "400px",
                                            },
                                            style_cell={
                                                "textAlign": "left",
                                                "fontFamily": "sans-serif",
                                                "fontSize": "12px",
                                            },
                                            style_header={
                                                "backgroundColor": "rgb(230, 230, 230)",
                                                "fontWeight": "bold",
                                                "fontSize": "12px",
                                            },
                                            # limit table height
                                            style_data_conditional=[
                                                {
                                                    "if": {"row_index": "odd"},
                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                },
                                                # highlight growth_kpi column
                                                {
                                                    "if": {"column_id": "growth_kpi"},
                                                    "backgroundColor": "rgb(230, 230, 230)",
                                                    "fontWeight": "bold",
                                                },
                                            ],
                                            # be able to order columns
                                            sort_action="native",
                                        ),
                                    ],
                                    color="primary",
                                    size="lg",
                                    type="border",
                                ),
                            ],
                            width={
                                "size": 9,
                            },
                            style={"padding-left": "20px"},
                        ),
                    ],
                ),
                fluid=True,
                style={"padding": "0.5rem 3rem 0.5rem 3rem"},
            ),
        ]
    )

    return layout


def _create_navbar(app):
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url("specter-logo.png"),
                                    height="30px",
                                )
                            ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "High Growth Companies v{}".format(
                                        settings.VERSION
                                    ),
                                    className="ms-2",
                                    style={"margin-left": "6rem"},
                                )
                            ),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    # vertical alignment of logo / brand center
                    style={"vertical-align": "middle"},
                ),
            ],
            fluid=True,
            style={"padding": "0.5rem 3rem 0.5rem 3rem"},
        ),
    )
    return navbar
