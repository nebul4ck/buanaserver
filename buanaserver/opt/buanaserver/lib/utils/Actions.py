# -*- encoding: utf-8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Actions for buanarepo API.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

import commands
import re
import os
import sys
import logging
import urllib2
import ssl

from paramiko import *
from multiprocessing import *
from requests_pkcs12 import get
from subprocess import PIPE, Popen, CalledProcessError
from flask import jsonify
from git import Repo, remote, GitCommandError,\
                InvalidGitRepositoryError, NoSuchPathError
from conf.backup_conf import REMOTE_RSYNC_USER, PARTIAL_DIR,\
                            EXCLUDE_FROM, BUANAREPO, BASE_BUILD, URL_GIT,\
                            RSYNC_CMD, BASE_JENKINS_BUILD
from conf.settings import TOKEN, COMPANY, REMOTE_DEPLOY_USER, UPDATE_CMD,\
                        INSTALL_CMD, USER_API_RUNNER, MULTI_PACKAGE_PATH,\
                        URL_PKG, MOD_PATH, DEBS_BASE, UBUNTU_BASE,\
                        COMPONENTS, CMD_LS, CMD_REMOVE, CMD_UPLOAD,\
                        CERT_P12, CERT_P12_PASS, CA_CERT, API_USER, USER_PASS
from lib.utils.AppLoader import AppLoader
from lib.utils.logger import logger as l

class Actions(object):

    """ Actions Class for Api tasks """

    def __init__(self):
        super(Actions, self).__init__()

    def create_msg(self, fir_val, sec_val, ctrl):

        if ctrl == 'host':
            host_service = 'Host'
            install_update = 'Update'
        elif ctrl == 'service':
            host_service = 'Service'
            install_update = 'Install'

        cmd_stdout = { install_update: sec_val, host_service: fir_val }

        return cmd_stdout

    def get_app_version(self, control_file):

        """ Get App version """

        f = open(control_file, 'r')
        matches = re.findall(r'Version: (.*)', f.read())
        version = matches[0]
        f.close()
        return version

    def get_app_name(self, control_file):

        """ Get App name """

        f = open(control_file, 'r')
        matches = re.findall(r'Package: (.*)', f.read())
        pkg_name = matches[0]
        f.close()

        return pkg_name

    def rsync(self, Host, RemoteDirOrFile, LocalDirOrFile):

        """ Synchronize remote and local directories. Create a local backup.
        For the rsync it is necessary to copy the RSA of buanarepo user on the
        root user at remote host and know the fqdn."""

        PartialDir = PARTIAL_DIR
        ExcludeFrom = EXCLUDE_FROM
        RemoteRsyncUser = REMOTE_RSYNC_USER
        RemoteHost = Host
        RemoteDir = RemoteDirOrFile
        LocalDir = LocalDirOrFile
        RsyncCommand = RSYNC_CMD

        rsync = RsyncCommand.format(partialdir=PartialDir,\
                                    excludefrom=ExcludeFrom,\
                                    remoteuser=RemoteRsyncUser,\
                                    remotehost=RemoteHost,\
                                    remotedir=RemoteDir, localdir=LocalDir)

        command_stdout = commands.getoutput(rsync)

        return command_stdout

    def dpkg(self, appName, appDpkgSource, appVersion, pkgName, command,\
            branch, language=None):

        """ This method calls a buanarepo shell script. This script is\
        installed by default into /usr/local/bin. Buanarepo runs two actions:\
        builds a .deb package from source dir and add it in Saturn Suit Repo
            appName: App name
            appDpkgSource: Relative path to the app's package source, from BASE_BUILD.
            appVersion: App version number
            pkgName: Output package name
        """

        command_stderr = ''
        command_stdout = ''

        if command == 'git' or command == 'mpkg':
            cmd = [BUANAREPO, appName, appDpkgSource, pkgName, command,\
                    '%s_%s'% (appName, appVersion), language, branch]
        elif command == 'backup':
            cmd = [BUANAREPO, appName, appDpkgSource, pkgName, command,\
                    '%s_%s' % (appName, appVersion)]

        try:
            l.info('Launching Buanarepo Package Build: %s' % BUANAREPO)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            command_stdout, command_stderr = p.communicate()
        except CalledProcessError as e:
            command_stderr = {
                'Error': True,
                'Stderr': str(e)
            }
        except OSError, e:
            l.exception(e)
            if e.errno == 13:
                command_stderr = {
                    'Error': True,
                    'Stdout': '%s: Permission denied' % BUANAREPO
                }
            else:
                command_stderr = {
                    'Error': True,
                    'Stdout': str(e)
                }

        stdout = {}

        if not command_stderr:

            if re.findall(r'Use', command_stdout):
                stdout = {
                    'Error': True,
                    'Stdout': command_stdout
                    }
            else:
                stdout = {
                    'Error': False,
                    'Stdout': command_stdout
                }

        else:

            if re.findall(r'Skipping', command_stderr):
                stdout = {
                    'Error': False,
                    'Stdout': '%s' % command_stderr
                }
            else:
                stdout = {
                    'Error': True,
                    'Stdout': command_stderr
                }

        return stdout

    def make_pkg(self, appName, branch, language, command='mpkg'):

        appName = str(appName).lower()
        local_repo = '%s/%s' % (BASE_JENKINS_BUILD, appName)
        msg_return = {'Stdout': '', 'Error': False}
        msg_exception = ''

        try:
            msg_return = self.build_pkg(appName, command, branch, language)
        except Exception as msg_exception:
            msg_return['Stdout'] = msg_exception
            msg_return['Error'] = True

        return msg_return

    def useSubprocess(self, cmd):

        msg_return = {'Stdout': '', 'Error': False}
        stdout = ''
        stderr = ''

        try:
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
        except Exception as e:
            l.error(e)
            msg_return['Stdout'] = e
            msg_return['Error'] = True

        if not stdout:
            msg_return['Stdout'] = stderr
            msg_return['Error'] = True
        else:
            msg_return['Stdout'] = stdout

        return msg_return

    def make_sync(self, appName, branch):

        msg_return = ''
        appName = str(appName).lower()

        cmd_ls = CMD_LS % (DEBS_BASE, appName)
        search_package = self.useSubprocess(cmd_ls)

        if not search_package['Error']:
            package =  search_package['Stdout']

            for component in COMPONENTS:
                    cmd_remove = CMD_REMOVE % (UBUNTU_BASE, branch, component,\
                                                appName)
                    remove_package = self.useSubprocess(cmd_remove)

                    if not remove_package['Error']:
                        cmd_upload = CMD_UPLOAD % (UBUNTU_BASE, branch,\
                                    component, DEBS_BASE, package)
                        l.info(remove_package['Stdout'])
                        upload_package = self.useSubprocess(cmd_upload)

                        if upload_package['Error']:
                            l.error(upload_package['Stdout'])
                            raise Exception(msg_return)
                        else:
                            msg_return += upload_package['Stdout']
                            l.info(upload_package['Stdout'])

                    else:
                        msg_return = remove_package['Stdout']
                        l.error(remove_package['Stdout'])
                        raise Exception(msg_return)

        else:
            msg_return = search_package['Stdout']
            l.error(search_package['Stdout'])
            raise Exception(msg_return)

        return msg_return

    def clone_from_git(self, appName, language):

        appName = str(appName).lower()
        path_local_repo = '%s/%s' % (BASE_BUILD, appName)
        remote_url = 'https://%s:x-oauth-basic@github.com/%s/'\
                    % (TOKEN, COMPANY)
        remote_repo = remote_url + appName

        msg_stdout = {
                'Stdout' : 'Error: %s isn\'t a valid local repository'\
                % path_local_repo, 'Error' : True
        }

        try:
            repo = Repo(path_local_repo)
            msg_stdout['Error'] = False
        except InvalidGitRepositoryError as e:
            l.error(msg_stdout['Stdout'])
            msg_stdout['Error'] = True
        except NoSuchPathError:
            try:
                l.info('Clonning %s repository' % remote_repo)
                msg_stdout['Stdout'] = Repo.clone_from(remote_repo,\
                                        path_local_repo, depth=1)
                msg_stdout['Error'] = False
            except GitCommandError as gitException:

                if re.findall(r'Repository not found.', gitException.stderr):
                    msg_stdout['Stdout'] = gitException.stderr
                    msg_stdout['Error'] = True
                    l.error(msg_stdout['Stdout'])

        else:
            l.info('Repository %s already exists, doing pull...' % path_local_repo)
            origin = repo.remote(name='origin')

            """ If in this point is present the next API error "list out of range", the problem is git control file"""
            try:
                msg_stdout['Stdout'] = origin.pull()
                msg_stdout['Error'] = False
                l.info(msg_stdout['Stdout'])
            except Exception as e:
                msg_stdout['Stdout'] = str(e)
                msg_stdout['Error'] = True
                l.error(msg_stdout['Stdout'])

        return msg_stdout

    def build_from_git(self, appName, branch, language, command, remotehost):

        ''' call clone_from_git and build package from source cloned '''

        msg_stdout_git = ''
        msg_build_pkg = ''

        msg_stdout = self.clone_from_git(appName, language)

        if not msg_stdout['Error']:

            if command == 'backup':
                appLoader = AppLoader(MOD_PATH)

                """ It's like 'from lib.Kafka import Kafka' and 'loadClass = Kafka()' """

                try:
                    l.info('Loading %s class for sync...' % appName)
                    loadClass = appLoader.get_instance(appName)
                except ImportError as e:
                    stderr = str(e)
                    msg_stdout['Stdout'] = 'Error: Application "%s" not found'\
                                            % appName
                    msg_stdout['Error'] = True
                    l.error(stderr)
                else:

                    try:
                        msg_stdout['Stdout'] = loadClass.backup(remotehost)
                        l.info(msg_stdout['Stdout'])
                    except Exception as e:
                        msg_exception = str(e)
                        l.error(msg_exception)
                        msg_stdout['Stdout'] = msg_exception
                        msg_stdout['Error'] = True

            else:

                try:
                    msg_build_pkg = self.build_pkg(appName, command, branch,language)
                    l.info(msg_build_pkg['Stdout'])
                    msg_stdout['Stdout'] = msg_build_pkg['Stdout']
                    msg_stdout['Error'] = msg_build_pkg['Error']
                except Exception as e:
                    msg_stdout['Stdout'] = str(e)
                    msg_stdout['Error'] = True

        return msg_stdout

    def git_push(self, appName, branch):

        ''' Commit the changes '''

        appName = str(appName).lower()
        path_local_repo = '%s/%s' % (BASE_BUILD, appName)
        remote_url = 'https://%s:x-oauth-basic@github.com/%s/' % (TOKEN, COMPANY)
        remote_repo = remote_url + appName
        msg_stdout = ''

        try:
            repo = Repo(path_local_repo)
        except InvalidGitRepositoryError as e:
            msg_stdout = str(e)
            l.error(msg_stdout)
        except NoSuchPathError as e:
            msg_stdout = str(e)
            l.error(msg_stdout)
        else:
            origin = repo.remote(name='origin')
            """ If in this point is present the next API error "list out of range", the problem is git control file"""
            try:
                l.info('Commit the new changes at %s' % path_local_repo)
                git = repo.git
                git.add ('.')
                repo.index.commit('New %s configuration' % appName)
                origin.push()
                msg_stdout = 'The %s latest version was pushed!' % appName
            except Exception as e:
                msg_stdout = str(e)
                l.error(msg_stdout)

        return msg_stdout

    def build_pkg(self, appName, command, branch, language=None):

        """ Builds packages from local dirs or git repositories. """

        multiPackagePath = MULTI_PACKAGE_PATH
        path_local_repo = '%s/%s' % (BASE_BUILD, appName)
        local_jenkins_repo = '%s/%s' % (BASE_JENKINS_BUILD, appName)
        appName = str(appName).lower()
        msg_return = {'Stdout': '', 'Error': False}
        msg_exception = ''

        if command == 'git':
            base_path = '%s/%s' % (path_local_repo, appName)
            appDpkgSource = '%s/%s' % (appName, appName)
            # If multi-package folder exists, then process sub-packages in it:
            sub_package_path = '%s/%s' % (path_local_repo, multiPackagePath)
        elif command == 'mpkg':
            base_path = '%s/%s' % (local_jenkins_repo, appName)
            appDpkgSource = '%s/%s' % (appName, appName)
            sub_package_path = '%s/%s' % (local_jenkins_repo, multiPackagePath)
        elif command == 'backup':
            base_path = '%s' % (path_local_repo)
            appDpkgSource = appName

        l.info('Checks multi-package path: %s' % sub_package_path)
        if os.path.isdir(sub_package_path):
            l.info('Running multi-package case...')

            try:
                appBaseSource = '%s/%s' % (appName, multiPackagePath)
                msg_return = self.build_several_pkgs(sub_package_path,\
                                appBaseSource, command, branch, language)
                if msg_return['Error']:
                    l.error(msg_return['Stdout'])
                else:
                    l.info(msg_return['Stdout'])
            except Exception as msg_exception:
                l.error(msg_exception)
                msg_return['Stdout'] = str(msg_exception)
                msg_return['Error'] = True

        else:
            l.info('No multi-package case detected.')
            l.info('Building %s...' % appName)

            # Single package case
            try:
                control_file = '%s/DEBIAN/control' % base_path
                appVersion = self.get_app_version(control_file)
                pkgName = self.get_app_name(control_file)
                msg_return = self.dpkg(appName, appDpkgSource, appVersion,\
                                pkgName, command, branch, language)

                if msg_return['Error']:
                    l.error(msg_return['Stdout'])
                else:
                    l.info(msg_return['Stdout'])

            except Exception as msg_exception:
                l.error(msg_exception)
                msg_return['Stdout'] = str(msg_exception)
                msg_return['Error'] = True

        return msg_return

    def build_several_pkgs(self, base_path, appBaseSource, command, branch, language=None):

        """ Run dpkg function multiple times, once for each sub-folder under the base_path folder."""

        multi_dpkg_out = {
            'Error': False,
            'Stdout': ''
        }
        sub_packages = next(os.walk(base_path))[1]

        for appName in sub_packages:
            subAppSource = '%s/%s' % (appBaseSource, appName)
            sub_base_path = '%s/%s' % (base_path, appName)
            control_file = '%s/DEBIAN/control' % sub_base_path

            if os.path.exists(control_file):
                appVersion = self.get_app_version(control_file)
                pkgName = self.get_app_name(control_file)
                l.info('Building %s sub-package...' % pkgName)

                dpkg_stdout = self.dpkg(appName, subAppSource, appVersion, pkgName, command, branch, language)
                multi_dpkg_out['Error'] = multi_dpkg_out['Error'] or dpkg_stdout['Error']
                multi_dpkg_out['Stdout'] += dpkg_stdout['Stdout']

        return multi_dpkg_out

    def orchestrator(self, host, services, l_msg):

        RemoteDeployUser = REMOTE_DEPLOY_USER
        UpdateCommand = UPDATE_CMD
        InstallCommand = INSTALL_CMD
        msg_action = []
        proc = os.getpid()

        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, username=RemoteDeployUser, timeout=30.0)
            upd_cmd = UpdateCommand
            stdin, stdout, stderr = client.exec_command(upd_cmd)
        except SSHException as error:
            cmd_stdout = self.create_msg(host, error[0], 'host')
            l.error(cmd_stdout)
            msg_action.append(cmd_stdout)
        except AuthenticationException as error:
            cmd_stdout = self.create_msg(host, error[0], 'host')
            l.error(cmd_stdout)
            msg_action.append(cmd_stdout)
        except BadHostKeyException as error:
            cmd_stdout = self.create_msg(host, error[0], 'host')
            l.error(cmd_stdout)
            msg_action.append(cmd_stdout)
        except Exception as error:
            cmd_stdout = self.create_msg(host, 'Destination Host Unreachable',\
                                        'host')
            l.error(cmd_stdout)
            msg_action.append(cmd_stdout)
        else:

            for service in services:
                ins_cmd = '%s %s' % (InstallCommand, service)
                l.info(ins_cmd)

                try:
                    stdin, stdout, stderr = client.exec_command(ins_cmd)
                    exit_status = stdout.channel.recv_exit_status()

                    if exit_status == 0:

                        cmd_stdout = self.create_msg(service, 'ok', 'service')
                        l.info(cmd_stdout)
                        msg_action.append(cmd_stdout)
                    else:
                        cmd_stdout = self.create_msg(service, 'error', 'service')
                        l.error(cmd_stdout)
                        msg_action.append(cmd_stdout)

                except SSHException as error:
                    cmd_stdout = self.create_msg(service, error[0], 'service')
                    l.error(cmd_stdout)
                    msg_action.append(cmd_stdout)

            """When the command finishes executing, the channel will be closed and can’t be reused. You must open a new channel if you wish to execute another command."""

            client.close()
            msg_action = {'Host': host, 'Install': msg_action}

        l_msg.append(msg_action)

    def build_deploy_command(self, deploy_data):

        """ Builds command to provisioning remotes servers from deploy_data """

        jobs = []
        msg_action = []
        manager = Manager()
        l_msg = manager.list()

        for host, services in deploy_data.iteritems():
            p = Process(name='orchestration-host', target=self.orchestrator,\
                        args=(host, services, l_msg))
            jobs.append(p)
            p.start()

            for proc in jobs:
                proc.join()

        return l_msg

    def listPackage(self):

        l_packages = []
        pkg_file = None
        basic_auth = (API_USER, USER_PASS)

        try:
            request = get(URL_PKG, pkcs12_filename=CERT_P12, pkcs12_password=CERT_P12_PASS,\
                        verify=CA_CERT, auth=basic_auth)
            #request = urllib2.Request(URL_PKG)
            #response = urllib2.urlopen(request, context=ssl._create_unverified_context())
            pkg_file = request.text
        except Exception as e:
            l.error(e)
            result_packages = e

        if not pkg_file:
            l_packages = result_packages
        else:
            result_packages = re.findall('Package.*', pkg_file)

            for package in result_packages:
                pkg = package.split()
                l_packages.append(pkg[1])

        return l_packages
