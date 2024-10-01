from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mic/', views.mic, name='mic'),  # Added trailing slash
    path('mic_con/', views.mic_con, name='mic_con'),  # Added trailing slash
    path('product/', views.product, name='product'),  # Added trailing slash
]
