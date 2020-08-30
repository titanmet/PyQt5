from PyQt5 import QtSql

con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
con.setDatabaseName('data.sqlite')
con.open()
if 'good' not in con.tables():
    query = QtSql.QSqlQuery()
    query.exec("create table good(id integer primary key autoincrement, goodname text, goodcount integer) ")

query.prepare("insert into good values(null, ?, ?)")
query.addBindValue('Дискета')
query.addBindValue(10)
query.exec_()

query.prepare("insert into good values(null, ?, ?)")
query.bindValue(0, 'Дискета')
query.bindValue(1, 10)
query.exec_()

query.prepare("insert into good values(null, :name, :count)")
query.bindValue(':name', 'Дискета')
query.bindValue(':count', 10)
query.exec_()

query.prepare("insert into good values(null, :name, :count)")
lst1 = ['Дискета', 'Бумага для принтера', 'Барабан для принтера']
lst2 = [10, 3, 8]
query.bindValue(':name', lst1)
query.bindValue(':count', lst2)
query.execBatch()

query.prepare("select * from good order by goodname")
query.setForwardOnly(True)
query.exec_()
