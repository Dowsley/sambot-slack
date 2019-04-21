import os
from slackclient import SlackClient
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI')

def list_users():
    users_call = sc.api_call("users.list")
    if users_call.get('ok'):
        return users_call['members']
    return None

def send_message(userid):
    sc.api_call(
        "chat.postMessage",
        channel=userid,
        text="teste",
        username='SAMBOT',
        icon_emoji=':dog:'
    )

if __name__ == '__main__':   
    users = list_users()
    if users:
        for u in users:
            send_message(u['id'])
        print("Success!")



#sc.api_call(
 # "channels.info",
#  channel="#general"
#)

#sc.api_call(
#  "chat.postMessage",
#  channel='UJ2H2AR8X',
#  text="Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n/status para ver o estado de resolução do seu problema. "
#)