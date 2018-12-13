from django.db import models

# Create your models here.
class anime(models.Model):
    name        = models.CharField(max_length=120)
    genre       = models.CharField(max_length=120, null=True,blank=True)
    review      = models.CharField(max_length=120, null=True,blank=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    # my_date     = models.DateField(auto_now=False,auto_now_add=False,null=True)

    def __str__(self):   #dunder method
        return self.name
