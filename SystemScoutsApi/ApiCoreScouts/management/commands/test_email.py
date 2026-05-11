from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends a test email to verify SMTP configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send the test message to')

    def handle(self, *args, **kwargs):
        recipient = kwargs['recipient']
        subject = 'Test Email from SystemScoutsApi'
        message = 'This is a test email to verify that your SMTP configuration is working correctly.'
        email_from = settings.DEFAULT_FROM_EMAIL

        self.stdout.write(f"Attempting to send email to {recipient}...")
        self.stdout.write(f"From: {email_from}")
        self.stdout.write(f"Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        self.stdout.write(f"User: {settings.EMAIL_HOST_USER}")

        try:
            send_mail(
                subject,
                message,
                email_from,
                [recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent test email to {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
