from twilio.rest import Client
from .models import *
# Set environment variables for your credentials
# Read more at http://twil.io/secure


def sendSMS(x):

    account_sid = "ACc186d2e49cf13aa59462f0d82890ce3d"
    auth_token = "2c1d0bdfcef088b6fb9fa4f0aed25eb4"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Hello {x}, Donor have requested you to receive dontaion. Thankyou!!",
        from_="+14342803442",
        to="+9779818279844"
    )

    print("message send successfully!!")
