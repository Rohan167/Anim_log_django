from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from .utils import unique_slug_generator
from .validators import validate_name, validate_genres

# Create your models here.

User = settings.AUTH_USER_MODEL

class animeQuerySet(models.query.QuerySet):
    def search(self,query):  #anime.objects.all().search(query)
        return self.filter(
        Q(name__icontains=query)|
        Q(genre__icontains=query)|
        Q(review__icontains=query)
        )

class animeModelManager(models.Manager):
    def get_queryset(self):
        return animeQuerySet(self.model, using=self._db)
    def search(self, query):  #anime.objects.search()
        return self.get_queryset().search(query)

class anime(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)  #class_instance.model_set.all() #TO SHOW THE ASSOCIATIONS
    name        = models.CharField(max_length=120, validators=[validate_name])
    genre       = models.CharField(max_length=120, null=True,blank=True, validators=[validate_genres])
    review      = models.CharField(max_length=120, null=True,blank=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    slug        = models.SlugField(null=True,blank=True)
    # author      = models.ForeignKey(User, on_delete=models.CASCADE)
    # my_date     = models.DateField(auto_now=False,auto_now_add=False,null=True)

    objects     = animeModelManager() #add Model.objects.all()
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
