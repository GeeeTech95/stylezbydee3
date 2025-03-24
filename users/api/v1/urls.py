from django.urls import path,include

from . import account,password,auth, notification


urlpatterns = [

 
   
    #AUTH
    path("register/",auth.Register.as_view(),name='register-api'),
    path("login/",auth.Login.as_view(),name='login-api'),
    path("logout/",auth.Logout.as_view(),name='logout-api'),
    

    #PASSWORD
    path("update-password/",account.UpdatePassword.as_view(),name='update-password-api'),
    path("password-reset/request-token/", password.ResetPasswordRequestToken.as_view(), name='request-password-reset-token-api'),
    path("password-reset/", include('django_rest_passwordreset.urls', namespace='reset-password-api')),


    #NOTIFICATION
    path("notification/",notification.NotificationList.as_view(),name = 'notification-list-api')

   

]