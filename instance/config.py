SECRET_KEY = 'test' #Puede ser cualquier valor aleatorio
#database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:rootroot@rooms.chm8fehlinww.us-east-1.rds.amazonaws.com:3306/innodb'

#Email server configuration
MAIL_SERVER = 'smtp.gmail.com' # Se debe cambiar por el smtp usado, en este caso es el de Gmail
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'productos@ideaslab.com.co' # Direccion con que se envian los correos
MAIL_PASSWORD = 'productos2012*' # Contrasena del correo usado
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_RECYCLE = 60

#branch qa
