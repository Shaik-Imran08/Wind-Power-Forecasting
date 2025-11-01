import streamlit as st
import requests
import pandas as pd

try:
    import folium
    import streamlit_folium as st_folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    st.error("Folium and streamlit-folium are required for map functionality. Please install them using: pip install folium streamlit-folium")

# -------------------------------------------------------------------
# Helper Functions for API Calls
# -------------------------------------------------------------------

def get_location_coordinates(city_name):
    """
    Fetches latitude and longitude for a city name using Open-Meteo's
    free, no-key geocoding API.
    """
    # Use the Open-Meteo Geocoding API (no key required)
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {'name': city_name, 'count': 1}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad response
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            location = data['results'][0]
            return {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'name': location.get('name', city_name),
                'country': location.get('country', '')
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching location data: {e}")
        return None

def get_weather_data(latitude, longitude):
    """
    Fetches real-time weather data using Open-Meteo's
    free, no-key forecast API.
    """
    # Use the Open-Meteo Weather Forecast API (no key required)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true',  # We want the real-time data
        'temperature_unit': 'celsius',
        'windspeed_unit': 'kmh',
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'current_weather' in data:
            return data['current_weather']
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_weather_forecast(latitude, longitude):
    """
    Fetches 5-day weather forecast using Open-Meteo's
    free, no-key forecast API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': ['temperature_2m_max', 'temperature_2m_min', 'weathercode'],
        'timezone': 'auto',
        'forecast_days': 5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'daily' in data:
            forecast = []
            for i in range(len(data['daily']['time'])):
                forecast.append({
                    'date': pd.to_datetime(data['daily']['time'][i]).strftime('%a %d'),
                    'temperature_max': data['daily']['temperature_2m_max'][i],
                    'temperature_min': data['daily']['temperature_2m_min'][i],
                    'weathercode': data['daily']['weathercode'][i]
                })
            return forecast
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")
        return None

# -------------------------------------------------------------------
# Weather Symbol & Animation Mapping (Requirement 3 & 4)
# WMO Weather interpretation codes
# Full list: https://open-meteo.com/en/docs
# -------------------------------------------------------------------

WEATHER_SYMBOLS = {
    0: ("☀️", "Clear sky"),
    1: ("🌤️", "Mainly clear"),
    2: ("🌥️", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),
    48: ("🌫️", "Depositing rime fog"),
    51: ("🌦️", "Light drizzle"),
    53: ("🌦️", "Moderate drizzle"),
    55: ("🌦️", "Dense drizzle"),
    56: ("🌧️", "Light freezing drizzle"),
    57: ("🌧️", "Dense freezing drizzle"),
    61: ("🌧️", "Slight rain"),
    63: ("🌧️", "Moderate rain"),
    65: ("🌧️", "Heavy rain"),
    66: ("🌧️", "Light freezing rain"),
    67: ("🌧️", "Heavy freezing rain"),
    71: ("🌨️", "Slight snow fall"),
    73: ("🌨️", "Moderate snow fall"),
    75: ("🌨️", "Heavy snow fall"),
    77: ("❄️", "Snow grains"),
    80: ("🌧️", "Slight rain showers"),
    81: ("🌧️", "Moderate rain showers"),
    82: ("🌧️", "Violent rain showers"),
    85: ("🌨️", "Slight snow showers"),
    86: ("🌨️", "Heavy snow showers"),
    95: ("⛈️", "Thunderstorm"),
    96: ("⛈️", "Thunderstorm with slight hail"),
    99: ("⛈️", "Thunderstorm with heavy hail"),
}

def get_weather_animation(weather_code):
    """
    Triggers a simple Streamlit animation based on weather.
    (Requirement 4)
    """
    if weather_code in [71, 73, 75, 77, 85, 86]:
        st.snow()
    elif weather_code in [95, 96, 99]:
        st.balloons() # Just for fun, as there's no thunderstorm effect
    # Add more as desired

# -------------------------------------------------------------------
# Main Streamlit Application (Requirement 2, 3, 4)
# -------------------------------------------------------------------

# Set page title and icon
st.set_page_config(page_title="Real-Time Weather", page_icon="🌦️")

# Initialize session state for location data
if 'location_data' not in st.session_state:
    st.session_state['location_data'] = None

# --- 1. APPLICATION TITLE ---
st.title("🌦️ Real-Time Weather Predictor")

# --- 2. DYNAMIC LOCATION SELECTION (Search or Map) ---
st.subheader("Select Location")

# Tabs for search and map selection
tab1, tab2 = st.tabs(["🔍 Search by City", "🗺️ Select on Map"])

with tab1:
    city = st.text_input("Enter a location to get the weather:", placeholder="e.g., London, Tokyo, New York", key="city_input")
    if city:
        location_data = get_location_coordinates(city)
        if location_data:
            st.session_state['location_data'] = location_data
            st.success(f"Selected: {location_data['name']}, {location_data['country']}")
        else:
            st.error(f"Could not find location: '{city}'. Please try again.")
            st.session_state['location_data'] = None

with tab2:
    if FOLIUM_AVAILABLE:
        st.write("Click on the map to select a location:")
        # Create a folium map centered on a default location (e.g., London)
        m = folium.Map(location=[51.505, -0.09], zoom_start=2)
        # Add a click event to capture coordinates
        m.add_child(folium.LatLngPopup())

        # Display the map and capture click data
        map_data = st_folium(m, height=400, width=700, key="map")

        if map_data and 'last_clicked' in map_data and map_data['last_clicked']:
            selected_lat = map_data['last_clicked']['lat']
            selected_lon = map_data['last_clicked']['lng']
            location_data = {
                'latitude': selected_lat,
                'longitude': selected_lon,
                'name': f"Lat: {selected_lat:.4f}, Lon: {selected_lon:.4f}",
                'country': ''
            }
            st.session_state['location_data'] = location_data
            st.success(f"Selected location: {location_data['name']}")
    else:
        st.warning("Map functionality is not available. Please install folium and streamlit-folium to use map selection.")
        st.info("You can still use the city search feature above.")

# --- 3. GET DATA AND DISPLAY WEATHER ---
location_data = st.session_state['location_data']
if location_data:
    st.subheader(f"Weather for {location_data['name']}, {location_data['country']}")

    weather_data = get_weather_data(location_data['latitude'], location_data['longitude'])

    if weather_data:
        # --- 4. DISPLAY WEATHER CONDITION & SYMBOL (Requirement 3) ---
        temp = weather_data['temperature']
        wind = weather_data['windspeed']
        weather_code = weather_data['weathercode']

        symbol, description = WEATHER_SYMBOLS.get(weather_code, ("❓", "Unknown"))

        # Enhanced layout with better styling
        st.markdown("""
        <style>
        .weather-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .forecast-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            color: white;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display in columns for a clean layout
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌡️ Temperature</h3>
                <h1>{temp}°C</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💨 Wind Speed</h3>
                <h1>{wind} km/h</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="weather-card">
                <p style='font-size: 60px; margin: 0;'>{symbol}</p>
                <h3>{description}</h3>
            </div>
            """, unsafe_allow_html=True)

        # --- 5. DISPLAY ANIMATION (Requirement 4) ---
        get_weather_animation(weather_code)

        # --- 6. Show a map of the location ---
        st.subheader("📍 Location Map")
        st.map(pd.DataFrame({
            'lat': [location_data['latitude']],
            'lon': [location_data['longitude']]
        }))

        # --- 7. Add 5-day forecast ---
        st.subheader("📅 5-Day Weather Forecast")
        forecast_data = get_weather_forecast(location_data['latitude'], location_data['longitude'])
        if forecast_data:
            cols = st.columns(5)
            for i, day in enumerate(forecast_data[:5]):
                with cols[i]:
                    day_symbol, day_desc = WEATHER_SYMBOLS.get(day['weathercode'], ("❓", "Unknown"))
                    st.markdown(f"""
                    <div class="forecast-card">
                        <h4>{day['date']}</h4>
                        <p style='font-size: 30px; margin: 5px 0;'>{day_symbol}</p>
                        <p>{day['temperature_max']}°C / {day['temperature_min']}°C</p>
                        <small>{day_desc}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Could not retrieve forecast data.")

    else:
        st.error("Could not retrieve weather data for this location.")

# --- About Section ---
st.sidebar.title("🌦️ About")
st.sidebar.info(
    """
    **Real-Time Weather Predictor** provides instant weather information using the **Open-Meteo API** (no API key required).

    **Features:**
    - 🔍 Search by city name
    - 🗺️ Interactive map selection
    - 🌡️ Real-time temperature & wind speed
    - 🎨 Dynamic weather symbols & animations
    - 📍 Location mapping

    **How to use:**
    1. Choose a location via search or map click.
    2. View current weather conditions instantly.
    3. Enjoy weather-based animations!

    Built with ❤️ using Streamlit & Folium.
    """
)
