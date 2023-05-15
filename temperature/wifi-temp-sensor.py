from machine import ADC
import socket

from wifi import WIFI

class Temperature:
    def __init__(self):
        # initialize ADC 4 for temperature reading
        self.temp_sensor = ADC(4)
        self.readTemperature()
    

    def readTemperature(self):
        volts = self.temp_sensor.read_u16()
        volt_conversion = 3.3 / 65535
        self.tempC = volts * volt_conversion
        # calibrate the temperature
        self.tempC = 23 - (self.tempC - 0.706) / 0.001721
        self.convertToFahrenheit()
    

    def convertToFahrenheit(self):
        self.tempF = self.tempC * 9 / 5 + 32 


class WebTemperature:
    def __init__(self):
        # initiate temperature sensor
        self.sensor = Temperature()
        # create template
        self.html = """
        <html>
            <head>
                <title>Pico W Temp</title>
            </head>
            <body>
                <p>%s</p>
            </body>
        </html>
        """

        self.json = """
        {
            "temperature": "%s"
        }
        """
        
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(1)

        print('listening on', self.addr)
        self.listen()
    

    def listen(self):
        while True:
            try:
                cl, addr = self.sock.accept()
                print('client connected from', addr)
                request = cl.recv(1024)
                print(request)
                print('\n')

                # use this to specify multiple endpoints if necessary
                response = False
                endpoint = str(request).split(' ')[1]
                if endpoint == '/':
                    self.sensor.readTemperature()
                    #response = self.html % str(self.sensor.tempF)
                    response = self.json % str(self.sensor.tempF)
                elif endpoint == '/test':
                    response = self.html % 'you have found the secret location :)'
                
                if response:
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
                else:
                    cl.send('HTTP/1.0 404 Not Found')
                    response = """
                    <html>
                        <head>
                            <title>404 Not Found</title>
                        </head>
                        <body>
                            <h1>Not Found</h1>
                            <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
                        </body>
                    </html>
                    """
                    cl.send(response)
                    cl.close()
            except OSError as e:
                cl.close()
                print('connection closed')



def main():
    wifi = WIFI()
    server = WebTemperature()
    print(str(server.sensor.tempF))



if __name__ == '__main__':
    main()

