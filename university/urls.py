from django.urls import path

from .views import (
    ApiRootAPIView,
    ContactMessageCreateAPIView,
    PartnershipDiscussionCreateAPIView,
)

urlpatterns = [
    path('', ApiRootAPIView.as_view(), name='api-root'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='contact-message-create'),
    path('partnership-discussions/', PartnershipDiscussionCreateAPIView.as_view(), name='partnership-discussion-create'),
]