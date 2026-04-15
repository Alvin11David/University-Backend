from django.contrib import admin

from .models import ContactMessage, PartnershipDiscussion


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'created_at')
	search_fields = ('name', 'email', 'subject', 'message')
	list_filter = ('created_at',)


@admin.register(PartnershipDiscussion)
class PartnershipDiscussionAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'email', 'organization', 'partnership_goal', 'created_at')
	search_fields = ('full_name', 'email', 'organization', 'partnership_goal', 'message')
	list_filter = ('created_at',)
