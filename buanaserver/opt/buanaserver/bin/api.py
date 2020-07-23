# -*- encoding: utf-8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Saturn Repo Suit API. Build and add .deb package to a central repository.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: agonzalez@nebul4ck.es
   :Web :
"""

import commands, logging
import md5

from importlib import import_module
from flask import Flask, request, json, jsonify
from flask_httpauth import HTTPBasicAuth

from conf.settings import INFO, MOD_PATH, users
from lib.utils.Actions import Actions
from lib.utils.logger import logger as l

action = Actions()
app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(request_username, request_password):
	access = ''

	if request_username in users:
		m = md5.new()
		m.update(request_password)
		md5_pass = m.hexdigest()
		if md5_pass == users.get(request_username):
			l.info('User/Passwd Authentication is OK!')
			access = True
		else:
			l.error('Wrong User or Password. Please edit password and try again.')
			access = False
	else:
		l.error('User not found!')

	return access

@app.route('/get/info', methods=['GET'])
@auth.login_required
def show_info():
	return jsonify(INFO)

@app.route('/make/backup', methods=['POST'])
@auth.login_required
def run_backup():
	""" git clone/pull + rsync + git commit/push. Since Jenkins integration ,
		this command doesn't up the .deb into reprepro. Jenkins will do this."""

	params = request.json
	remotehost = params['host']
	appName = params['app']
	branch = 'master'
	language = 'none'
	command = 'backup'
	msg_stdout = ''
	msg_return = ''
	msg_git_push = ''

	''' Clone/pull from git + Rsync '''
	msg_stdout = action.build_from_git(appName, branch, language, command, remotehost)
	l.info(msg_stdout['Stdout'])

	''' Add new changes, commit and push '''
	if not msg_stdout['Error']:
		msg_git_push = action.git_push(appName, branch)
		concatenate_git_output = '\n\n %s' % msg_git_push
		msg_stdout['Stdout'] += concatenate_git_output

	''' Jenkins will make the new package from source '''
	if msg_stdout['Stdout']:
		msg_return = msg_stdout['Stdout']
	else:
		msg_return = 'Unknown error: please contact with Buanarepo Admin or take a look to Buanarepo-Server logs.'
		l.error(msg_return)

	return msg_return

@app.route('/make/git', methods=['POST'])
@auth.login_required
def run_git():
	""" If a git repository doesn't exists into buanarepo's build path (ej.
	/srv/buanarepo-build), This repository will be cloned. Later, a new .deb pkg will be created """
	params = request.json
	appName = params['app']
	branch = params['branch']
	language = params['language']
	command = 'git'
	msg_return = ''
	msg_stdout = ''

	# Clone or pull Git repository
	msg_stdout = action.build_from_git(appName, branch, language, command, remotehost=None)

	if msg_stdout['Stdout']:
		msg_return = msg_stdout['Stdout']
	else:
		msg_return = 'Unknown error: please contact with Buanarepo Admin or take a look to Buanarepo-Server logs.'
		l.error(msg_return)

	return msg_return

@app.route('/make/mpkg', methods=['POST'])
@auth.login_required
def run_mpkg():
	""" Create package from source whitout pull/clon the code."""
	params = request.json
	appName = params['app']
	branch = params['branch']
	language = params['language']
	default_command = 'mpkg'
	msg_return = {}

	# Make the package
	msg_return = action.make_pkg(appName, branch, language)

	if msg_return['Stdout']:
		msg_return = msg_return['Stdout']
	else:
		msg_return = 'Unknown error: please contact with Buanarepo Admin or take a look to Buanarepo-Server logs.'
		l.error(msg_return)

	return msg_return

@app.route('/make/sync', methods=['POST'])
@auth.login_required
def run_sync():
	""" Create package from source whitout pull/clon the code."""
	params = request.json
	appName = params['app']
	branch = params['branch']
	msg_return = ''

	# Sync repositories
	msg_return = action.make_sync(appName, branch)

	return msg_return

@app.route('/run/deploy', methods=['POST'])
@auth.login_required
def run_deploy():
	""" Runs servers automated provisioning. """
	params = request.json
	hosts = action.build_deploy_command(params)

	return str(hosts)

@app.route('/get/listpkg', methods=['GET'])
@auth.login_required
def pkgList():
	pkglist = action.listPackage()

	return str(pkglist)

if __name__ == '__main__':
	app.run()
