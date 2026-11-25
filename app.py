import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Weather Dashboard Pro",
    page_icon="🌦️",
    layout="wide"
)

# ---------- PROFESSIONAL DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,
    #07111f, #102b50, #164e75);
    color: white;
}

h1, h2, h3, p, label, span {
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    padding: 15px;
}

.subtitle {
    text-align: center;
    color: #c7e7ff;
    font-size: 17px;
}

.weather-card {
    background: linear-gradient(135deg,
    rgba(75,160,230,0.35),
    rgba(255,255,255,0.10));
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 25px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.temperature {
    font-size: 75px;
    font-weight: 900;
    margin: 5px;
}

.city-name {
    font-size: 30px;
    font-weight: bold;
}

.weather-icon {
    width: 110px;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.12);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.2);
}

.stButton button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    border: none;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    width: 100%;
}

.forecast-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 18px;
    padding: 12px;
    text-align: center;
}

.footer {
    text-align: center;
    color: #c7e7ff;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    '<div class="main-title">🌦️ WEATHER DASHBOARD PRO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real-Time Weather Information Around The World</div>',
    unsafe_allow_html=True
)

st.write("")

# ---------- SEARCH SECTION ----------
col1, col2 = st.columns([3, 2])

with col1:
    city = st.text_input(
        "📍 Enter City Name",
        value="Kolkata"
    )

with col2:
    api_key = st.text_input(
        "🔑 OpenWeatherMap API Key",
        type="password"
    )

search = st.button("🔍 GET LIVE WEATHER")

# ---------- WEATHER FUNCTION ----------
def get_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        url, params=params, timeout=15
    )

    response.raise_for_status()
    return response.json()


def get_forecast(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        url, params=params, timeout=15
    )

    response.raise_for_status()
    return response.json()


# ---------- DISPLAY WEATHER ----------
if search:

    if not city.strip() or not api_key.strip():
        st.warning("Please enter city name and API key.")

    else:
        try:
            with st.spinner("Loading live weather..."):

                data = get_weather(city, api_key)
                forecast = get_forecast(city, api_key)

            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            visibility = data.get("visibility", 0) / 1000

            description = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]

            city_name = data["name"]
            country = data["sys"]["country"]

            st.success("Weather data loaded successfully!")

            # MAIN WEATHER CARD
            st.markdown(f"""
            <div class="weather-card">
                <div class="city-name">
                    📍 {city_name}, {country}
                </div>

                <img class="weather-icon"
                src="https://openweathermap.org/img/wn/{icon}@4x.png">

                <div class="temperature">
                    {temp:.1f}°C
                </div>

                <h3>{description.title()}</h3>

                <p>Feels Like {feels:.1f}°C</p>
                <p>Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # WEATHER DETAILS
            st.subheader("🌡️ Weather Details")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("💧 Humidity", f"{humidity}%")
            c2.metric("💨 Wind Speed", f"{wind} m/s")
            c3.metric("🌡️ Pressure", f"{pressure} hPa")
            c4.metric("👁️ Visibility", f"{visibility:.1f} km")

            # HOURLY FORECAST
            st.write("")
            st.subheader("🕒 Hourly Forecast")

            hourly = forecast["list"][:8]

            cols = st.columns(4)

            for i, item in enumerate(hourly):
                with cols[i % 4]:

                    hour = datetime.fromtimestamp(
                        item["dt"]
                    ).strftime("%I %p")

                    htemp = item["main"]["temp"]
                    hicon = item["weather"][0]["icon"]

                    st.markdown(f"""
                    <div class="forecast-card">
                        <p>{hour}</p>
                        <img width="65"
                        src="https://openweathermap.org/img/wn/{hicon}@2x.png">
                        <h3>{htemp:.1f}°C</h3>
                        <p>{item["weather"][0]["main"]}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # FIVE DAY FORECAST
            st.write("")
            st.subheader("📅 5-Day Weather Forecast")

            daily = {}

            for item in forecast["list"]:

                day = datetime.fromtimestamp(
                    item["dt"]
                ).strftime("%a, %d %b")

                if day not in daily:
                    daily[day] = []

                daily[day].append(item)

            forecast_cols = st.columns(5)

            for i, (day, items) in enumerate(
                list(daily.items())[:5]
            ):

                avg_temp = sum(
                    x["main"]["temp"] for x in items
                ) / len(items)

                weather = items[0]["weather"][0]["main"]
                ficon = items[0]["weather"][0]["icon"]

                with forecast_cols[i]:

                    st.markdown(f"""
                    <div class="forecast-card">
                        <p>{day}</p>
                        <img width="70"
                        src="https://openweathermap.org/img/wn/{ficon}@2x.png">
                        <h3>{avg_temp:.1f}°C</h3>
                        <p>{weather}</p>
                    </div>
                    """, unsafe_allow_html=True)

        except requests.exceptions.HTTPError:
            st.error("Invalid city or API key. Please check again.")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {e}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    🌦️ Weather Dashboard Pro
    <br>
    Developed with Python & Streamlit
    <br>
    © 2026 My Weather App
</div>
""", unsafe_allow_html=True)