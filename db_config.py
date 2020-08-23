from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'AngelGarrido'
app.config['MYSQL_DATABASE_PASSWORD'] = '1342.Adfs'
app.config['MYSQL_DATABASE_DB'] = 'db_biblioteca'
app.config['MYSQL_DATABASE_HOST'] = 'AngelGarrido.mysql.pythonanywhere-services.com'
mysql.init_app(app)
