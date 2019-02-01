from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from .utils import unique_slug_generator
from .validators import validate_name, validate_genres

# Create your models here.

User = settings.AUTH_USER_MODEL
class anime(models.Model):
    owner       = models.ForeignKey(User)  #class_instance.model_set.all() #TO SHOW THE ASSOCIATIONS
    name        = models.CharField(max_length=120, validators=[validate_name])
    genre       = models.CharField(max_length=120, null=True,blank=True, validators=[validate_genres])
    review      = models.CharField(max_length=120, null=True,blank=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(null=True,blank=True)
    # my_date     = models.DateField(auto_now=False,auto_now_add=False,null=True)

    def __str__(self):   #dunder method
        return self.name

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        # return f"/animes/{self.slug}"
        return reverse('animes:detail', kwargs={'slug': self.slug})

    # def get_absolute_url():



def anime_pre_save_recieve(sender, instance, *args, **kwargs):
    instance.name = instance.name.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    return instance.name


# def anime_post_save_recieve(sender, instance, *args, **kwargs):
#     print('saved')
#     print(instance.timestamp)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()


pre_save.connect(anime_pre_save_recieve, sender=anime)

# post_save.connect(anime_post_save_recieve, sender=anime)
