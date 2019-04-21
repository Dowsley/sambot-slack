import os
from slackclient import SlackClient
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI')



def fetch_id():
	email_input = input("Email: ")
	user_info=sc.api_call(
			"users.lookupByEmail",
			email=email_input,
			)
	return user_info['user']


def send_message(userid):
    sc.api_call(
        "chat.postMessage",
        channel=userid,
        text="Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n/status para ver o estado de resolução do seu problema. ",
        username='SAMBOT',
        icon_emoji=':dog:'
    )

if __name__ == '__main__':
 	u=fetch_id()
 	send_message(u['id'])
 	print("Success!")

