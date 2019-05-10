from . import views

from django.urls import path, re_path
from django.contrib.auth import views as auth_views


app_name = 'trainer'

urlpatterns = [

    path('', views.homepage, name='homepage'),

    # Account related
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('user/profile/<int:user_pk>/', views.user_profile, name='user_profile'),
    path('user/profile/edit/', views.setup_client, name='edit_profile'),
    path('regimen/change', views.add_regimen, name='edit_regimen')
]

'''# User related
    path('user/profile/', views.my_user_profile, name='my_user_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    '''