# -*- coding: utf-8 -*-
"""
Experiment Recording Tool
"""


import argparse
import datetime
import os
import json
import re
import subprocess


GIT_INFO_AS_DICT = ('head', 'branch', 'remote')
GIT_INFO_AS_TEXT = ('diff', 'log', 'status')
EXEC_COUNT_PATTERN = '_run-\d+'


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


def _split_lines(text):
    """Split multi-line text content into list of string."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return lines


def check_git_status():
    """Check git repository status."""
    if not _is_under_git_control():
        return None

    git_data = {
        'head': _issue_command('git rev-parse HEAD').strip(),
        'branch': _issue_command('git rev-parse --abbrev-ref HEAD').strip(),
        'diff': _issue_command('git diff'),
        'status': _issue_command('git status'),
        'log': _issue_command('git log -n 30'),
        'remote': _split_lines(_issue_command('git remote -v')),
    }
    return git_data


def _get_execution_count_with_same_name(output_root, dirname):
    """Get execution count with same name."""
    if not os.path.exists(output_root):
        return 0
    existing_names = sorted(os.listdir(output_root))
    execution_count = 0
    pattern = re.compile('^' + dirname + EXEC_COUNT_PATTERN + '$')
    for name in existing_names:
        if not name.startswith(dirname):
            continue
        if name == dirname:
            execution_count = 1
            continue
        if pattern.match(name):
            execution_count = int(name.split('-')[-1])
    return execution_count


class ArgumentParser(argparse.ArgumentParser):
    """Extended argument parser that records some experiment info."""

    def __init__(self, name=None, output_root='./experiments',
                 output_option_name='out', add_comment_option=True,
                 **kwargs):
        self._name = name
        self._output_option_name = output_option_name
        self._ignore_keys = ('comment', 'output_root', output_option_name)

        super().__init__(**kwargs)

        self.add_argument('--output-root', type=str, default=output_root,
                          help='path to root of experiment directories.')
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
        exec_count = _get_execution_count_with_same_name(
            args.output_root, dirname)
        if exec_count:
            dirname += '_run-{}'.format(exec_count + 1)

        # make directory
        output_dir = os.path.abspath(
                         os.path.join(args.output_root, dirname))
        try:
            os.makedirs(output_dir)
        except OSError:
            pass

        # set 'out' key to namespace object and remove 'output_root' key
        setattr(args, self._output_option_name, output_dir)
        del args.output_root

        # dump collected info
        with open(os.path.join(args.out, 'args'), 'w') as f:
            json.dump(vars(args), f, indent=2)
        if git_data:
            # save ``git`` file
            git_data_as_dict = {k: v for k, v in git_data.items()
                                if k in GIT_INFO_AS_DICT}
            with open(os.path.join(args.out, 'git'), 'w') as f:
                json.dump(git_data_as_dict, f, indent=2)
            # save git-XXXX.txt
            for k in GIT_INFO_AS_TEXT:
                fname = 'git-{}.txt'.format(k)
                with open(os.path.join(args.out, fname), 'w') as f:
                    f.write(git_data[k])

        return args
