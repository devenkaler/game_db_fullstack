import psycopg2
from psycopg2.extras import RealDictCursor
from config import load_config

def connect():
    config=load_config()
    
    #try connecting to DB
    try:
        with psycopg2.connect(**config) as conn:
            print('Successful connection to DB')
            return conn
        
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def connectDict():
    config=load_config()
    
    #try connecting to DB
    try:
        with psycopg2.connect(**config, cursor_factory=RealDictCursor) as conn:
            print('Successful connection to DB')
            return conn
        
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)