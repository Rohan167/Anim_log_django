from django.contrib.auth import get_user_model


User    = get_user_model()

random_r  = User.objects.last()

#my followers

random_r.profile.followers.all()

#who I follow

randow_r.is_following.all()
