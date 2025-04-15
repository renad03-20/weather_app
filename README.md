🌤️ Weather App — PyQt5 + OpenWeather API
A simple desktop weather application built using Python and PyQt5. It fetches real-time weather data using the OpenWeatherMap API and displays the current temperature, weather description, and an emoji representing the weather condition.

 Features
Enter any city name and get the current weather

Beautiful emoji representation of weather conditions (☀️ 🌧️ ❄️ etc.)

Handles API errors gracefully with user-friendly messages

Styled GUI using PyQt5

Uses environment variables for secure API key storage

Technologies Used
Python 3

PyQt5

OpenWeatherMap API

python-dotenv (load_dotenv for managing secrets)

 How to Run the App
Clone the repository: git clone https://github.com/renad03-20/weather_app.git cd weather_app

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

Install dependencies: 
pip install -r requirements.txt

Create a file named .env or key.env in the root directory and add your OpenWeather API key:
API_KEY=your_openweather_api_key

Run the app