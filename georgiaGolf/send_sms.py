from twilio.rest import Client
import env

# Your Account Sid and Auth Token from twilio.com/console
account_sid = env.account_sid
auth_token = env.auth_token

client = Client(account_sid, auth_token)


def send_message(number,golf_info):
    message = client.messages \
                    .create(
                         body=golf_info ,
                         from_='+14702645974',
                         to=number
                     )

    print(message.sid)
