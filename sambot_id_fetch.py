import os
from slackclient import SlackClient
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI')


def fetch_id(email):
	user_info=sc.api_call(
			"users.lookupByEmail",
			email=email,
			)
	return user_info['user']


def send_message(userid):
    sc.api_call(
        "chat.postMessage",
        as_user=True,
        channel=userid,
        text="Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n/statusrelatorio para ver o estado de resolução do seu problema. ",
    )


if __name__ == '__main__':
    email_input = input("Email: ")
    u=fetch_id(email_input)
    send_message(u['id'])
    print("Successo: Primeira mensagem enviada!")

    
