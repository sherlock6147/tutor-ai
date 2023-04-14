from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

# Create your models here.
class Learner(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    registered_on = models.DateTimeField(auto_now_add=True)

    @property
    def profile_img(self):
        img_url = "./static/learners/default.svg"
        social_account = SocialAccount.objects.get(user=self.user)
        if social_account:
            img_url = social_account.extra_data.get('picture')
        return img_url

    def __str__(self) -> str:
        return self.user.username

class Moderator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    @property
    def profile_img(self):
        img_url = "./static/learners/default.svg"
        social_account = SocialAccount.objects.get(user=self.user)
        if social_account:
            img_url = social_account.extra_data.get('picture')
        return img_url

    def __str__(self) -> str:
        return self.user.username