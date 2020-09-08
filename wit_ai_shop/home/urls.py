from django.urls import path
from home import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('mic',views.mic,name='mic'),
    path('mic_con',views.mic_con,name='mic_con'),
    path('product', views.product, name='product')
]

