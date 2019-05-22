import MySQLdb # Lib para conectar com o banco de dados MySQL
import time  # Necessária para fazer delays no loop
from slackclient import SlackClient  # Lib principal para o bot funcionar
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI') # Token de controle do BOT
from database_connector import db_userinfo # Variável que carrega os dados de usuario do novo request

email_input = db_userinfo['email_usuario']
problema_input = db_userinfo['problema_reportado']
status_input = db_userinfo['status']
id_usuarios_report = db_userinfo['id_usuarios_report']

print("Email detectado:", email_input)
print("Problema detectado:", problema_input)

con = MySQLdb.connect(
    host="localhost",
    user="root",
    password="s4mb0t_cesarschool",
    port = 3306,
    db="database_report"
    )
print(con)

c = con.cursor(MySQLdb.cursors.DictCursor) #Parametros do cursor estão definidos para retornar um dict (ou mandar?)

def update(where):
    global c, con
    query = "UPDATE usuarios_report"
    query += " SET status = 'O report foi cancelado por você.'"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()

def fetch_info(email): # Busca as info. de um usuário no workspace de acordo com o e-mail de entrada
    user_info=sc.api_call(
            "users.lookupByEmail",
            email=email,
            )
    return user_info['user']


def send_firstmessage(slack_userinfo): # Manda a primeira mensagem
    if slack_userinfo['profile']['display_name']=='':
        name=slack_userinfo['profile']['real_name']
    else:
        name=slack_userinfo['profile']['display_name']

    texto = "Olá " + name + "! Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n-status para ver o estado de resolução do seu problema.\n-cancelar para anular o seu report."

    sc.api_call(
        "chat.postMessage",
        as_user=True,
        channel=slack_userinfo['id'],
        text=texto,
    )


def commands(userid, status, problema_input): # Reconhece comandos e os responde
    conv_info=sc.api_call(
        "conversations.open",
        users=userid,
        return_im=True,
    )
    
    ult_msg=conv_info['channel']['latest']['text']
    ult_msg=ult_msg.strip().lower()

    if ult_msg=='-status':
        text_status= problema_input + status
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text=text_status,
            )
        print("Comando -status detectado.")
        return status

    elif ult_msg=='-cancelar':
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text="Report cancelado com sucesso",
            )
        print("Comando -cancelar detectado")
        update(id_usuarios_report)
        return "O report foi cancelado por você."

    else:
        return status

if __name__ == '__main__':  # Estrutura de execução, só entra se o programa for chamado
    problema_input += ": "
    slack_userinfo=fetch_info(email_input)
    send_firstmessage(slack_userinfo)
    print("Successo: Primeira mensagem enviada!")
    while 'true'=='true':
        status_input=commands(slack_userinfo['id'], status_input, problema_input)
        time.sleep(1)
        con.commit()