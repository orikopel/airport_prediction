import requests
import pandas as pd
import plotly.io as pio
from io import StringIO
from datetime import datetime, timedelta

import kaleido
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from prophet import Prophet

def load_traffic_data(traffic_path, airport_designator, start_date, end_date):
    """
    Loads and transforms traffic data from a CSV file.

    Args:
        traffic_path (str): The path to the CSV file containing traffic data.
        airport_designator (str): The designator of the airport for which to filter the data.
        start_date (datetime): The start date for filtering the data.
        end_date (datetime): The end date for filtering the data.
    Returns:
        traffic_data(pd.DataFrame): A DataFrame containing the transformed traffic data.
    """

    # load from file
    traffic_data = pd.read_csv(traffic_path)[["date_of_flight", "airport_country", "airport_name", "airport_designator", "max_total_traffic"]]
    traffic_data = traffic_data[traffic_data["airport_designator"] == airport_designator]

    # calc total traffic per day
    traffic_data = traffic_data.groupby(["date_of_flight", "airport_country", "airport_name", "airport_designator"]).agg({"max_total_traffic": "sum"}).reset_index()

    # format date column
    traffic_data["date_of_flight"] = pd.to_datetime(traffic_data["date_of_flight"], utc=False)
    traffic_data['date_of_flight'] = traffic_data['date_of_flight'].dt.tz_localize(None)
    traffic_data = traffic_data.rename({"airport_country":"airport_state"}, axis=1)

    # filter by date range
    traffic_data = traffic_data[(traffic_data["date_of_flight"] >= start_date) & (traffic_data["date_of_flight"] <= end_date)]

    # rename cols
    traffic_data.columns = ["date_of_flight", "airport_state", "airport_name", "airport_designator", "traffic"]

    return traffic_data

def plot_pred(forecast, pred_data, date_to_predict, predicted_value, plot_title):
    """
    Plot the predicted traffic data.

    Args:
        forecast (pd.DataFrame): A DataFrame containing the predicted traffic data.
        pred_data (pd.DataFrame): A DataFrame containing the actual traffic data.
        date_to_predict (str): The date for which to make predictions in the format 'YYYY-MM-DD'.
        predicted_value (float): The predicted traffic value for the specified date.

    Returns:
        fig: The plot of the predicted traffic data.
    """

    # visualize the prediction
    fig = px.line(forecast, x="ds", y="yhat", title=plot_title)
    fig.add_scatter(x=pred_data["ds"], y=pred_data["y"], mode="markers", name="Actual Traffic", marker=dict(color="gray", size=5))
    fig.add_scatter(x=[date_to_predict], y=[predicted_value], mode="markers", marker=dict(color="green", size=10), name="Predicted Traffic")
    fig.add_annotation(x=date_to_predict, y=predicted_value,
                      text="Predicted Traffic",
                      showarrow=False,
                      font=dict(size=16, color='white'),
                       xshift=10, yshift=15)

    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      xaxis_title_text='Date',
                      yaxis_title_text='Traffic',
                      xaxis_title_font_color='white',
                      yaxis_title_font_color='white',
                      xaxis_tickfont_color='white',
                      yaxis_tickfont_color='white',
                      showlegend=False
                      )
    return fig

def predict_traffic(data, date_to_predict, plot_title):
    """
    Use Prophet to predict traffic data for a specific airport and date.

    Args:
        data (pd.DataFrame): A DataFrame containing the traffic data.
        date_to_predict (str): The date for which to make predictions in the format 'YYYY-MM-DD'.

    Returns:
        predicted_value (float): The predicted traffic value for the specified date.
        plot: The plot of the predicted traffic data.
    """

    # try:
    # filter to get dataset for prediction
    pred_data = data[["date_of_flight", "traffic"]].copy()
    pred_data.columns = ["ds", "y"]
    pred_data = pred_data.dropna()

    # set and train model
    model = Prophet(daily_seasonality=False)
    model.fit(pred_data)

    # define date range for prediction results
    start_date = pred_data["ds"].min()
    #start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    date_to_predict = pd.to_datetime(date_to_predict, format='%Y-%m-%d')

    td = date_to_predict - start_date
    future = model.make_future_dataframe(periods=td.days, freq='D')

    # prediction
    future = future[(future['ds'] >= start_date) & (future['ds'] <= date_to_predict)]
    forecast = model.predict(future)
    predicted_value = forecast[forecast['ds'] == date_to_predict]['yhat'].values[0]

    fig = plot_pred(forecast, pred_data, date_to_predict, predicted_value, plot_title)

    return predicted_value, fig