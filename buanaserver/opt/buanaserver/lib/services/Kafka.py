# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Kafka main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
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
