Actions
=======

If you install a package with the
[package](https://docs.ansible.com/ansible/latest/modules/package_module.html) module
(or
[apt](https://docs.ansible.com/ansible/latest/modules/apt_module.html),
[yum](https://docs.ansible.com/ansible/latest/modules/yum_module.html)
or
[dnf](https://docs.ansible.com/ansible/latest/modules/dnf_module.html))
then
[etckeeper](https://etckeeper.branchable.com/)
will be automatically called and changes in `/etc` will be committed.
However changes caused by other modules like for instance
[lineinfile](https://docs.ansible.com/ansible/latest/modules/lineinfile_module.html)
or
[user](https://docs.ansible.com/ansible/latest/modules/user_module.html)
are not committed automatically.

With the two actions `etckeeper-pre-task` and `etckeeper-post-task` you can
make sure that any changes in `/etc` triggered by an ansible task are commited.

Requirements
------------

The actions need to be run as root.

Variables
---------

None.

Dependencies
------------

Etckeeper must be installed and initialized.

Example Playbook
----------------

Here is an example of how to capture changes made by `user` module with etckeeper:

```yaml
---
- hosts: all
  gather_facts: no
  tasks:
    - etckeeper-pre-task:

    - name: Remove user Darl McBribe
      user:
        name: dmcbribe
        state: absent
        remove: yes
      register: user_result

    - etckeeper-post-task:
      when: user_result.changed
```

License
-------

[GPL](gpl.txt) version 3 or (at your option) any later version. ([summary](https://tldrlegal.com/l/gpl-3.0))

Author Information
------------------

Håkon Løvdal <kode@denkule.no>
