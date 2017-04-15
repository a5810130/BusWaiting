from django.db import models

# Create your models here.
class Route(models.Model):
    bus_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.bus_number
    
class BusStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    create = models.DateTimeField('create')
    bus_terminus = models.BooleanField()
    
    def __str__(self):
        return self.name
    
class PassedTime(models.Model):
    busStop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    time = models.DateTimeField('passed_time')
    
    def bus_number(self):
        return self.busStop.route.bus_number