from django.urls import path
from . import views
from .views import LoginView, LogoutView


urlpatterns = [
    path('create/', views.create_store, name='create_store'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),  # AJAX URL
    path('login', LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout', LogoutView.as_view(), name='logout'),
    # Add additional paths as needed
]