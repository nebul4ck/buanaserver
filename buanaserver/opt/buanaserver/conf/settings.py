# -*- encoding: utf-8 -*-

#
# Global configs:

INFO = {'Api':'Backups & Deploy',
    'Desc':'This API creates backups from internal software\
    and deployed BigData IT Backend',
    'Version': '1.4.0',
    'Last Update': '24/04/2019',
    'Author': 'A. Gonzalez',
    'First Release': '13/10/2017'}

# Path, dirs and Files:
TOKEN = '64317f2bcaadfad364843036589fe0fcac6f85a1'
COMPANY = 'nebul4ck'
REMOTE_DEPLOY_USER = 'root'
USER_API_RUNNER = 'buanarepo'
UPDATE_CMD = 'apt update'
INSTALL_CMD = 'apt install -y'
LOGFILE = '/var/log/buanaserver/buanaserver.log'
MOD_PATH = 'lib.services'
CONF_PATH = 'conf'
MULTI_PACKAGE_PATH = 'deb_packages'
DEBS_BASE = '/srv/buanarepo-debs'
UBUNTU_BASE = '/srv/buanarepo-repo/ubuntu'
COMPONENTS = ['main', 'restricted']
CMD_LS = "ls -lt %s|grep %s|head -1|awk '{printf $NF}'"
CMD_REMOVE = "reprepro -Vb %s/%s -C %s remove xenial %s"
CMD_UPLOAD = "reprepro -Vb %s/%s -S utils -C %s includedeb xenial %s/%s"
URL_PKG = 'https://master.buanarepo-main.nebul4ck.es:8080/ubuntu/master/dists/xenial/main/binary-amd64/Packages'
CERT_P12 = '/etc/apache2/ssl/buanAPTclient-main.p12'
CA_CERT = '/etc/apache2/ssl/buanaCA.crt'
CERT_P12_PASS = 'cert-password'
API_USER = 'user'
USER_PASS = 'password'

users = {
    # The password is a md5sum. You must think a new password and create its md5sum.
    # In this case de plain text password is: password-
    "user": "a830e3204c7f8511e37ceceb91dfe1bf"
}
