from rest_framework.exceptions import PermissionDenied
from django.http import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from django.utils import timezone

from subscriptions.models import UserSubscription


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/api/v1/orders/":
            try:
                subscription = self.__check_has_subscription(request.user)
                self.__is_active(subscription)
            except PermissionDenied as err:
                return JsonResponse(
                    {"error": str(err)},
                    status=HTTP_403_FORBIDDEN
                    )
            
        return self.get_response(request)

    def __check_has_subscription(self, user):
        try: 
            return UserSubscription.objects.get(user=user)
        except UserSubscription.DoesNotExist:
            raise PermissionDenied("Subscription required")
        
    def __is_active(self, subscription):
        if subscription.end_date < timezone.now():
            raise PermissionDenied("Your subscription has expired")
        