from django.urls import path
from . import views

urlpatterns = [
    path('login/with/phone/', views.LoginWithPhone.as_view(), name='login'),
    path('verify/main/phone/', views.VerifyPhoneMain.as_view(), name='login'),
    path('change/phone/', views.PhoneNumberChangeView.as_view(), name='changephone'),
    path('verify/changed/phone/', views.VerifyChangedPhoneNumber.as_view(), name='verifychangedphone'),
    path('resend/verify/code/', views.ResendVerifyCodeView.as_view(), name='resendcode')
]