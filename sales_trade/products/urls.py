from django.urls import path
from .views import product_detail, product_list
from .api_views import (ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView)
urlpatterns = [
    
    # API endpoints
    path("", ProductListCreateView.as_view(), name="product-list-create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),

    # HTML template views
    path("template/products/", product_list, name="product_list"),
    path("template/products/<int:product_id>/", product_detail, name="product_detail"),

]
