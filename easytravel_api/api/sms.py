from twilio.rest import Client
from django.conf import settings

account_sid = 'ACac687b62efa422001a1c42dd3ebff5e1'
account_token = '204b61a0c610636fe507af25f10a7aca'
TWILIO_VERIFICATION_SID = 'VAab5c1a9102ea422dd2a2beb006250424'

client = Client(account_sid, account_token)


def verifications(phone_number, medium):
    return client.verify \
        .services(TWILIO_VERIFICATION_SID) \
        .verifications \
        .create(to=phone_number, channel=medium)


def verification_checks(phone_number, token):
    return client.verify \
        .services(TWILIO_VERIFICATION_SID) \
        .verification_checks \
        .create(to=phone_number, code=token)
