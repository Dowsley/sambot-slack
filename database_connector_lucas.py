import MySQLdb

con = MySQLdb.connect(
	host="sql223.main-hosting.eu",
	user="u980762916_form",
	password="Recife02",
	port = 3306,
	db="u980762916_form"
	)
print(con)