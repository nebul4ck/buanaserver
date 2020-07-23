# -*- encoding: utf-8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Auto loader class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail:  a.gonzalezmesas@gmail.com
   :Web :
"""

from importlib import import_module

class AppLoader(object):
    """ Automatic class loader """

    def __init__(self, mod_path):
        super(AppLoader, self).__init__()
        self.mod_path = mod_path

    def get_instance(self, appName):
        """ Application name capitalize to import app class. Ej kafka =>\
        Kafka (class) """

        className = str(appName).capitalize().replace('-','')
        try:
            loadMod = import_module('{path}.{app}'.format(app=className, path=self.mod_path))
        except ImportError:
            import traceback
            traceback.print_exc()
            raise
        else:
            """ Class initiation """
            return getattr(loadMod, className)()
