from django.urls import path

from .views import ApiRootAPIView, ContactMessageCreateAPIView

urlpatterns = [
    path('', ApiRootAPIView.as_view(), name='api-root'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='contact-message-create'),
]