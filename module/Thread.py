import os
import time
import json
import queue
import threading

# customized module
from . import Dcard

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/data/'

# global
q = queue.Queue()

def dump(obj):
	try:
		with open(PATH + '%s/%d.json' % (obj.forumAlias, obj.id), 'w+') as file:
			json.dump(obj.__dict__, file)
	except Exception as e:
		print('[%10s] %s' % ('dump', str(e)))

def next(var):
	while q.qsize() > 0:
		# init
		obj = q.get()

		_max = max(obj.id)
		obj.content = Dcard.get_content(obj.id)
		obj.comments = Dcard.get_comments(obj.id)

		dump(obj)

		if var['debug']:
			print('[%10s] %s %d' % ('crawling', obj.forumAlias, obj.id))



def run(var):
	# init
	threads = []
	for i in range(0, var['threads_num']):
		t = threading.Thread(name='T' + str(i), target=next, args=(var, ))
		threads.append(t)

	# run
	for i in range(0, len(threads)):
		threads[i].start()

	# wait until finish
	while any(thread.is_alive() for thread in threads):
		time.sleep(1)