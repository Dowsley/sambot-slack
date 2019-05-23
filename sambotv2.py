import MySQLdb # Lib para conectar com o banco de dados MySQL
import time  # Necessária para fazer delays no loop
from slackclient import SlackClient  # Lib principal para o bot funcionar
from database_connector import db_userinfo # Variável que carrega os dados de usuario do novo request
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI') # Token de controle do BOT

# Informações individuais sobre o report
email_input = db_userinfo['email_usuario']
problema_input = db_userinfo['problema_reportado']
status_input = db_userinfo['status']
id_usuarios_report = db_userinfo['id_usuarios_report']

print("Email detectado:", email_input)
print("Problema detectado:", problema_input)

# Conexão com o banco de dados
con = MySQLdb.connect(
    host="localhost",
    user="root",
    password="s4mb0t_cesarschool",
    port = 3306,
    db="database_report"
    )
print(con)

#Parametros do cursor estão definidos para retornar um dict
c = con.cursor(MySQLdb.cursors.DictCursor) 

# Seletor de informações
def select(fields, tables, where): 
    global c
    query = "SELECT " + fields + " FROM " + tables
    query += " WHERE " + where
    c.execute(query)
    return c.fetchall()

# Função que realiza update de informações (atualmente só cancela report)
def update(where):
    global c, con
    query = "UPDATE usuarios_report"
    query += " SET status = 'Cancelado'"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()

# Busca as info. de um usuário no workspace de acordo com o e-mail de entrada
def fetch_info(email): 
    user_info=sc.api_call(
            "users.lookupByEmail",
            email=email,
            )
    return user_info['user']

# Manda a primeira mensagem do BOT para o usuário
def send_firstmessage(slack_userinfo):
    if slack_userinfo['profile']['display_name']=='':
        name=slack_userinfo['profile']['real_name']
    else:
        name=slack_userinfo['profile']['display_name']

    texto = "Olá " + name + "! Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n\nSTATUS para ver o estado de resolução do seu problema.\n\nCANCELAR para anular o seu report."

    sc.api_call(
        "chat.postMessage",
        as_user=True,
        channel=slack_userinfo['id'],
        text=texto,
    )

# Reconhece comandos e os responde correspondentemente
def commands(userid, status, problema_input): 
    conv_info=sc.api_call(
        "conversations.open",
        users=userid,
        return_im=True,
    )
    
    ult_msg=conv_info['channel']['latest']['text']
    ult_msg=ult_msg.strip().upper()

    if ult_msg == 'STATUS':
        if "não resolvido" in status.strip().lower() or "nao resolvido" in status.strip().lower():
            text_status = problema_input + "Não resolvido. A equipe já foi mobilizada e você será avisado aqui quando o problema for solucionado"
        else:
            text_status= problema_input + status
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text=text_status,
            )
        print("Comando STATUS detectado.")

    elif ult_msg=='CANCELAR':
        cancelar=True
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text="Você tem certeza que quer cancelar seu report? Digite SIM para confirmar.",
            )
        print("Comando CANCELAR detectado")
        update(id_usuarios_report)

    elif ult_msg=='SIM' and confirm==True:
        sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text="Report cancelado com sucesso",
            )
        print("CONFIRMAÇÃO de CANCELAR detectado")
        update(id_usuarios_report)

# Estrutura de execução principal, chama todas as funções
if __name__ == '__main__':  
    passagem=False
    cancelar=False
    problema_input += ": "
    slack_userinfo=fetch_info(email_input)
    send_firstmessage(slack_userinfo)
    print("Successo: Primeira mensagem enviada!")
    while 'sam'=='sam':
        commands(slack_userinfo['id'], status_input, problema_input)
        status_input=select("status", "usuarios_report", "id_usuarios_report={}".format(id_usuarios_report))[0]['status']        
        
        if status_input.lower() =="resolvido" and passagem==False:
            sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=slack_userinfo['id'],
            text="Seu problema foi resolvido! Obrigado por contribuir com o SAM."
            )
            passagem=True
            print("Problema resolvido... Encerrando o script.")

        time.sleep(1)
        con.commit()