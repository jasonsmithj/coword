import multiprocessing

'''
Config file for gunicorn

Start command
gunicorn run:app -c guniconf.py -D
'''

# Server Socket
bind = 'tcp://0.0.0.0:3000'

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2
debug = False
spew = False

# Logging
accesslog = None
errorlog = '/var/www/coword/logs/gunicorn-error.log'
loglevel = 'info'
logconfig = None

# Process Name
proc_name = 'coword'

