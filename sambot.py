import os
import time
from slackclient import SlackClient
from login_request import email_request
from login_request import problema_request
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI')

print("Email detectado: ",email_request)

def fetch_id(email):
	user_info=sc.api_call(
			"users.lookupByEmail",
			email=email,
			)
	return user_info['user']


def send_message(userid,userdata):
    if userdata['profile']['display_name']=='':
        name=userdata['profile']['real_name']
    else:
        name=userdata['profile']['display_name']

    texto = "Olá " + name + "! Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n--status para ver o estado de resolução do seu problema.\n--cancelar para anular o seu report."

    sc.api_call(
        "chat.postMessage",
        as_user=True,
        channel=userid,
        text=texto,
    )


def commands(userid, status, problema_input):
    conv_info=sc.api_call(
        "conversations.open",
        users=userid,
        return_im=True,
    )
    
    ult_msg=conv_info['channel']['latest']['text']
    ult_msg=ult_msg.strip().lower()

    if ult_msg=='--status':
        text_status= problema_input + status
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text=text_status,
            )
        print("Comando --status detectado.")
        return status

    elif ult_msg=='--cancelar':
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text="Report cancelado com sucesso",
            )
        print("Comando --cancelar detectado")
        return " O report foi cancelado por você."

    else:
        return status

if __name__ == '__main__':
    email_input = email_request
    problema_input = str(problema_request + ":")
    u=fetch_id(email_input)
    send_message(u['id'],u)
    print("Successo: Primeira mensagem enviada!")
    status=" Não resolvido. A equipe já foi mobilizada e você será notificado quando o problema for solucionado."
    while 'true'=='true':
        status=commands(u['id'], status, problema_input)
        time.sleep(1)