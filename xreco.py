#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Experiment Recording Tool
"""


import argparse
import datetime
import os
import json
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


class ArgumentParser(argparse.ArgumentParser):
    """Extended argument parser that records some experiment info."""

    def __init__(self, name=None, output_root='./experiments',
                 output_option_name='out', add_comment_option=True,
                 **kwargs):
        self._name = name
        self._output_root = output_root
        self._output_option_name = output_option_name
        self._ignore_keys = ('comment', output_option_name)

        super().__init__(**kwargs)
        if add_comment_option:
            self.add_argument('--comment', type=str, default=None,
                              help='comments on this experiment.')

    def parse_args(self, *args, **kwargs):
        """Override ``parse_args`` to dump experiment info to output directory."""
        # parse command line arguments
        args = super().parse_args(*args, **kwargs)

        # check git status
        git_data = check_git_status()

        # build output directory name
        dirname = self._name + '_' if self._name else ''
        dirname += datetime.datetime.now().strftime('%Y%m%d')
        if git_data:
            dirname += '_' + git_data['head'][:7]
        for k, v in vars(args).items():
            if k in self._ignore_keys:
                continue
            default = self.get_default(k)
            if v != default:
                dirname += '_{}-{}'.format(k, v)

        # make directory
        output_dir = os.path.abspath(
                         os.path.join(self._output_root, dirname))
        try:
            os.makedirs(output_dir)
        except OSError:
            pass

        # set 'out' key to namespace object
        setattr(args, self._output_option_name, output_dir)

        # dump collected info
        with open(os.path.join(args.out, 'args'), 'w') as f:
            json.dump(vars(args), f, indent=2)
        if git_data:
            with open(os.path.join(args.out, 'git'), 'w') as f:
                json.dump(git_data, f, indent=2)

        return args
