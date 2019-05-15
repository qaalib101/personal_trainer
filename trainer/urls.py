from . import views, views_client

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'trainer'

urlpatterns = [

    path('', views.homepage, name='homepage'),

    # Account related
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('user/profile/', views.my_user_profile, name='my_user_profile'),
    path('user/profile/<int:user_pk>/', views.user_profile, name='user_profile'),
    path('user/profile/edit/', views_client.setup_client, name='edit_profile'),

    path('client/progress/add/', views_client.submit_progress, name='submit_progress'),
    path('client/progress/get/<int:pk>/', views_client.get_progress, name='get_progress'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''# User related
    path('user/profile/', views.my_user_profile, name='my_user_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    '''