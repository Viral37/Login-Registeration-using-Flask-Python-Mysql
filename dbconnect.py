import MySQLdb


def connectToDB():
    connection = MySQLdb.connect('localhost', 'root', 'root', 'student')
    cursor = connection.cursor()
    return connection, cursor
