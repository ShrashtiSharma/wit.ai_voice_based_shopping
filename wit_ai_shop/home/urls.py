from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # Home view
    path('mic/', views.mic, name='mic'),           # Mic view (for /mic/)
    path('mic/mic', views.mic, name='mic_duplicate'), # Mic view (for /mic/mic)
    path('mic_con/', views.mic_con, name='mic_con'), # Mic control view
    path('product/', views.product, name='product'), # Product view
    path('products.html', views.products_view, name='products'),  # Products view
]
