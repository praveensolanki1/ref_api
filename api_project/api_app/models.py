from django.db import models
import random
import string



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    referral_code = models.CharField(max_length=100, blank=True, null=True,unique=True)
    timestamp_of_registration = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def generate_referral_code(self):
        
        while True:
            referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not User.objects.exclude(pk=self.pk).filter(referral_code=referral_code).exists():
               return referral_code   



class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referee = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('referrer', 'referee')

    def __str__(self):
        return f"Referral from {self.referrer} to {self.referee}"   
    
