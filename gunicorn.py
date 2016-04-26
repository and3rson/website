# bind = 'unix:/var/sock/app_kappaweb.sock'
# pidfile = '/var/sock/app_kappaweb.pid'
# chdir = '/var/apps/kappaweb'
# proc_name = 'kappaweb'
# user = 'http'
# group = 'http'
workers = 1

accesslog = '/var/apps/dunai/log/access.log'
errorlog = '/var/apps/dunai/log/error.log'

worker_class = 'gevent'
