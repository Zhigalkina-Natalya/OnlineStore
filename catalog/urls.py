from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView, ProductUnpublishView, CategoryProductListView
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/create/", ProductCreateView.as_view(), name="create_product"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("product/unpublish/<int:pk>/", ProductUnpublishView.as_view(), name="product_unpublish"),
    path("category/<int:category_id>/", CategoryProductListView.as_view(), name="category_products"),
]
