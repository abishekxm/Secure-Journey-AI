# Sending SMS
# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# sms.py or utils.py

from twilio.rest import Client
from django.conf import settings

def sendSms(phone_number, message):
    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    client.messages.create(
        to="+91" + phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )

    
    

