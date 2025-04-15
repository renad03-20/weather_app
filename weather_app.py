from dotenv import load_dotenv
import os
import sys
import requests 
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout) # type: ignore
from PyQt5.QtCore import Qt 
import requests.exceptions 
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel('Enter City Name: ', self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()  

    def initUI(self):  
        self.setWindowTitle('Weather App')

        vbox = QVBoxLayout()  

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

        self.setStyleSheet("""
            QLabel, QPushButton{
            font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: 'Segoe UI emoji'
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        load_dotenv('key.env')
        api_key = os.getenv('API_KEY')
        api_key = '3047a809189fc4b7d75679547a2094a3'
        city = self.city_input.text()#!this function lets us get the text
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            #!whaen we make an api request we will get back a ressponse
            response = requests.get(url)
            response.raise_for_status()#!this method will rais an execption if there is an error
            data = response.json()#!convertin the response to jason

            if data['cod'] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error('Invalid Name: \nPlease Check your Input')
                case 401:
                    self.display_error('Unauthorized: \ninvalid API key')
                case 403:
                    self.display_error('Forbidden: \naccess is denied')
                case 404:
                    self.display_error('Not found: \nCity not found')
                case 500:
                    self.display_error('Internal Server error: \nplease try again later')
                case 502:
                    self.display_error('Bad gateway and invalid: \nresponse from the server')
                case 503:
                    self.display_error('Service unavailable: \navailable servers are down')
                case 504:
                    self.display_error('Gateway timeout: \nno response from the server')
                case _:
                    self.display_error(f"HTTP error occured: \n{http_error}")
                
        except requests.exceptions.RequestException as req_error:
            self.display_error(f'request error:\n{req_error}')
        except requests.exceptions.TooManyRedirects:
            self.display_error('too many redirect\ncheck the url')
        except requests.exceptions.Timeout:
            self.display_error('timeout error\n the request timed out')
        except requests.exceptions.ConnectionError:
            self.display_error('connection error\ncheck your internet connection')
        
    def display_error(self, message):
        self.temperature_label.setStyleSheet('font-size: 30px;')
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet('font-size: 75px;')
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        weather_description = data['weather'][0]['description']
        weather_id = data['weather'][0]['id']

        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.temperature_label.setText(f'{temperature_c:0f}°C')

    def get_weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return '⛈️'  # Thunderstorm
        elif 300 <= weather_id <= 321:
            return '🌦️'  # Drizzle
        elif 500 <= weather_id <= 531:
            return '🌧️'  # Rain
        elif 600 <= weather_id <= 622:
            return '❄️'  # Snow
        elif 701 <= weather_id <= 781:
            return '🌫️'  # Atmosphere (mist, smoke, haze, etc.)
        elif weather_id == 800:
            return '☀️'  # Clear sky
        elif 801 <= weather_id <= 804:
            return '☁️'  # Clouds
        else:
            return ''  
        
if __name__ == "__main__":  
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())