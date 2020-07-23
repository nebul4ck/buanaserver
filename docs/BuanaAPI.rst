BuanaServer API
###############

To connect with the buanaserver repository and run commands (deploy, backups, git...) it will be necessary to install **BuanaServer API**. It accepts remote commands from *BuanaClient* and launch actions from buanaserver to buanaclient.

Install
*******

From Github
===========

.. code:: console

  $ cd ~
  $ git clone https://github.com/nebul4ck/buanaserver
  $ cd buanaserver
  $ dpkg -b buanaserver buanaserver-0.1.0_amd64.deb 
  $ sudo dpkg -i buanaserver-0.1.0_amd64.deb
  $ cd ~
  $ rm -rf buanaserver
..

From another Buanarepo Repository
=================================

1. Add repository

  https://wiki-nebul4ck-org.nebul4ck.es/doku.php?id=nebul4ck-org:general:buanarepo

2. Install from repo

.. code:: console

  $ sudo apt install buanaserver
..

Configure
*********

Buanarepo User SSH-KEY
======================

Buanarepo will needs some things to it runs safetly in remote mode:

* Buanaserver must resolv remote servers-clients (DNS or hosts file).
* Copy the buanarepo user account's PUB-KEY into remotes servers clients root account.
* To use buanarepo repository in servers/clients, you need create buanarepo.list into /etc/apt/source.list.d directory.

User root: for rsyncs with clients (PRE servers)
------------------------------------------------

**Create SSH-KEY:**

.. code:: console

  $ sudo su -
  # ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -C '' -N ''
..

**Copy the SSH-KEY into the remote clients/server to make backups:**

.. code:: console

  # ssh-copy-id root@remote-server
..

**Note:** maybe will be necessary to create a root user password and to configure ssh daemon into remote server to it accepts remote conexions with root user.

In remote server (client):

.. code:: console

  # vi /etc/ssh/sshd_config
  ...
  #PermitRootLogin prohibit-password
  PermitRootLogin yes
  ...

  # systemctl restart sshd
..

**Remember** to reconfigure remote sshd service


User buanarepo: deploying and provisioning
------------------------------------------

Generate a SSH-KEY and copy it into servers that you need orchestrate.

.. code:: console

  $ ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -C '' -N ''
  $ ssh-copy-id root@<server_to_orchestrate>
..

Config files
============

/opt/buanaserver/rsync/conf/exclude
-----------------------------------

Here, you can to exclude files and directories names that you don't want synchronize from remote servers.

ie:

.. code:: console

  store
  logs
  log
  version-2
  *pid
  run
  persistent
  tmp
  workers
  data
..

/opt/buanaserver/conf/backup_conf.py
------------------------------------

This file configure the directories and files to synchronize.

ie: 

.. code:: console

  ...
  """Root privileges are necessary on the remote hosts"""
  REMOTE_RSYNC_USER = 'root'
  RSYNC_CMD = 'sudo rsync -r -l -t -D -v -h -z --progress --partial-dir={partialdir}\
                --delete --exclude-from={excludefrom} {remoteuser}@{remotehost}:{remotedir}\
                {localdir}'

  """The Following directories and files are created during the API install"""
  EXCLUDE_FROM = '/opt/buanaserver/rsync/conf/exclude'
  PARTIAL_DIR = '/opt/buanaserver/rsync/partial'
  BASE_BUILD = '/srv/buanarepo-build'
  URL_GIT = 'git@github.com:nebul4ck'

  #
  #######################
  # BACKUP APP SETTINGS #
  #######################

  """ Kafka Settings """
  """Warning: the end slash ("/") is necessary"""
  KAFKA_REMOTE_APP_DIR = '/opt/kafka/'
  KAFKA_REMOTE_SYSTEMD_FILE = '/lib/systemd/system/kafka.service'
  KAFKA_REMOTE_BINS = '/usr/bin/kafka-*'
  KAFKA_REMOTE_LOGROTATE = '/etc/logrotate.d/kafka'
  KAFKA_LOCAL_LOGROTATE = '{base_build}/kafka/kafka/etc/logrotate.d/kafka'.format(\
          base_build=BASE_BUILD)
  KAFKA_LOCAL_APP_DIR = '{base_build}/kafka/kafka/opt/kafka'.format(\
          base_build=BASE_BUILD)
  KAFKA_LOCAL_SYSTEMD_FILE = '{base_build}/kafka/kafka/lib/systemd/system/'.format(\
          base_build=BASE_BUILD)
  KAFKA_LOCAL_BINS = '{base_build}/kafka/kafka/usr/bin/'.format(\
          base_build=BASE_BUILD)
  ...
..

/opt/buanaserver/lib/services/Kafka.py
--------------------------------------

Make a python class in order tu initialize the service backup:

.. code:: console

  # -*- encoding: utf 8 -*-

  """
  .. module:: main
     :platform: Unix/Linux
     :synopsis: Kafka main class.
  .. moduleauthor::
     :Nickname: Alberto González
     :mail: agonzalez@nebul4ck.es
     :Web :
  """

  from lib.utils.Actions import Actions
  from conf.backup_conf import KAFKA_REMOTE_APP_DIR, KAFKA_REMOTE_SYSTEMD_FILE, \
    KAFKA_LOCAL_APP_DIR, KAFKA_LOCAL_SYSTEMD_FILE, KAFKA_REMOTE_BINS, \
    KAFKA_LOCAL_BINS, KAFKA_REMOTE_LOGROTATE, KAFKA_LOCAL_LOGROTATE

  class Kafka(object):
    """Kafka-Backup main methods"""
    def __init__(self):
      super(Kafka, self).__init__()
      self.KafkaRemoteAppDir = KAFKA_REMOTE_APP_DIR
      self.KafkaRemoteSystemdFile = KAFKA_REMOTE_SYSTEMD_FILE
      self.KafkaRemoteBins = KAFKA_REMOTE_BINS
      self.KafkaRemoteLogRotate = KAFKA_REMOTE_LOGROTATE
      self.KafkaLocalAppDir = KAFKA_LOCAL_APP_DIR
      self.KafkaLocalSystemdFile = KAFKA_LOCAL_SYSTEMD_FILE
      self.KafkaLocalBins = KAFKA_LOCAL_BINS
      self.KafkaLocalLogRotate = KAFKA_LOCAL_LOGROTATE
      self.action = Actions()

    def backup(self, RemoteHost):
      Host = RemoteHost

      # TODO Check if exits app in host
      
      """ Backup: /opt/kafka """
      home_stdout = self.action.rsync(Host, self.KafkaRemoteAppDir, self.KafkaLocalAppDir)
      
      """ Backup: kafka.service """
      systemd_stdout = self.action.rsync(Host, self.KafkaRemoteSystemdFile, \
              self.KafkaLocalSystemdFile)
      """ Backup: /usr/bin/create-kafka-topics """
      create_topics_stdout = self.action.rsync(Host, self.KafkaRemoteBins, \
              self.KafkaLocalBins)

      """ Backup: /etc/logrotate.d/kafka """
      logrotate_stdout = self.action.rsync(Host, self.KafkaRemoteLogRotate, \
              self.KafkaLocalLogRotate) 

      logger = '{home_stdout}\n{systemd_stdout}\n{create_topics_stdout}\n{logrotate_stdout}'.format(
            home_stdout=home_stdout, logrotate_stdout=logrotate_stdout, \
            systemd_stdout=systemd_stdout,create_topics_stdout=create_topics_stdout)
      
      return logger
..

Now reload apache2:

.. code:: console

 systemctl reload apache2
..


Test BuanaServer
****************

Webbrowser
==========

Yo must import your client digital certificate to access Buanarepo repository from your favorite web browser.

How import User Digital Certificate into Web browser:

* Firefox: https://www.jscape.com/blog/firefox-client-certificate
* Chrome: https://support.google.com/chrome/a/answer/6080885?hl=en

Import trusted CA to verify connexions:

* Firefox: https://wiki.wmtransfer.com/projects/webmoney/wiki/Installing_root_certificate_in_Mozilla_Firefox
* Chrome: https://support.securly.com/hc/en-us/articles/206081828-How-to-manually-install-the-Securly-SSL-certificate-in-Chrome


Access to https://www.your-ip/

Test Buanarepo API: get/info
============================

Acces to http://your-ip:8081/get/info and fill the gaps in user box (user/pass) with the credentials set in */opt/buanarepo/conf/settings.py*

API use
*******

You must download `Buanarepo Client <https://github.com/nebul4ck/buanarepo-client>`_ to create .deb packages and add them to reprepro.

With BuanaClient you could make backups from remote servers, create packages from GitHub, deploy or provisionning servers.

API Endpoints
=============

* **info** [/get/info]: get info about buanarepo API. 
* **backup** [/make/backup]: make rsync from remote server to buanarepo server and build it in .deb package.
* **git** [/make/git]: clone git repository and build it in .deb package.
* **mpkg** [/make/mpkg]: Build package from Jenkins sources.
* **deploy** [/run/deploy]: App deployment and orchestration, all from one system.
* **list** [/get/listpkg]: List all available packages in repository.