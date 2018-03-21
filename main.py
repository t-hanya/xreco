#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sample program
"""


from xreco import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(name='train')
    parser.add_argument('dataset', choices=['mnist', 'cifar10'])
    parser.add_argument('--batchsize', '-b', type=int, default=32)
    args = parser.parse_args()
