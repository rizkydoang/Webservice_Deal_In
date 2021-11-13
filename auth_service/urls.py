from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('user/signup/', views.SignUp, name='ApiSignup'),
    path('user/signup_store/<slug:username>/', views.SignUpStore, name='ApiSignupStore'),
    path('user/signup_store_auth/', views.SignUpStoreAuth, name='ApiSignupStoreAuth'),
    path('user/login/', views.Login, name='ApiLogin'),

    path('user/role/', views.Role, name='ApiRoles'),
    path('user/role/<int:id>/', views.Role, name='ApiRolesById'),
]