import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium

# Function to generate mock data
def generate_mock_data(start_date, end_date, base_value, amplitude, frequency):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    t = np.arange(len(date_range))
    trend = base_value + amplitude * np.sin(2 * np.pi * frequency * t / len(t))
    noise = np.random.normal(0, amplitude / 4, len(t))
    values = trend + noise
    return pd.DataFrame({'date': date_range, 'value': values})

# Define the location and date range
location = {"name": "Bengaluru", "latitude": 12.9716, "longitude": 77.5946}

# Date range (5 years in the past to 5 years in the future)
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * 5)
future_end_date = end_date + timedelta(days=365 * 5)

# Generate mock datasets
datasets = {
    "Precipitation (mm/day)": generate_mock_data(start_date, future_end_date, 5, 3, 2),
    "Evapotranspiration (mm/day)": generate_mock_data(start_date, future_end_date, 3, 1, 1.5),
    "Humidity (%)": generate_mock_data(start_date, future_end_date, 60, 20, 1),
}

# Create subplots
fig = make_subplots(rows=3, cols=1, subplot_titles=list(datasets.keys()))

# Add traces to subplots
for i, (name, df) in enumerate(datasets.items(), start=1):
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['value'], mode='lines', name=name),
        row=i, col=1
    )

# Update layout
fig.update_layout(
    height=900,
    title_text=f"Irrigation Data Visualization for {location['name']}",
    showlegend=False,
    template="plotly_white"
)

# Create a map
m = folium.Map(location=[location['latitude'], location['longitude']], zoom_start=4)
folium.Marker(
    [location['latitude'], location['longitude']],
    popup=location['name'],
    tooltip=location['name']
).add_to(m)

# Save the map to an HTML string
map_html = m._repr_html_()

# Generate HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Irrigation Data Visualization for {location['name']}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2 {{
            color: #2c3e50;
            text-align: center;
        }}
        .container {{
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        #plotly-graph {{
            width: 100%;
            height: 900px;
        }}
        #map {{
            width: 100%;
            height: 400px;
        }}
    </style>
</head>
<body>
    <h1>Irrigation Data Visualization for {location['name']}</h1>
    <div class="container">
        <h2>Location Map</h2>
        {map_html}
    </div>
    <div class="container">
        <p>
            This visualization presents mock data for various climate parameters relevant to irrigation in {location['name']}.
            The data spans from {start_date.strftime('%Y-%m-%d')} to {future_end_date.strftime('%Y-%m-%d')}, including both historical and projected values.
            Please note that this is simulated data and should not be used for actual planning or decision-making.
        </p>
        <div id="plotly-graph"></div>
    </div>
    <script>
        var plotlyData = {fig.to_json()};
        Plotly.newPlot('plotly-graph', plotlyData.data, plotlyData.layout);
    </script>
</body>
</html>
"""

# Write HTML content to a file
with open("irrigation_data_visualization.html", "w") as file:
    file.write(html_content)

print("HTML file created successfully: irrigation_data_visualization.html")