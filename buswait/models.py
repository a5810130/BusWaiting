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
    
    def previous(self):
        previous = self.route.busstop_set.filter(id__lt=self.id).order_by('create').last()
        return previous
    
    def get_time(self):
        return self.passedtime_set.last().time
        
    def find_bus_coming(self):
        n = self.passedtime_set.count()
        previous = self.previous()
        while True:
            if previous.passedtime_set.count() > n :
                return previous
            else:
                if previous.bus_terminus == True :
                    return self
                else :
                    previous = previous.previous()
    
class PassedTime(models.Model):
    busStop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    time = models.DateTimeField('passed_time')
