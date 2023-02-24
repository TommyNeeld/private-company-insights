"""callbacks for the app."""
from config import settings
from dash import Input, Output, State, dcc
import plotly.express as px
from preprocess import preprocessor
from data_loader import load_data


def callbacks(app):
    @app.callback(
        [
            Output("growth-plot", "figure"),
            Output("growth-table", "data"),
            Output("total-funding-slider-output", "children"),
            Output("figure-metric-dropdown", "options"),
        ],
        [
            Input("metric-dropdown", "value"),
            Input("total-funding-slider", "value"),
            Input("figure-metric-dropdown", "value"),
        ],
    )
    def refresh_figure_and_table(metrics, total_funding_range, metric):

        # load data (this is cached)
        df = load_data(settings.FILE_NAME)

        # preprocess data
        metrics = metrics if metrics else None
        processed_data = preprocessor(df, metrics=metrics)

        # filter by total funding range settings.TOTAL_FUNDING_COL
        processed_data = processed_data[
            (processed_data[settings.TOTAL_FUNDING_COL] >= total_funding_range[0])
            & (processed_data[settings.TOTAL_FUNDING_COL] <= total_funding_range[1])
        ]

        # plot
        top_n_figure = 15

        data = (
            processed_data[settings.GROWTH_METRICS[metric]["growth"]]
            .head(top_n_figure)
            .T
        )
        data.index = range(1, len(data) + 1)

        # mapping from specter ID to company name
        company_name_mapping = df["Company Name"].to_dict()
        data = data.rename(columns=company_name_mapping)

        fig = px.line(
            data,
            x=data.index,
            y=data.columns,
            title="Normalized {} Growth of Top {} Companies by Slope".format(
                metric, top_n_figure
            ),
            markers=True,
            template="plotly_white",
            line_shape="spline",
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Normalized {} Growth".format(metric),
            legend_title="Company",
        )

        # table
        columns = [
            "Company Name",
            "Website",
            settings.TOTAL_FUNDING_COL,
            "Ranking",
        ] + [f"{metric} growth" for metric in metrics]

        # only show 2 decimal places if float
        table_data = processed_data[columns].copy()
        for col in columns:
            if table_data[col].dtype == "float64":
                table_data[col] = table_data[col].apply(lambda x: round(x, 2))

        # show total funding range
        total_funding_range = "Total Funding Range: ${} - ${}".format(
            total_funding_range[0], total_funding_range[1]
        )

        # update dropdown options
        figure_metric_dropdown_options = [
            {"label": metric, "value": metric} for metric in metrics
        ]

        return (
            fig,
            table_data.to_dict("records"),
            total_funding_range,
            figure_metric_dropdown_options,
        )

    # modal
    @app.callback(
        Output("report-modal", "is_open"),
        [Input("open-report-modal", "n_clicks")],
        [State("report-modal", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output("download-csv", "data"),
        Input("download-csv-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        # load data (this is cached)
        df = load_data(settings.FILE_NAME)
        return dcc.send_data_frame(df.to_csv, "taxonomy_result.csv")
