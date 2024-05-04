from django.urls import path, include
from rest_framework import routers

from .views import EventViewSet, RegistrationViewSet, TicketViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('registrations', RegistrationViewSet)
router.register('tickets', TicketViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
