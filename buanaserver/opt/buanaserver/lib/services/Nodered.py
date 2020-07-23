# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Nodered main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import NODERED_REMOTE_CONFIG_FILE, NODERED_REMOTE_SYSTEMD_FILE,\
    NODERED_REMOTE_FLOW_FILE, NODERED_LOCAL_CONFIG_FILE, NODERED_LOCAL_SYSTEMD_FILE,\
    NODERED_LOCAL_FLOW_FILE

class Nodered(object):
    """Nodered-Backup main methods"""
    def __init__(self):
        super(Nodered, self).__init__()
        self.NoderedRemoteConfFiles = NODERED_REMOTE_CONFIG_FILE
        self.NoderedRemoteSystemdFile = NODERED_REMOTE_SYSTEMD_FILE
        self.NoderedRemoteFlowFile = NODERED_REMOTE_FLOW_FILE
        self.NoderedLocalConfFiles = NODERED_LOCAL_CONFIG_FILE
        self.NoderedLocalSystemdFile = NODERED_LOCAL_SYSTEMD_FILE
        self.NoderedLocalFlowFile = NODERED_LOCAL_FLOW_FILE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /opt/nodered/settings.js """
        confFile_stdout = self.action.rsync(Host, self.NoderedRemoteConfFiles, self.NoderedLocalConfFiles)

        """ Backup: /lib/systemd/system/nodered.service """
        systemd_stdout = self.action.rsync(Host, self.NoderedRemoteSystemdFile, self.NoderedLocalSystemdFile)

        """ Backup: /opt/nodered/flow/ """
        flow_stdout = self.action.rsync(Host, self.NoderedRemoteFlowFile, self.NoderedLocalFlowFile)

        logger = '{confFile_stdout}\n{systemd_stdout}\n{flow_stdout}'.format(
                confFile_stdout=confFile_stdout, systemd_stdout=systemd_stdout, flow_stdout=flow_stdout)

        return logger
