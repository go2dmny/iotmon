#sqlite testing

import sys, os, configparser, bottle, sqlite3, datetime, socket
from fsmonitor import FSMonitor
from bottle import route, run

count = 1

config = configparser.ConfigParser()
config.read('settings.conf')
config.sections()
m = FSMonitor()                                                                                                                                                                                                      

for key in config['directories']:
	a = config['directories'][key]
	print(a)
	watch = m.add_dir_watch(a)

for key in config['files']:
	b = config['files'][key]
	print(b)
	watch = m.add_file_watch(b)

while True:
	usedb = sqlite3.connect('monitor.sqlite')
	cursor = usedb.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS events (Host TEXT, Date_Time TEXT, Event_Action TEXT, Event_Name TEXT, Event_Path TEXT )')
	for evt in m.read_events():
		time = str(datetime.datetime.now())
		host = socket.gethostname()
		cursor.execute("INSERT INTO events (Host, Date_Time, Event_Action, Event_Name, Event_Path) VALUES (?,?,?,?,?)",
		(host, time, evt.action_name, evt.name, evt.watch.path))
		usedb.commit()
		count += 1


