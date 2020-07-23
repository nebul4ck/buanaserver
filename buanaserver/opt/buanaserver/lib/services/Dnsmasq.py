# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: DNSmasq main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import DNSMASQ_REMOTE_CONF_FILE, DNSMASQ_REMOTE_SYSTEMD_FILE, \
	DNSMASQ_LOCAL_CONF_FILE, DNSMASQ_LOCAL_SYSTEMD_FILE, DNSMASQ_REMOTE_LOGROTATE, \
	DNSMASQ_LOCAL_LOGROTATE

class Dnsmasq(object):
	"""Dnsmasq-Backup main methods"""
	def __init__(self):
		super(Dnsmasq, self).__init__()
		self.DnsmasqRemoteConfFile = DNSMASQ_REMOTE_CONF_FILE
		self.DnsmasqRemoteSystemdFile = DNSMASQ_REMOTE_SYSTEMD_FILE
		self.DmsmasqRemoteLogRotate = DNSMASQ_REMOTE_LOGROTATE
		self.DnsmasqLocalConfFile = DNSMASQ_LOCAL_CONF_FILE
		self.DnsmasqLocalSystemdFile = DNSMASQ_LOCAL_SYSTEMD_FILE
		self.DnsmasqLocalLogRotate = DNSMASQ_LOCAL_LOGROTATE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/dnsmasq.conf """
		confFile_stdout = self.action.rsync(Host, self.DnsmasqRemoteConfFile, self.DnsmasqLocalConfFile)

		#""" Backup: /etc/logrotate.d/dnsmasq """
		logrotate_stdout = self.action.rsync(Host, self.DmsmasqRemoteLogRotate, self.DnsmasqLocalLogRotate)

		""" Backup: /lib/systemd/system/dnsmasq.service """

		systemd_stdout = self.action.rsync(Host, self.DnsmasqRemoteSystemdFile, self.DnsmasqLocalSystemdFile)

		logger = '{confFile_stdout}\n{systemd_stdout}\n{logrotate_stdout}\n'.format(
				confFile_stdout=confFile_stdout,systemd_stdout=systemd_stdout,\
				logrotate_stdout=logrotate_stdout)

		return logger
