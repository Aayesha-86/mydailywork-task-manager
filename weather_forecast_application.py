

# Import libraries
import requests
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from pyngrok import ngrok

# OpenWeatherMap API function to fetch weather data
def get_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main_data = data["main"]
        wind_data = data["wind"]
        weather_desc = data["weather"][0]["description"]
        
        weather_details = {
            "City": city,
            "Temperature": main_data["temp"],
            "Humidity": main_data["humidity"],
            "Wind Speed": wind_data["speed"],
            "Description": weather_desc
        }
        return weather_details
    else:
        return None

# Initialize the Dash app
app = Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Weather Forecast Dashboard"),
    
    # Input field for city
    dcc.Input(id='city-input', type='text', value='London'),
    html.Button(id='submit-btn', n_clicks=0, children='Submit'),
    
    # Display weather details
    html.Div(id='weather-output'),
    
    # Graph for temperature trend
    dcc.Graph(id='temp-graph')
])

# Callback to update weather information
@app.callback(
    [Output('weather-output', 'children'),
     Output('temp-graph', 'figure')],
    [Input('submit-btn', 'n_clicks')],
    [Input('city-input', 'value')]
)
def update_weather(n_clicks, city):
    api_key = 'your_openweathermap_api_key' # Replace with your actual API key
    weather_info = get_weather_data(city, api_key)
    
    if weather_info:
        weather_details = [
            html.P(f"City: {weather_info['City']}"),
            html.P(f"Temperature: {weather_info['Temperature']}°C"),
            html.P(f"Humidity: {weather_info['Humidity']}%"),
            html.P(f"Wind Speed: {weather_info['Wind Speed']} m/s"),
            html.P(f"Description: {weather_info['Description']}")
        ]
        
        # Placeholder 7-day forecast data (replace with real API data)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        temperatures = [20, 22, 19, 24, 25, 23, 21]
        
        # Create the graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days, y=temperatures,
            mode='lines+markers',
            line=dict(color='royalblue', width=2)
        ))
        fig.update_layout(
            title='7-Day Temperature Forecast',
            xaxis_title='Days',
            yaxis_title='Temperature (°C)',
            template='plotly_dark'
        )
        return weather_details, fig
    else:
        return [html.P("City not found!")], go.Figure()

# Set up ngrok tunnel
public_url = ngrok.connect(8050)
print("Dash app running at:", public_url)

# Run the Dash app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)