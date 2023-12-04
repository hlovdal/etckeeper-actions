
# Ansible etckeeper actions

## Introduction

[Ansible](http://ansible.com) is a tool to automate configuration and management of one or more hosts. [Etckeeper](https://etckeeper.branchable.com/) is a tool to put file changes under the `/etc` directory into version control.

This repository contrains Ansible actions so that when an Ansible task changes something
under the `/etc` directory, those changes are checked in into version control.

## Description

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

With the three actions `etckeeper-pre-task`, `etckeeper-commit-task`, and `etckeeper-post-task` you can
make sure that any changes in `/etc` triggered by an ansible task are commited.


## Example Playbook

Here is an example of how to capture changes made by the `user` module:

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

If there were uncommitted changes when the playbook started, those were checked in
with commit message `saving uncommitted changes in /etc prior to ansible task run`.

If the user were removed, that change would be checked in with a commit with message
`saving uncommitted changes in /etc prior to ansible task run`.

To set a custom message on a commit:
```yaml
---
- hosts: all
  gather_facts: no
  tasks:
    - etckeeper-commit-task:
      msg: Etckeeper commit in role_name taskfile before some_change
```


## Dependencies

Etckeeper must be installed and initialized. Notice however that if etckeeper is not
installed on a host, the actions does not fail so it is safe to add them to
a playbook even if not all hosts use etckeeper.

## Requirements

The actions need to be run as root.

## Installation

TBD

## Configuration

There is nothing to configure for the actions.

## Contributing

You are welcome to create pull requests if you think there is something that can be
improved.

### TODO list

* Figure out how to share code between the two files.

## FAQ

### Why not using `notify` and `handlers` instead of `actions`?

Because handler invocations are delayed to the end, multiple calls are joined and
reduced to one, and handlers might not be called under some circumstances.

### But I do not want to pepper my playbooks with calls to etckeeper actions around all tasks that can modify `/etc`.

You should and you have to. If you think that you rather would have one commit for
all changes made by a playbook, you are forgetting that any calls to `package`
[et al.](https://en.wiktionary.org/wiki/et_al.#English) will create individual
commits inbetween thus ruining that idea.

It is possible to achieve this idea if you first check out a new *playbook run* branch,
create commits on that one and then at the end do a non-fast-forward merge back to master.
But you still should create individual commit for individual changes,
which is good version control practice in any case.

Now if you really want to put in minium effort, it is possible to put just one call
to etckeeper-pre-task at the very beginning and one unconditional call to
etckeeper-post-task at the very end. That will work fine, just not giving
you the full granularity you could have had.

## Version

The latest version is 1.0.0. See the [changelog](./CHANGELOG.md) for details.

## Maintainers

Håkon Løvdal <kode@denkule.no>

## License

[GPL](LICENSE.txt) version 3 or (at your option) any later version. ([summary](https://tldrlegal.com/l/gpl-3.0))
