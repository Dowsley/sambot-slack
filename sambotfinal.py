# Olá! Este SCRIPT (sambotv2) é o componente principal do programa, responsável por executar o BOT enquanto está rodando.
# Ele foi dividido em algumas partes para facilitar seu entendimento e execução.
# Para o BOT funcionar, o SCRIPT precisa resgatar informações de um novo report no banco de dados MySQL...
# ...e é isso que o segundo script (database_connector) faz: Mantém uma constante detecção e só para quando um novo report entra.
# Assim que as informações do novo report são importadas, a execução é retomada e o BOT começa a funcionar.

# É importante deixar claro que esse conjunto de scripts foi feito de tal forma que possa ser reescrito, reestruturado, por vocês.
# O objetivo aqui é criar adaptabilidade às possíveis integrações no seu sistema, inclusive no GLPI.
# Qualquer dúvida sobre o código, pode me contatar em: jfcd@cesar.school


# --------------------------------------- IMPORT E CONEXÃO ---------------------------------------
import MySQLdb # Lib para conectar com o banco de dados MySQL
import time # Necessária para fazer delays no loop
from slackclient import SlackClient  # Lib principal para o bot funcionar
from dbsite_connector import db_userinfo # Variável que carrega os dados de usuario do novo request, executa segundo Script.

sc = SlackClient('xoxb-310770145379-665484575621-za7alq4MDso5erL0TDNPBuKM') # Conexão com o token de controle do BOT

con = MySQLdb.connect( # É aqui que se coloca as credenciais de conexão com o banco de dados de vocês, portanto que seja MySQL.
    host="sql223.main-hosting.eu",
    user="u980762916_form",
    password="Recife02",
    port = 3306,
    db="u980762916_form" 
    )
print(con)


c = con.cursor(MySQLdb.cursors.DictCursor) # Parametros do cursor estão definidos para retornar em forma de dicionário.




# --------------------------------------- FUNÇÕES ---------------------------------------
def select(fields, tables, where): # Seleciona e devolve determinadas informações da DB.
    global c
    query = "SELECT " + fields + " FROM " + tables
    query += " WHERE " + where
    c.execute(query)
    return c.fetchall()


def update(where): # Função que realiza update (mudança) de informações na DB.
    global c, con
    query = "UPDATE mensagens_contatos"
    query += " SET status = 'Cancelado'"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()


def delete(where): # Deleta um report de usuário. Não foi utilizado no código, mas talvez sirva para alterações futuras.
    global c, con
    query = "DELETE FROM mensagens_contatos"
    query += " WHERE id_usuarios_report = {}".format(where)
    c.execute(query)
    con.commit()


def fetch_info(email): # Busca as info. de um usuário no workspace de acordo com o e-mail de entrada
    user_info=sc.api_call(
            "users.lookupByEmail",
            email=email,
            )
    return user_info['user']


def send_message(userid, text): # Manda uma mensagem (como BOT) para o usuário
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

    texto = "Olá " + name + "! Seu report foi enviado com sucesso. Para receber mais feedback, utilize os seguintes comandos:\n\nSTATUS para ver o estado de resolução do seu problema.\nCANCELAR para anular o seu report.\n\nNão se preocupe com as letras maiúsculas ou acentos :)"
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
    

    if 'bot_id' not in conv_info['channel']['latest']:    
        ult_msg=conv_info['channel']['latest']['text']
        ult_msg=ult_msg.strip().upper()

        if ult_msg == 'STATUS':
            if "não resolvido" in status.strip().lower() or "nao resolvido" in status.strip().lower():
                text_status = problema + "Não resolvido. A equipe já foi mobilizada e você será notificado aqui quando o problema for solucionado."
            else:
                text_status = problema + status

            send_message(userid, text_status)
            print("Comando STATUS detectado.") # Debugger

        elif ult_msg=='HELP':
            text_status = "Os comandos disponíveis são:\n\nSTATUS para ver o estado de resolução do seu problema.\nCANCELAR para anular o seu report."
            send_message(userid, text_status)
            print("Comando HELP detectado") # Debugger

        elif ult_msg=='CANCELAR':
            global cancelar
            cancelar=True
            text_status = "Você tem certeza que quer cancelar seu report? Digite SIM para confirmar ou NÃO para anular esta ação."
            send_message(userid, text_status)
            print("Comando CANCELAR detectado") # Debugger

        elif ult_msg=='SIM' and cancelar==True:
            text_status = "Report cancelado com sucesso, você não receberá mais atualizações sobre o problema. Obrigado por contribuir com o SAM!"
            send_message(userid, text_status)
            update(primarykey)
            print("CONFIRMAÇÃO de CANCELAMENTO detectado") # Debugger

        elif (ult_msg=='NÃO' or ult_msg=='NAO') and cancelar==True:
            cancelar = False
            text_status = "Tudo bem, continuaremos o processo de resolução do problema."
            send_message(userid, text_status)
            print("ANULAÇÃO de CANCELAMENTO detectado") # Debugger

        else:
            text_status = "Comando não reconhecido. Talvez você queira digitar HELP para relembrar quais são os comandos disponíveis."
            send_message(userid, text_status)




# --------------------------------------- RESGATE E DEFINIÇÃO DE INFORMAÇÕES ---------------------------------------
# As informações do request (importadas no começo do script) são divididas em informações menores e definidas.

if db_userinfo['problema_reportado'] != None and db_userinfo['problema_reportado'] != '':
    problema_input = db_userinfo['problema_reportado']  # Problema reportado
    print("Problema botão!")

else:
    problema_input = db_userinfo['mensagem'] # Caso o problema tenha sido um preenchimento na área "Outros"
    print("Problema de Outros!")

email_input = db_userinfo['email_usuario'] # Email do usuário do Report
status_input = db_userinfo['status'] # Estado de resolução do problema
primarykey_input = db_userinfo['id_usuarios_report'] # Primarykey identificadora do report na tabela

print("Email detectado:", email_input) # Debugger
print("Problema detectado:", problema_input) # Debugger
print("Chave do usuário: {}".format(primarykey_input)) #Debugger




# --------------------------------------- EXECUÇÃO ---------------------------------------
# Inicia a execução e realiza todas as operações do bot através de um loop, que não para até o problema ser resolvido/cancelado.

if __name__ == '__main__':  
    problema_input += ": "
    passagem=False
    cancelar=False

    slack_userinfo=fetch_info(email_input)
    send_firstmessage(slack_userinfo)
    print("Successo: Primeira mensagem enviada!") # Debugger

    while True:
        commands(slack_userinfo['id'], status_input, problema_input,primarykey_input)
        status_input=select("status", "mensagens_contatos", "id_usuarios_report={}".format(primarykey_input))[0]['status']        
        
        if 'cancelado' in status_input.lower():
            print("Report cancelado... Encerrando Script.") # Debugger
            break


        if (status_input.lower()=='resolvido' or status_input.lower()=='resolvido.') and passagem==False:
            passagem=True
            text_status = "Seu problema foi resolvido! Você não receberá mais atualizações sobre o problema. Obrigado por contribuir com o SAM!"
            send_message(slack_userinfo['id'], text_status)
            print("Problema resolvido... Encerrando o script.") # Debugger
            break

        time.sleep(1) # Sleep de 1 segundo, essencial para manter-se na faixa do request rate-limit do Slack.
        con.commit()