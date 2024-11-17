from django.urls import path
from mycoinApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home' ),
    path('my_coin/', views.my_coin, name = 'my_coin' ),
    path('coins/<int:id>/', views.coins, name = 'coins' ),
    path('contact/', views.contact, name = 'contact' ),
    path('contact-request/', views.ContactRequest, name = 'contact-request'),
    path('login/', views.login, name = 'login' ),
    path('logout/', views.logout, name = 'logout' ),
    path('signup/', views.signup, name = 'signup' ),
    path('otp-verification/', views.otp_verification, name = 'otp-verification' ),
    path('coin-detail/<int:id>', views.coinDetail, name = 'coin-detail' ),
    path('submit-count', views.submitCount, name = 'submit-count' ),
    path('request-coin', views.requestCoin, name = 'request-coin' ),
    path('forgot_password', views.ForgotPassword, name= 'forgot-password'),
    path('reset_password/<str:token>/', views.ResetPassword, name = 'reset-password')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)