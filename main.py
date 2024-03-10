import psycopg
import jwt
import time
import sys
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SECRET_KEY")

def get_token(idpart: str) -> str:
      """ Generate token from id part """
      connection = psycopg.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASS"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT")
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
    
    parser = argparse.ArgumentParser(
         description="Script para gerar token jwt do participante"
    )

    parser.add_argument("--idpart", required=True, default=1, type=int, help="Enter o idpart: 8012")

    args = parser.parse_args()

    idpart = args.idpart

    print(get_token(idpart))