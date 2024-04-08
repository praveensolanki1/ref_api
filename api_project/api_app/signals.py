from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def generate_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = instance.generate_referral_code()
        instance.save()
