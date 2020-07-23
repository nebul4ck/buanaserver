# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Redis main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import REDIS_REMOTE_CONF_FILE, REDIS_REMOTE_DEFAULT_FILE, \
	REDIS_REMOTE_SYSTEMD_FILE, REDIS_LOCAL_CONF_FILE, REDIS_LOCAL_SYSTEMD_FILE, \
	REDIS_LOCAL_DEFAULT_FILE, REDIS_REMOTE_LOGROTATE_FILE, REDIS_LOCAL_LOGROTATE_FILE

class Redis(object):
	"""Redis-Backup main methods"""
	def __init__(self):
		super(Redis, self).__init__()
		self.RedisRemoteConfFile = REDIS_REMOTE_CONF_FILE
		self.RedisRemoteLogrotateFile = REDIS_REMOTE_LOGROTATE_FILE
		self.RedisRemoteDefaultFile = REDIS_REMOTE_DEFAULT_FILE
		self.RedisRemoteSystemdFile = REDIS_REMOTE_SYSTEMD_FILE
		self.RedisLocalConfFile = REDIS_LOCAL_CONF_FILE
		self.RedisLocalSystemdFile = REDIS_LOCAL_SYSTEMD_FILE
		self.RedisLocalDefaultFile = REDIS_LOCAL_DEFAULT_FILE
		self.RedisLocalLogrotateFile = REDIS_LOCAL_LOGROTATE_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/redis/redis.conf """
		confFile_stdout = self.action.rsync(Host, self.RedisRemoteConfFile, self.RedisLocalConfFile)

		""" Backup: /etc/logrotate.d/redis-server """
		logrotateFile_stdout = self.action.rsync(Host, self.RedisRemoteLogrotateFile, self.RedisLocalLogrotateFile)

		""" Backup: /etc/default/redis-server """
		defaultFile_stdout = self.action.rsync(Host, self.RedisRemoteDefaultFile, self.RedisLocalDefaultFile)

		""" Backup: /lib/systemd/system/redis-server.service """

		systemd_stdout = self.action.rsync(Host, self.RedisRemoteSystemdFile, \
						self.RedisLocalSystemdFile)

		logger = '{confFile_stdout}\n{logrotateFile_stdout}\n{defaultFile_stdout}\n{systemd_stdout}\n'.format(
				confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
				defaultFile_stdout=defaultFile_stdout,systemd_stdout=systemd_stdout)

		return logger
