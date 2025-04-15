from django.shortcuts import redirect
# import sendgrid 
# from django.core.mail import send_mail
from django.conf import settings
# from sendgrid.helpers.mail import Mail   

from django.core.mail import EmailMessage

def send_email(recipient, subject, html_content):
    print(f"Sending email to: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {html_content}")
    try:
        msg = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, [recipient])
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")

# def send_email(to, subject, content, sender='temf2006@gmail.com'):
#     sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
#     mail = Mail(
#         from_email=sender,
#         to_emails=to,
#         subject=subject,
#         html_content=content
#     )
#     return sg.send(mail)
