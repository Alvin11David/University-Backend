from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactMessage
from .serializers import ContactMessageSerializer


def _base_email_html(title, subtitle, accent, content_html):
	return f"""
	<!doctype html>
	<html>
	<head>
	  <meta charset=\"utf-8\" />
	  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
	  <title>{title}</title>
	</head>
	<body style=\"margin:0;padding:0;background:#f4f1ea;font-family:Segoe UI,Arial,sans-serif;color:#1f2937;\">
	  <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding:28px 14px;\">
	    <tr>
	      <td align=\"center\">
	        <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"max-width:680px;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #e5e7eb;\">
	          <tr>
	            <td style=\"padding:28px;background:{accent};color:#ffffff;\">
	              <div style=\"font-size:12px;letter-spacing:1.3px;text-transform:uppercase;opacity:0.9;\">University Portal</div>
	              <h1 style=\"margin:8px 0 0;font-size:28px;line-height:1.2;\">{title}</h1>
	              <p style=\"margin:10px 0 0;font-size:15px;opacity:0.94;\">{subtitle}</p>
	            </td>
	          </tr>
	          <tr>
	            <td style=\"padding:26px;\">
	              {content_html}
	            </td>
	          </tr>
	          <tr>
	            <td style=\"padding:18px 26px;background:#f8fafc;border-top:1px solid #e5e7eb;color:#64748b;font-size:12px;\">
	              This message was generated automatically by the University Portal contact service.
	            </td>
	          </tr>
	        </table>
	      </td>
	    </tr>
	  </table>
	</body>
	</html>
	"""


def _message_html(message_text):
	return escape(message_text).replace('\n', '<br>')


class ApiRootAPIView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(
			{
				'message': 'University Portal API',
				'endpoints': {
					'contact': '/api/contact/',
				},
			}
		)


class ContactMessageCreateAPIView(generics.CreateAPIView):
	queryset = ContactMessage.objects.all()
	serializer_class = ContactMessageSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		contact_message = serializer.save()

		university_email = getattr(settings, 'UNIVERSITY_CONTACT_EMAIL', '')
		if not university_email:
			return Response(
				{'detail': 'UNIVERSITY_CONTACT_EMAIL is not configured.'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR,
			)

		university_subject = f'University Portal Contact: {contact_message.subject}'
		university_body = (
			f'Name: {contact_message.name}\n'
			f'Email: {contact_message.email}\n'
			f'Subject: {contact_message.subject}\n\n'
			f'{contact_message.message}'
		)
		university_html = _base_email_html(
			title='New Contact Request',
			subtitle='A new message was submitted from your portal contact form.',
			accent='linear-gradient(135deg,#0f766e 0%,#155e75 100%)',
			content_html=(
				f'<p style="margin:0 0 12px;font-size:15px;"><strong>Name:</strong> {escape(contact_message.name)}</p>'
				f'<p style="margin:0 0 12px;font-size:15px;"><strong>Email:</strong> {escape(contact_message.email)}</p>'
				f'<p style="margin:0 0 16px;font-size:15px;"><strong>Subject:</strong> {escape(contact_message.subject)}</p>'
				'<div style="margin-top:8px;border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc;padding:16px;">'
				f'<p style="margin:0;font-size:15px;line-height:1.6;">{_message_html(contact_message.message)}</p>'
				'</div>'
			),
		)
		university_mail = EmailMultiAlternatives(
			subject=university_subject,
			body=university_body,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[university_email],
			reply_to=[contact_message.email],
		)
		university_mail.attach_alternative(university_html, 'text/html')
		university_mail.send(fail_silently=False)

		confirmation_subject = f'We received your message: {contact_message.subject}'
		confirmation_body = (
			f'Hello {contact_message.name},\n\n'
			'We received your message and will review it shortly.\n\n'
			f'Subject: {contact_message.subject}\n'
			f'Message:\n{contact_message.message}\n'
		)
		confirmation_html = _base_email_html(
			title='Message Received',
			subtitle=f'Thank you, {escape(contact_message.name)}. We have received your request.',
			accent='linear-gradient(135deg,#7c2d12 0%,#b45309 100%)',
			content_html=(
				'<p style="margin:0 0 16px;font-size:15px;line-height:1.65;">'
					'Our admissions support team will review your message and respond as soon as possible.'
				'</p>'
				'<div style="margin-top:6px;border:1px solid #e5e7eb;border-radius:12px;background:#fff7ed;padding:16px;">'
				f'<p style="margin:0 0 10px;font-size:15px;"><strong>Subject:</strong> {escape(contact_message.subject)}</p>'
				f'<p style="margin:0;font-size:15px;line-height:1.6;">{_message_html(contact_message.message)}</p>'
				'</div>'
			),
		)
		confirmation_mail = EmailMultiAlternatives(
			subject=confirmation_subject,
			body=confirmation_body,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[contact_message.email],
		)
		confirmation_mail.attach_alternative(confirmation_html, 'text/html')
		confirmation_mail.send(fail_silently=False)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
