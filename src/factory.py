import owlready2 as owl
onto = owl.get_ontology("http://test.org/factory.owl")

with onto:
    class Component(owl.Thing):
        pass
    
    class Sensor(owl.Thing):
        pass
    
    class Alert(owl.Thing):
        pass
    
    class has_sensor(Component >> Sensor):
        pass
            
    class raised_alert(Sensor >> Alert):
        pass
    
    # Inverse Property
    class prev_step(Component >> Component):
        pass
    
    class next_step(owl.ObjectProperty):
         domain           = [Component]
         range            = [Component]
         inverse_property = prev_step

    # Data Property
    class has_value(owl.DataProperty, owl.FunctionalProperty):
        domain = [Sensor]
        range = [int]
    
    class alert_on_value_greater_then(owl.DataProperty, owl.FunctionalProperty):
        domain = [Sensor]
        range = [int]
    
onto.save('ontology/factory.owl')