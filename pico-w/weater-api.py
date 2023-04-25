import machine
import secrets
from time import sleep
import urequests as requests
import wifi

# Expects secrets.py with the following format
#
# WEATHER_API_KEY = "your api key"


class WeatherAPI:
    def __init__(self, token, zip):
        print('Initializing Weather API...')
        self.token = token
        self.zip = str(zip)

        self.url = 'http://api.weatherapi.com/v1/current.json?key=%s&q=%s&aqi=no' % (self.token, self.zip)
        self.get_temperature()

    def get_temperature(self):
        print('Getting weather data...')
        resp = requests.get(url=self.url).json()
        
        # temperatures
        self.temp_c = resp['current']['temp_c']
        self.temp_f = resp['current']['temp_f']
        self.feelslike_c = resp['current']['feelslike_c']
        self.feelslike_f = resp['current']['feelslike_f']
        
        # conditions
        self.condition = resp['current']['condition']['text']
        self.wind_mph = resp['current']['wind_mph']
        self.wind_dir = resp['current']['wind_dir']
        self.wind_degree = resp['current']['wind_degree']
        self.pressure_mb = resp['current']['pressure_mb']
        self.precipitation = resp['current']['precip_in']
        self.humidity = resp['current']['humidity']
        self.cloud = resp['current']['cloud']
        self.visibility = resp['current']['vis_miles']
        self.uv = resp['current']['uv']
        self.gust_mph = resp['current']['gust_mph']
        print('Done!\n')




def main():
    # turn on LED so we know the pi is powered on
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()

    connection = wifi.WIFI()
    apiToken = secrets.WEATHER_API_KEY
    zipCode = '80817'

    weather = WeatherAPI(apiToken, zipCode)
    while True:
        print('\nReading:\n')
        print('Temperature: %s F' % weather.temp_f)
        print('Condition: %s' %weather.condition)
        print('Humidity: %s' % weather.humidity)
        print('Cloud: %s' % weather.cloud)
        print('Visibility: %s' % weather.visibility)
        print('UV: %s' % weather.uv)
        print('Wind MPH: %s' % weather.wind_mph)
        print('Wind Gust MPH: %s' % weather.gust_mph)
        print('\nTakin\' a snooze :)\n')
        # wait 15 minutes before performing the next check
        # so as to not abuse our free API :)
        sleep(900)



if __name__ == '__main__':
    main()