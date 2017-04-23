from django.db import models
import datetime

# Create your models here.
class Route(models.Model):
    bus_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.bus_number
    
class BusStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    bus_terminus = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    def previous(self):
        previous = self.route.busstop_set.filter(
            id__lt=self.id).order_by('id').last()
        return previous
    
    def get_time(self):
        return self.passedtime_set.filter(
            time__gte=datetime.date.today()).last().time
    
    def get_time_set(self):
        first = self.route.busstop_set.first()
        n = first.passedtime_set.count()
        if n > 5 :
            time_set = set()
            i = 0
            for time in self.passedtime_set.all():
                if i < n-5:
                    i += 1
                else:
                    time_set.add(time)
        else:
            time_set = self.passedtime_set.filter(
            time__gte=datetime.date.today())
        return time_set
    
    def add_time(self, time):
        self.passedtime_set.create(time=time)
        first = self.route.busstop_set.first()
        if (self.name != first.name):
            n = self.passedtime_set.count()
            if self.previous().passedtime_set.count() < n:
                self.previous().add_time(time)
        
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
