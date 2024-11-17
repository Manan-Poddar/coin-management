from django.contrib import admin
from .models import *

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('denomination', 'description', 'metal', 'year')
    search_fields = ('denomination', 'description', 'metal', 'year')

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CoinStateCondition)
class CoinStateConditionAdmin(admin.ModelAdmin):
    list_display = ('coin', 'state', 'condition', 'price', 'front_image', 'back_image')
    search_fields = ('coin', 'state', 'condition', 'price', 'front_image', 'back_image')

@admin.register(UserCoinOwnership)
class UserCoinOwnershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_state_condition', 'count','request')
    search_fields = ('user', 'coin_state_condition', 'count','request')

@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_user', 'created_at','message')
    search_fields = ('user', 'request_user', 'created_at','message')