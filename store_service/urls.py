from django.urls import path
from . import views

urlpatterns = [
    # Store Service

    # Index
    path('store/index/', views.Index, name="ApiIndex"),
    path('store/index/<slug:id_store>/', views.IndexStore, name="ApiIndexById"),

    # Category
    path('store/category/', views.Category, name="ApiCategory"),
    path('store/category/<int:id>/', views.Category, name="ApiCategoryById"),

    # Items
    path('store/item/', views.Item, name="ApiItems"),
    path('store/item/<int:id>/', views.Item, name="ApiItemsById"),

    # Carts
    path('store/cart/', views.Cart, name="ApiCarts"),
    path('store/cart/<int:id>/', views.Cart, name="ApiCartsById"),

    # Transaction
    path('store/transaction/', views.Transaction, name="ApiTransactions"),
    path('store/transaction/<int:id>/', views.Transaction, name="ApiTransactionsById"),

    # Search
    path('store/search/<slug:search>/', views.Search, name="ApiSearchItems"),

]