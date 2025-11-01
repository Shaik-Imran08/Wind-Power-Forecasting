# 🌦️ Real-Time Weather Dashboard

![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0%2B-brightgreen.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An interactive, real-time weather dashboard built purely in Python. Select a location by searching for a city or clicking directly on an interactive map. This app is powered by Streamlit, Folium, and the **100% free, no-API-key-required** Open-Meteo API.

---

## 📸 Application Demo

*(It is highly recommended to replace this placeholder with a real screenshot or GIF of your app!)*

![Demo GIF of the Streamlit Weather App](https://placehold.co/800x400/262730/E0E2E6?text=Add+a+GIF+of+your+app+here!)

---

## ✨ Key Features

* **Real-Time Weather:** Get current temperature, wind speed, and weather conditions.
* **5-Day Forecast:** View a 5-day weather forecast with max/min temperatures and daily conditions.
* **Dual Location Input:**
    * **City Search:** Type any city name for instant results.
    * **Interactive Map:** Click anywhere on a `Folium` map to get the weather for that specific latitude and longitude.
* **Dynamic UI:** Weather-appropriate icons (emojis) and live animations (like `st.snow()` for snow) create an engaging user experience.
* **No API Key Needed:** Built with the free [Open-Meteo API](https://open-meteo.com/), allowing anyone to clone and run the app instantly.

---

## 🛠️ Tech Stack

* **Framework:** [Streamlit](https://streamlit.io/)
* **Weather Data:** [Open-Meteo API](https://open-meteo.com/) (Forecast & Geocoding)
* **Interactive Map:** [Folium](https://python-visualization.github.io/folium/) & [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
* **API/Data Handling:** [Requests](https://requests.readthedocs.io/en/latest/) & [Pandas](https://pandas.pydata.org/)

---

## 🌱 Project Evolution

This project began as a Jupyter Notebook (`Wind_Power_Generation_Forecasting.ipynb`) for analyzing and forecasting wind power generation using machine learning (Random Forest, Linear Regression).

It has since evolved into a fully-interactive, front-end web application focused on providing real-time, user-friendly weather data for any location in the world.

---

## 🚀 How to Run Locally

Get this application running on your local machine in 4 simple steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv
    
    # On Windows:
    .\venv\Scripts\activate
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run weather_app.py
    ```

Your default web browser will automatically open with the running application.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
