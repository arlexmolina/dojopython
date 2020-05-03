SECRET_KEY = 'test' #Puede ser cualquier valor aleatorio
#database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:rootroot@rooms.chm8fehlinww.us-east-1.rds.amazonaws.com:3306/innodb'

#Email server configuration atributos
MAIL_SERVER = 'smtp.gmail.com' # Se debe cambiar por el smtp usado, en este caso es el de Gmail
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'materiapps@gmail.com' # Direccion con que se envian los correos
MAIL_PASSWORD = 'Hola1234' # Contrasena del correo usado
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_RECYCLE = 60

