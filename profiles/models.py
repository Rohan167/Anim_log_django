from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from .utils import code_generator
from django.core.mail import send_mail
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
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    followers       = models.ManyToManyField(User, related_name='is_following', blank=True)
    image           = models.ImageField(default='default.jpg',upload_to='profile_pics')
    # following   = models.ManyToManyField(User, related_name='following', blank=True)
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects     = ProfileManager()
    def __str__(self):
        return self.user.username

    # 
    # def get_absolute_url(self):
    #     # return f"/animes/{self.slug}"
    #     return reverse('profiles:userupdate', kwargs={'username': self.user.username})

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator() #'SomeKey'
            self.save()
            path_p = reverse('activate', kwargs={'code':self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {path_p}'
            recipient_list = [self.user.email]
            html_message = f'<p>Activate your account here: {path_p}</p>'
            print(html_message)
            # sent_mail = send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)  #send_activation_email()
            # return sent_mail




def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created  = Profile.objects.get_or_create(user = instance)
        default_user_profile    = Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)
        # default_user_profile.save()
        profile.followers.add(default_user_profile.user)



post_save.connect(post_save_user_receiver, sender= User)
