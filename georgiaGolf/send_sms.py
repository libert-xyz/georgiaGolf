from twilio.rest import Client
import env

# Your Account Sid and Auth Token from twilio.com/console
account_sid = env.account_sid
auth_token = env.auth_token

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Golf Georgia - https://golfgeorgia.info/ansley-golf-club",
                     from_='+14702645974',
                     to='+14717191900'
                 )

print(message.sid)
