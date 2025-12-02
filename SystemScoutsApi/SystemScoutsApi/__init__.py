import pymysql

pymysql.install_as_MySQLdb()

# Monkey patch version to satisfy Django's requirement for mysqlclient >= 1.4.3
import MySQLdb
MySQLdb.version_info = (1, 4, 6, 'final', 0)

