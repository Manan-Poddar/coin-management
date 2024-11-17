from django.db import models
from django.utils import timezone
from authentication.models import User

class Coin(models.Model):
    denomination = models.CharField(max_length=100)
    description = models.TextField()
    metal = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.denomination} ({self.year})"


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name        


class Condition(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CoinStateCondition(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    front_image = models.ImageField( upload_to="images/coins", blank=True, null=True, default="images/coins")
    back_image = models.ImageField( upload_to="images/coins/coin1.jpg", blank=True, null=True)

    class Meta:
        unique_together = ('coin', 'state', 'condition')

    def __str__(self):
        return f"{self.coin} - {self.state} - {self.condition}"


class UserCoinOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coin_ownerships')
    coin_state_condition = models.ForeignKey(CoinStateCondition, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    request = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'coin_state_condition')

    def __str__(self):
        return f"{self.user.email} owns {self.count} of {self.coin_state_condition.coin.denomination} in {self.coin_state_condition.state.name} for condition {self.coin_state_condition.condition.name}"        


class PushNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notification')
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_user')
    created_at = models.DateTimeField(default=timezone.now) 
    message = models.CharField( max_length=50)

    def __str__(self):
        return f"{self.user} - {self.message}"

class Contact(models.Model):
    name = models.CharField(max_length=50)  
    created_at = models.DateTimeField(default=timezone.now) 
    email = models.EmailField()  
    mobile_number = models.CharField(max_length=10) 
    message = models.CharField( max_length=250)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at