from django.conf import settings
from django.db import models
from animes.models import anime
from django.core.urlresolvers import reverse

# Create your models here.

class Item(models.Model):
    #associations
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    anime       = models.ForeignKey(anime)
    #Actual Item Data
    name        = models.CharField(max_length=120)
    contents    = models.TextField(default='')
    public      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ['-updated','-timestamp']


    def get_contents(self):
        return self.contents.split(",")

    def get_absolute_url(self):
        # return f"/animes/{self.slug}"
        return reverse('episodes:detail', kwargs={'pk': self.pk})
