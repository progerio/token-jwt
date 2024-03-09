import psycopg
import jwt
import time
import sys

key = 'e072b6332e650e041d8114e48af3caca60e07ed8ade231cc21b14b9f62966d27'

def get_token(idpart: str) -> str:
      """ Generate token from id part """
      connection = psycopg.connect(
                dbname="postgres",
                user="dev",
                password="123456",
                host="localhost",
                port="5432"
        )
        
      cursor = connection.cursor()
      
      cursor.execute("""
                     SELECT concat(id_part, ':', id_usu)
                     FROM public.usuarios
                     WHERE id_part = %s
                     AND administrador='1'
                     AND ativo='1' """, [idpart], binary=True)

      iss = cursor.fetchone()[0]
              
      payload = {
                'iss': iss,
                'aud': 1,
                'iat': time.time(),
                'exp': 1893466800
      }  

      cursor.close()

      encoded_data = jwt.encode(payload=payload,
                              key=key,
                              algorithm="HS256") 
      
      return encoded_data          


if __name__ == "__main__":
     idpart = sys.argv[1]
     
     print(get_token(idpart))       
