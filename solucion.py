'''
Leer todos los archivos json y validar que el archivo debe de comenzar con "informacion" esta prueba sera evaluada colocando su codigo con mas archivos json entonces su codigo debera leer solo aquellos que comiencen con "informacion", debera de crear tablas hagalo a su conveniencia , esta parte de la creacion de tablas tambien tendra su respectiva calificacion. Debe de usar psycopg2 para conectarse a la base de datos . 
'''
from os import getcwd, scandir
import pymysql, json
from json import load

class NewDBConnection:
  def __init__(self, route):
    # connection configurations
    self.conn = pymysql.connect(
      host = route['host'],
      user = route['user'],
      password = route['password'],
      database = route['DB']
    )
    self.conn.autocommit = True
    # init methods
    self.CheckTables()
  
  def CheckTables(self):
    queries = [
      '''
      create table if not exists cities(
        id serial,
        city varchar(80) not null,
        primary key (id)
      )
      ''',
      '''
      create table if not exists universities(
        id serial,
        university varchar(80) not null,
        primary key (id)
      )
      ''',
      '''
      create table if not exists users(
	      id serial,
        username varchar(100),
        identification varchar(100),
        city_id int,
        email varchar(100),
        gender varchar(6),
        university_id int,
        primary key (id),
        unique (identification),
        constraint city_name foreign key (city_id) references cities(id),
        constraint university_name foreign key (university_id) references univercities(id)
      )
      '''
    ]

    for q in queries:
      cursor = self.conn.cursor()
      cursor.execute(q)

class JSONfiles:
  def __init__(self):
    self.folder = getcwd()
    self.GetJSON()
  
  def GetJSON(self):
    self.files = list(
      filter(
        lambda x: x[:len('informacion')] == 'informacion' and x.split('.')[1] == 'json',
        [x.name for x in scandir(self.folder)]
      )
    )
  
  def GetData(self):
    reg = list()
    for f in self.files:
      with open(f, encoding = 'utf-8') as doc:
        reg += json.load(doc)
        doc.close()

    return reg


if __name__ == '__main__':
  json_data = JSONfiles()

  database = NewDBConnection({
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'DB': 'interview_exam'
  })