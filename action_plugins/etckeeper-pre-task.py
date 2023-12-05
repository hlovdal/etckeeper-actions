#!/usr/bin/python

# Copyright: (c) 2018, Håkon Løvdal <kode@denkule.no>
# GNU General Public License v3.0+ (see gpl.txt, https://tldrlegal.com/l/gpl-3.0 or https://www.gnu.org/licenses/gpl-3.0.txt)

# TODO: Find a way to share this between the files. Failed attempts:
#from lib_etckeeper import run_etckeeper   # ERROR! Unexpected Exception, this is probably a bug: No module named 'lib_etckeeper'
#from .lib_etckeeper import run_etckeeper  # ERROR! Unexpected Exception, this is probably a bug: No module named 'ansible.plugins.action.lib_etckeeper'
#from . import lib_etckeeper               # ERROR! Unexpected Exception, this is probably a bug: cannot import name 'lib_etckeeper' from 'ansible.plugins.action' (/usr/lib/python3.7/site-packages/ansible/plugins/action/__init__.py)

import os

def run_etckeeper(self, msg):
    # Make sure we are not parsing localized text
    os.environ["LC_ALL"] = "C"

    result = self._low_level_execute_command('etckeeper commit "%s"' % msg)

    # In case of no changes the command will fail, but ignore that
    if (result['rc'] == 1) and ('nothing to commit' in result['stdout']):
        result['rc'] = 0

    # If etckeeper is not installed, do not treat that as an error.
    # Return code 127 is established behaviour for command not found. http://www.tldp.org/LDP/abs/html/exitcodes.html, https://stackoverflow.com/q/1763156/23118
    if (result['rc'] == 127) and ('command not found' in result['stdout']):
        result['rc'] = 0

    return result


from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        msg = 'saving uncommitted changes in /etc prior to ansible task run'
        result = run_etckeeper(self, msg)
        return result
