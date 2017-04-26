from django.db import models
import datetime
from itertools import chain

# Create your models here.
class Route(models.Model):
    bus_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.bus_number
    
class BusStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    time = models.DateTimeField('time', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_previous(self):
        previous = self.route.busstop_set.filter(
            id__lte=self.id).order_by('-id')[:3]
        return previous
    
    def is_today(self):
        try:
            return datetime.date.today() == self.time.date()
        except:
            return False
    