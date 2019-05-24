import bs4 as bs
import urllib.request
from subprocess import call

source = urllib.request.urlopen("http://pingteste.ga/SITE%20CERTO%20-%20Banco02/")
soup = bs.BeautifulSoup(source, "lxml")

# Enfiar um while aqui, pq isso tem q rodar ativamente até detectar entrada de user
list_parsed = []
for paragraph in soup.find_all("h2"):
	list_parsed.append(paragraph.text)

list_parsed[0] = list_parsed[0].replace("E-mail:","").strip()
list_parsed[1] = list_parsed[1].replace("Mensagem:","").strip()

email_request = list_parsed[0]
problema_request = list_parsed[1]