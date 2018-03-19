#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Experiment Recording Tool
"""


import subprocess


def _is_under_git_control():
    """Check whether current directory is under git control."""
    ret = subprocess.run('git rev-parse'.split(),
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    return ret.returncode == 0


def _issue_command(command):
    """Issue specified command in subprocess and return output."""
    out = subprocess.check_output(command.split())
    return out.decode('utf-8')


def check_git_status():
    """Check git repository status."""
    if not _is_under_git_control():
        return None

    git_data = {
        'head': _issue_command('git rev-parse HEAD'),
        'branch': _issue_command('git branch'),
        'diff': _issue_command('git diff'),
        'status': _issue_command('git status'),
        'log': _issue_command('git log -n 30'),
    }
    return git_data
