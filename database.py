from databaseClass import databaseClass

class database():
    dbcon=databaseClass()
    def __init__(self):
        return

    def insertdata(self):
        database.dbcon.insertOp('1', 100, "test", '00283744537')
        database.dbcon.insertOp('2', 23, 'second', '00477278767')
        database.dbcon.insertOp('3', 34, 'last', '00283598439')
        database.dbcon.insertOp('5', -20, 'down', '00787592758')
        database.dbcon.insertOp('8', -35, 'last', '00283594339')