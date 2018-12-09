from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        msg = 'committing changes in /etc after ansible task run'
        result = self._low_level_execute_command('etckeeper commit "%s"' % msg)
        # In case of no changes the command will fail, but ignore that
        if (result['rc'] == 1) and ('nothing to commit, working tree clean' in result['stdout']):
            result['rc'] = 0
        return result
