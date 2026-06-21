import psycopg2
from psycopg2 import sql



class myDB :
  def __init__(self) -> None:
    self.config = {
      'host': 'localhost',   # или '127.0.0.1'
      'port': '5432',        # порт по умолчанию
      'user': 'postgres',    # ваше имя пользователя
      'password': 'staff',   # ваш пароль
      'dbname': 'postgres'   # подключаемся к системной БД, которая существует всегда
    }

    self.new_db_name = 'my_new_database'

    self.conn = None
  def _createDB(self) :
    try:
      self.conn = psycopg2.connect(**self.config)
      self.conn.autocommit = True
      
      cursor = self.conn.cursor()
      
      # Проверяем, существует ли уже база
      cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [self.new_db_name])
      if not cursor.fetchone():
          create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.new_db_name))
          cursor.execute(create_db_query)
    #       print(f"База данных '{self.new_db_name}' успешно создана!")
    #   else:
    #       print(f"База данных '{self.new_db_name}' уже существует")
      
      cursor.close()

    except psycopg2.Error as e:
        print(f"Произошла ошибка: {e}")
        if "password authentication failed" in str(e):
            print("Неверный пароль! Попробуйте сбросить пароль PostgreSQL командой:")
            print("sudo -u postgres psql -c \"ALTER USER postgres WITH PASSWORD 'новый_пароль';\"")
    finally:
        if self.conn:  
            self.conn.close()
            print("Соединение закрыто.")


  def insertUser(self , name:str , information:str) :
    
    self._createDB()
    
    conn = psycopg2.connect(
        **self.config
    )

    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            inf TEXT
        )
    """)

    
    cursor.execute("INSERT INTO users (name, inf) VALUES (%s, %s)", 
                  (name, information))

   
    conn.commit()

  def deleteDB(self) :
    conn = psycopg2.connect(
    **self.config
)

    cursor = conn.cursor()

    
    cursor.execute("DROP TABLE users;")

    
    conn.commit()

    print("Таблица удалена!")

    cursor.close()
    conn.close()

  @property
  def all_users(self) :
    
    conn = psycopg2.connect(
        **self.config
    )

    
    cursor = conn.cursor()
    


    try:
        # conn = psycopg2.connect(**self.config)
        # cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return [(1,"Empty" , "Empty")]
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
  @property
  def last_id(self)->int :
    
    conn = psycopg2.connect(
        **self.config
    )

    
    cursor = conn.cursor()
    


    try:
        # conn = psycopg2.connect(**self.config)
        # cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return int(cursor.fetchall()[-1][0])
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return 1
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
  
  def deleteUser(self , user_id:int) :
    conn = psycopg2.connect(
    **self.config
)

    cursor = conn.cursor()

    
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

    
    conn.commit()

    print("Пользователь удален!")

    cursor.close()
    conn.close()

if __name__ == "__main__" :
   db = myDB()
#    db.deleteUser(2)
   db.insertUser("Yuriy" , "+7952652")
   print(db.all_users)
