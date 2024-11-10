from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mic/', views.mic, name='mic'),
    path('mic_con/', views.mic_con, name='mic_con'),
    path('product/', views.product, name='product'),
    path('products.html', views.products_view, name='products'),  # Corrected to reference products_view
]
