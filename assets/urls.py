from django.urls import path
from . import views

urlpatterns = [
    path('', views.assets, name="assets"),
    path('asset/<str:pk>/', views.asset, name="asset"),

    path('create-asset/', views.createAsset, name="create-asset"),

    path('update-asset/<str:pk>/', views.updateAsset, name="update-asset"),

    path('delete-asset/<str:pk>/', views.deleteAsset, name="delete-asset"),
]
