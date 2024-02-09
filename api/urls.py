from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views

from rest_framework.authtoken.views import  ObtainAuthToken

router = DefaultRouter()
router.register('v1/emp',views.EmployeeModelViewSetViewSet, basename='employees')
router.register('v1/task',views.TasksView, basename='tasks')


urlpatterns = [
    path('v1/token/',ObtainAuthToken.as_view())
    
] + router.urls
