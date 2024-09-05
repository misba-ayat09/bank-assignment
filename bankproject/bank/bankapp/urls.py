from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-account/', views.create_account, name='create-account'),
    path('transaction/', views.transaction, name='transaction'),
    path('logout/', views.logout_view, name='logout'),  # Add this line
]

