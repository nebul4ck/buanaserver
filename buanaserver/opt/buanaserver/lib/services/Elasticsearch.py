# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Elasticsearch main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import ELASTICSEARCH_REMOTE_CONF_FILES, ELASTICSEARCH_REMOTE_DEFAULT_FILE, \
	ELASTICSEARCH_REMOTE_SYSTEMD_FILE, ELASTICSEARCH_LOCAL_CONF_FILES, ELASTICSEARCH_LOCAL_SYSTEMD_FILE, \
	ELASTICSEARCH_LOCAL_DEFAULT_FILE, ELASTICSEARCH_REMOTE_LOGROTATE_FILE, ELASTICSEARCH_LOCAL_LOGROTATE_FILE, \
	ELASTICSEARCH_REMOTE_SHARE, ELASTICSEARCH_LOCAL_SHARE

class Elasticsearch(object):
	"""Elasticsearch-Backup main methods"""
	def __init__(self):
		super(Elasticsearch, self).__init__()
		self.ElasticsearchRemoteConfFiles = ELASTICSEARCH_REMOTE_CONF_FILES
		self.ElasticsearchRemoteDefaultFile = ELASTICSEARCH_REMOTE_DEFAULT_FILE
		self.ElasticsearchRemoteLogrotateFile = ELASTICSEARCH_REMOTE_LOGROTATE_FILE
		self.ElasticsearchRemoteSystemdFile = ELASTICSEARCH_REMOTE_SYSTEMD_FILE
		self.ElasticsearchRemoteShareFiles = ELASTICSEARCH_REMOTE_SHARE
		self.ElasticsearchLocalConfFiles = ELASTICSEARCH_LOCAL_CONF_FILES
		self.ElasticsearchLocalSystemdFile = ELASTICSEARCH_LOCAL_SYSTEMD_FILE
		self.ElasticsearchLocalDefaultFile = ELASTICSEARCH_LOCAL_DEFAULT_FILE
		self.ElasticsearchLocalLogrotateFile = ELASTICSEARCH_LOCAL_LOGROTATE_FILE
		self.ElasticsearchLocalShareFiles = ELASTICSEARCH_LOCAL_SHARE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/elasticsearch/ """
		confFile_stdout = self.action.rsync(Host, self.ElasticsearchRemoteConfFiles, self.ElasticsearchLocalConfFiles)

		""" Backup: /etc/default/elasticsearch """
		defaultFile_stdout = self.action.rsync(Host, self.ElasticsearchRemoteDefaultFile, self.ElasticsearchLocalDefaultFile)

		""" Backup: /etc/logrotate.d/elasticsearch """
		logrotateFile_stdout = self.action.rsync(Host, self.ElasticsearchRemoteLogrotateFile, self.ElasticsearchLocalLogrotateFile)

		""" Backup: /usr/lib/systemd/system/elasticsearch.service """

		systemd_stdout = self.action.rsync(Host, self.ElasticsearchRemoteSystemdFile, self.ElasticsearchLocalSystemdFile)

		""" Backup: /usr/share/elasticsearch """
		share_stdout = self.action.rsync(Host, self.ElasticsearchRemoteShareFiles, self.ElasticsearchLocalShareFiles)

		logger = '{confFile_stdout}\n{defaultFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n{share_stdout}\n'.format(
				confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
				defaultFile_stdout=defaultFile_stdout,systemd_stdout=systemd_stdout,share_stdout=share_stdout)

		return logger
