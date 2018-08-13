import psutil


class Seninfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get():
        d = {}

        try:
            d['sensors_temperature'] = psutil.sensors_temperature()
        except AttributeError:
            print("Temperature sensors not supported!")

        try:
            d['sensors_fans'] = psutil.sensors_fans()
        except AttributeError:
            print("Fan sensors not supported!")

        try:
            d['sensors_battery'] = psutil.sensors_battery()
        except:
            print("Battery sensors not supported!")

        return d
