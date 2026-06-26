from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def test_email(request):
    send_mail(
        "TEST EMAIL",
        "Email system working",
        settings.EMAIL_HOST_USER,
        ["controlroom.official181@gmail.com"],
        fail_silently=False
    )
    return HttpResponse("Email sent")
