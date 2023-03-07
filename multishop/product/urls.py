from django.urls import path
from product import views


app_name = 'product'
urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view(), name='product_detail')
]