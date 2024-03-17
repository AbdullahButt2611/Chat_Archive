from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.signup, name='signup'),

    # Password Reset URLS
    path( 'password_ reset/' ,auth_views.PasswordResetView.as_view(),name='password_reset'),
    path( 'password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path(' reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
