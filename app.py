import streamlit as st
import requests
import matplotlib.pyplot as plt

def fetch_weather_data(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def show_weather_info(weather_data, city):
    current = weather_data['current_condition'][0]
    st.header(f"Weather in {city.title()}")
    st.subheader(current['weatherDesc'][0]['value'])
    st.metric("🌡 Temperature", current['temp_C'] + " °C")
    st.metric("💧 Humidity", current['humidity'] + " %")
    st.metric("🌬 Wind Speed", current['windspeedKmph'] + " km/h")
    st.metric("🌫 Visibility", current['visibility'] + " km")
    st.write(f"Feels Like: {current['FeelsLikeC']} °C")
    st.info(f"🕒 Observation Time: {current['observation_time']} UTC")

def plot_hourly_temperature(data):
    hourly_data = data['weather'][0]['hourly']
    times = [f"{int(item['time'])//100:02d}:00" for item in hourly_data]
    temps = [int(item['tempC']) for item in hourly_data]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, temps, marker='o', color='tab:blue')
    ax.set_title("🌤 Hourly Temperature (Today)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_days_forecast(data):
    st.subheader("📊 Temperature Forecast Chart (Next 3 Days)")
    dates = [day['date'] for day in data['weather'][:3]]
    max_temps = [int(day['maxtempC']) for day in data['weather'][:3]]
    min_temps = [int(day['mintempC']) for day in data['weather'][:3]]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, max_temps, label="Max Temp", marker='o', color='red')
    ax.plot(dates, min_temps, label="Min Temp", marker='o', color='blue')
    ax.set_title("📅 3-Day Temperature Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def show_forecast_table(data):
    st.subheader("📋 Weather Forecast for Next 3-Days")
    for day in data['weather'][:3]:
        st.markdown(f"**📆 {day['date']}**")
        st.write(f"🌞 Max Temp: {day['maxtempC']} °C")
        st.write(f"🌙 Min Temp: {day['mintempC']} °C")
        st.write(f"🌤 Condition: {day['hourly'][4]['weatherDesc'][0]['value']}")
        st.write("---")

# Streamlit App UI
st.set_page_config("Weather App", "🌦")
st.title("🌦 Real-Time Weather App")

city = st.text_input("Enter your city:")

if st.button("Get Weather"):
    if city.strip():
        weather_data = fetch_weather_data(city)
        if weather_data:
            show_weather_info(weather_data, city)
            plot_hourly_temperature(weather_data)
            plot_days_forecast(weather_data)  # <-- Added this line
            show_forecast_table(weather_data)
        else:
            st.error("⚠️ Unable to fetch weather data. Try another city.")
    else:
          st.warning("Please enter a valid city name.")
  