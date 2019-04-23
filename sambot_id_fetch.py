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
        text="Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n--status para ver o estado de resolução do seu problema.\n --cancelar para cancelar seu último report.",
    )


def commands(userid, status):
    conv_info=sc.api_call(
        "conversations.open",
        users=userid,
        return_im=True,
    )
    ult_msg=conv_info['channel']['latest']['text']

    if ult_msg=='--status':
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text=status,
            )
        print("Comando --status detectado.")

    elif ult_msg=='--cancelar':
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text="Report cancelado com sucesso",
            )
        return "O report foi cancelado por você."
        print("Comando --cancelar detectado")
    else:
        return status

if __name__ == '__main__':
    email_input = input("Email: ")
    u=fetch_id(email_input)
    send_message(u['id'])
    print("Successo: Primeira mensagem enviada!")
    status="A equipe já foi mobilizada. Você será notificado quando seu problema for resolvido"
    while 'true'=='true':
        status=commands(u['id'], status)

