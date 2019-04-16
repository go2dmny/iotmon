import sys, os, configparser, pymysql, datetime, socket
from fsmonitor import FSMonitor
from sshtunnel import SSHTunnelForwarder


config = configparser.ConfigParser()
config.read('settings.conf')
config.sections()

m = FSMonitor()

def dirs():
	for key in config['directories']:
		a = config['directories'][key]
		print(a)
		watch = m.add_dir_watch(a)

def files():	
	for key in config['files']:
		b = config['files'][key]
		print(b)
		watch = m.add_file_watch(b)

dirs()
files()

def poststuff(): 		
	server = SSHTunnelForwarder(
	('AWS INSTANCE URL', 22), ssh_private_key="keylocation.pem", ssh_username="ubuntu", ##Change ssh key location and user name
	remote_bind_address=('0.0.0.0', 3306))
	for evt in m.read_events():
		server.start()
		##Change database user name, password, and DB name
		conn = pymysql.connect(user='username',passwd='password',db='databasename',host='0.0.0.0',port=server.local_bind_port)
		time = str(datetime.datetime.now())
		host = socket.gethostname()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO events (Host, Date_Time, Event_Action, Event_Name, Event_Path) VALUES (%s,%s,%s,%s,%s)",
		(host, time, evt.action_name, evt.name, evt.watch.path))
		conn.commit()
		cursor.close()
		server.stop()


while True:
	poststuff()
