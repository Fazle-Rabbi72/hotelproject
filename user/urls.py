from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
router = DefaultRouter()
router.register(r'user_list', views.UserViewset,)

urlpatterns = [
    path('', include(router.urls)),
    path('deposit/',views.DepositView.as_view(), name='deposit'),
    path('register/',views.UserRegistrationView.as_view(), name='register'),
    path('login/',views.UserLoginApiView.as_view(), name='login'),
    path('logout/',views.LogoutAPIview.as_view(), name='logout'),
    path('register/active/<uid64>/<token>/',views.active,name='activet'),
]
