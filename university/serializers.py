from rest_framework import serializers

from .models import ContactMessage, PartnershipDiscussion


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'email', 'subject', 'message', 'created_at')
        read_only_fields = ('id', 'created_at')


class PartnershipDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipDiscussion
        fields = (
            'id',
            'full_name',
            'email',
            'organization',
            'partnership_goal',
            'message',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')