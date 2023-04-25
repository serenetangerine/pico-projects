import machine
import urequests
import wifi


def getUrl(url):
    requests = urequests.get(url)
    content = requests.content
    requests.close()
    return content


def main():
    # turn on LED so we know the pi is powered on
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()

    connection = wifi.WIFI()

    print(getUrl('https://api.ipify.org'))


if __name__ == '__main__':
    main()