import os
from slackclient import SlackClient
sc = SlackClient('xoxb-601279383251-616213772279-sffjqQxH5C6eh2zL26dhsUOI')

sc.api_call(
	"conversations.open",
	users='UJ2H2AR8X',
)


sc.api_call(
   "chat.postMessage",
	channel='UJ2H2AR8X',
	text="Olá! Sou o SAMBOT.",
)