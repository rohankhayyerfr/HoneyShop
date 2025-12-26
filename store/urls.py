from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list/', views.product_list, name="product_list"),
    # urls.py
    path('product/<slug:slug>/', views.product_detail, name='product_detail')

]

