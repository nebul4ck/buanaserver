#!/usr/bin/python
# Si cada app va a tener su propio entorno virtual:
##python_home = '/srv/4backup-env1/api'
##python_home = '/srv/4backup-env2/api'

##activate_this = python_home + '/bin/activate_this.py'
##execfile(activate_this, dict(__file__=activate_this))

# Ademas hay que crear un env vacio:
##WSGIDaemonProcess myapp python-home=/srv/4backup-env-empty/app

# Si solo hay un WSGI o se va a compartir el entorno virtual:

from bin.api import app as application

# Y anadir en el VirtualHost:
## WSGIDaemonProcess myapp python-home=/srv/4backup-env/apps

#if __name__ == "__main__":
#    application.run()
