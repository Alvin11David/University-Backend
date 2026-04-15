from django.db import models


class ContactMessage(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField()
	subject = models.CharField(max_length=150)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name} - {self.subject}'


class PartnershipDiscussion(models.Model):
	full_name = models.CharField(max_length=120)
	email = models.EmailField()
	organization = models.CharField(max_length=180, blank=True)
	partnership_goal = models.CharField(max_length=180)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.full_name} - {self.partnership_goal}'
