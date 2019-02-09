from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
# Create your models here.

User    = settings.AUTH_USER_MODEL


class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_p = Profile.objects.get(user__username__iexact=username_to_toggle)
        user    = request_user
        is_following = False
        if user in profile_p.followers.all():
            profile_p.followers.remove(user)
        else:
            profile_p.followers.add(user)
            is_following = True
        return profile_p, is_following

class Profile(models.Model):
    user        = models.OneToOneField(User)
    followers   = models.ManyToManyField(User, related_name='is_following', blank=True)
    # following   = models.ManyToManyField(User, related_name='following', blank=True)
    activated   = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects     = ProfileManager()
    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        pass



def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created  = Profile.objects.get_or_create(user = instance)
        default_user_profile    = Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)
        # default_user_profile.save()
        profile.followers.add(default_user_profile.user)



post_save.connect(post_save_user_receiver, sender= User)
