import owlready2 as owl
onto = owl.get_ontology("file://../ontology/factory.owl").load()

import random

class Cookie:
    def __init__(self, size):
        self.burned = None
        self.size = size
    
with onto:
    class BurnedSensor(onto.Sensor):
        def __call__(self, cookie):
            self.has_value = 1 if cookie.burned else 0
            if self.has_value > self.alert_on_value_greater_then:
                self.raised_alert = [onto.Alert(self.name + '_alert')]
            return self.has_value

    class SizeSensor(onto.Sensor):
        def __call__(self, cookie):
            self.has_value = cookie.size
            if self.has_value > self.alert_on_value_greater_then:
                self.raised_alert = [onto.Alert(self.name + '_alert')]
            return self.has_value
    
    class CookieDoughCutter(onto.Component):
        def __call__(self):
            return Cookie(size=random.randint(1, 10))
            return cookie
    
    class Oven(onto.Component):
        def __call__(self, cookie):
            current_temperature = random.randint(150, 200)
            cookie.burned = current_temperature > 180
            return cookie
    
    class CookieInspector(onto.Component):
        def __call__(self, cookie):
            for sensor in self.has_sensor:
                sensor(cookie)