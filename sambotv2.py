# Olá! Este SCRIPT (sambotv2) é o componente principal do programa, responsável por executar o BOT enquanto está rodando.
# Ele foi dividido em algumas partes para facilitar seu entendimento e execução.
# Para o BOT funcionar, o SCRIPT precisa resgatar informações de um novo report no banco de dados MySQL...
# ... e é isso que o segundo script (database_connector) faz: Mantém uma constante detecção e só para quando um novo report entra.
# Assim que as informações do novo report são importadas, a execução é retomada e o BOT começa a funcionar.




# --------------------------------------- IMPORT E CONEXÃO ---------------------------------------
import MySQLdb # Lib para conectar com o banco de dados MySQL
import time  # Necessária para fazer delays no loop
from slackclient import SlackClient  # Lib principal para o bot funcionar
from db_connector import db_userinfo # Variável que carrega os dados de usuario do novo request, executa segundo Script.

sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI') # Conexão com o token de controle do BOT

con = MySQLdb.connect( # Conexão com o banco de dados
    host="localhost",
    user="root",
    password="s4mb0t_cesarschool",
    port = 3306,
    db="database_report"
    )

print(con)

c = con.cursor(MySQLdb.cursors.DictCursor) # Parametros do cursor estão definidos para retornar um dict




# --------------------------------------- FUNÇÕES ---------------------------------------
def select(fields, tables, where): # Seleciona e devolve determinadas informações da DB.
    global c
    query = "SELECT " + fields + " FROM " + tables
    query += " WHERE " + where
    c.execute(query)
    return c.fetchall()


def update(where): # Função que realiza update (mudança) de informações na DB.
    global c, con
    query = "UPDATE usuarios_report"
    query += " SET status = 'Cancelado'"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()


def delete(where): # Deleta um report de usuário. Servirá pra cancelar seu report por vontade própria.
    global c, con
    query = "DELETE FROM usuarios_report"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()


def fetch_info(email): # Busca as info. de um usuário no workspace de acordo com o e-mail de entrada
    user_info=sc.api_call(
            "users.lookupByEmail",
            email=email,
            )
    return user_info['user']


def send_message(userid,text): # Manda uma mensagem (como BOT) para o usuário
    sc.api_call(
            "chat.postMessage",
            as_user=True,
            channel=userid,
            text=text
            )


def send_firstmessage(slack_userinfo): # Manda a primeira mensagem do BOT para o usuário
    if slack_userinfo['profile']['display_name']=='':
        name=slack_userinfo['profile']['real_name']
    else:
        name=slack_userinfo['profile']['display_name']

    texto = "Olá " + name + "! Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n\nSTATUS para ver o estado de resolução do seu problema.\nCANCELAR para anular o seu report."
    sc.api_call(
        "chat.postMessage",
        as_user=True,
        channel=slack_userinfo['id'],
        text=texto,
    )


def commands(userid, status, problema, primarykey): # Reconhece comandos e os responde correspondentemente
    conv_info=sc.api_call(
        "conversations.open",
        users=userid,
        return_im=True
    )
    
    ult_msg=conv_info['channel']['latest']['text']
    ult_msg=ult_msg.strip().upper()

    if ult_msg == 'STATUS':
        if "não resolvido" in status.strip().lower() or "nao resolvido" in status.strip().lower():
            text_status = problema + "Não resolvido. A equipe já foi mobilizada e você será notificado aqui quando o problema for solucionado."
        else:
            text_status= problema + status

        send_message(userid, text_status)
        print("Comando STATUS detectado.") # Debugger

    elif ult_msg=='CANCELAR':
        global cancelar
        cancelar=True
        text_status = "Você tem certeza que quer cancelar seu report? Digite SIM para confirmar ou NÃO para anular esta ação."
        send_message(userid, text_status)
        print("Comando CANCELAR detectado") # Debugger

    elif ult_msg=='SIM' and cancelar==True:
        text_status = "Report cancelado com sucesso. Você não receberá mais atualizações sobre o problema."
        send_message(userid, text_status)
        update(primarykey)
        print("CONFIRMAÇÃO de CANCELALAMENTO detectado") # Debugger

    elif (ult_msg=='NÃO' or ult_msg=='NAO') and cancelar==True:
        cancelar = False
        text_status = "Tudo bem, continuaremos o processo de resolução do problema."
        send_message(userid, text_status)
        print("ANULAÇÃO de CANCELAMENTO detectado") # Debugger




# --------------------------------------- RESGATE E DEFINIÇÃO DE INFORMAÇÕES ---------------------------------------
# As informações do request (importadas no começo do script) são divididas em informações menores e definidas.

email_input = db_userinfo['email_usuario'] # Email do usuário do Report
problema_input = db_userinfo['problema_reportado'] # Problema reportado
status_input = db_userinfo['status'] # Estado de resolução do problema
primarykey_input = db_userinfo['id_usuarios_report'] # Primarykey identificadora do report na tabela

print("Email detectado:", email_input) # Debugger
print("Problema detectado:", problema_input) # Debugger




# --------------------------------------- EXECUÇÃO ---------------------------------------
# Realiza todas as operações de bot num loop eterno (até o problema ser resolvido)

if __name__ == '__main__':  
    problema_input += ": "
    passagem=False
    cancelar=False

    slack_userinfo=fetch_info(email_input)
    send_firstmessage(slack_userinfo)
    print("Successo: Primeira mensagem enviada!")

    while True:
        commands(slack_userinfo['id'], status_input, problema_input,primarykey_input)
        status_input=select("status", "usuarios_report", "id_usuarios_report={}".format(primarykey_input))[0]['status']        
        
        if status_input.lower() =="resolvido" and passagem==False:
            passagem=True
            text_status = "Seu problema foi resolvido! Obrigado por contribuir com o SAM. Fui!"
            send_message(slack_userinfo['id'], text_status)
            print("Problema resolvido... Encerrando o script.") # Debugger
            break

        time.sleep(1)
        con.commit()