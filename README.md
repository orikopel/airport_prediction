# Airport Traffic Prediction App

## Overview
This Streamlit application predicts future airport traffic using Facebook's Prophet library and provides interactive visualizations including a map view and forecast charts. The app is designed to help airport managers, analysts, and planners make data-driven decisions based on projected passenger traffic.

![image](https://github.com/user-attachments/assets/1d4a370e-1461-400f-b3da-1a3fe8c11403)

## Features
* Interactive map visualization of airports
* Time series forecasting of airport traffic using Prophet
* Customizable prediction parameters
* Visual representation of historical data and future predictions
* Easy-to-use interface for selecting airports and adjusting forecast date

## File Structure
* app.py: Main Streamlit application file
* predict_traffic.py: Contains functions for traffic prediction using Prophet
* plot_map.py: Handles the creation and rendering of the map visualization

## Installation
Clone the repository:

git clone https://github.com/orikopel/airport_prediction.git
cd airport-prediction
Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:
pip install -r requirements.txt

## Usage
To run the Streamlit app:
streamlit run app.py
Navigate to the provided local URL in your web browser to interact with the application.

## How It Works
* Data Input: Users can select an airport from the provided list.
* Map Visualization: The plot_map.py script generates an interactive map showing the location of airports and their predicted traffic.
* Traffic Prediction: The predict_traffic.py script uses the Prophet model to forecast future airport traffic based on historical data.

## Dependencies
* Streamlit
* Prophet
* Plotly
* Pandas
* NumPy

For a complete list of dependencies, refer to the requirements.txt file.

## Contributing
Contributions to improve the app are welcome. Please follow these steps:
* Fork the repository
* Create a new branch (git checkout -b feature/AmazingFeature)
* Commit your changes (git commit -m 'Add some AmazingFeature')
* Push to the branch (git push origin feature/AmazingFeature)
* Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
* Facebook's Prophet library for time series forecasting
* Streamlit for the interactive web application framework
* ESRI for map data

## Contact
Ori Kopelovich - orikopel@gmail.com

Project Link: https://github.com/orikopel/airport-prediction
