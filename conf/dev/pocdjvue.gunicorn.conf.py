from multiprocessing import cpu_count

# Process Naming
proc_name = 'pocdjvue'

# Server Socket
bind = "unix:/home/ubuntu/poc/pocdjvue.sock"  # Este tipo de sockets es más rápido que
# utilizando la interfaz local. Por lo que si el Nginx y el Gunicorn están en
# el mismo servidor es el que les recomiendo.

# Worker Processes
workers = cpu_count() * 2 + 1  # Valor recomendado por la doc oficial.
# worker_class = 'gevent'  # Le decimos que utilice gevent para un mejor rendimiento.
worker_class = 'sync'
timeout = 90

# Security
limit_request_line = 8192

# Server Mechanics
pidfile = '/home/ubuntu/poc/pocdjvue.pid'
user = 'ubuntu'
group = 'ubuntu'

# Logging
loglevel = 'error'
accesslog = '/home/ubuntu/poc/log/gunicorn.access.log'
errorlog = '/home/ubuntu/poc/log/gunicorn.error.log'
