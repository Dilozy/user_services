from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name = "subscriptions"

router = DefaultRouter()
router.register("subscriptions",
                views.UserSubscriptionViewSet,
                basename="user-subscriptions")

urlpatterns = [
    path("tariffs/", views.ListTariffsAPIView.as_view(), name="list_tariffs"),
]
urlpatterns.extend(router.urls)