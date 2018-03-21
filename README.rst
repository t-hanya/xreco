====================================
xreco: Utility to record experiments
====================================


This repository contains the implementation of extended ArgumentParser class that records experiment information in the output directory. 


Usage
=====

Sample program ( ``main.py`` ):

.. code-block:: python

   # -*- coding: utf-8 -*-


   from xreco import ArgumentParser


   if __name__ == "__main__":
       parser = ArgumentParser(name='train')
       parser.add_argument('dataset', choices=['mnist', 'cifar10'])
       parser.add_argument('--batchsize', '-b', type=int, default=32)
       args = parser.parse_args()


Run with various arguments::

   $ python main.py mnist
   $ python main.py mnist
   $ python main.py cifar10
   $ python main.py mnist --batchsize 128


Created contents::

    experiments/
    ├── train_20180321_003f20d_dataset-cifar10
    │   ├── args
    │   ├── git
    │   ├── git-diff.txt
    │   ├── git-log.txt
    │   └── git-status.txt
    ├── train_20180321_003f20d_dataset-mnist
    │   ├── args
    │   ├── git
    │   ├── git-diff.txt
    │   ├── git-log.txt
    │   └── git-status.txt
    ├── train_20180321_003f20d_dataset-mnist_batchsize-128
    │   ├── args
    │   ├── git
    │   ├── git-diff.txt
    │   ├── git-log.txt
    │   └── git-status.txt
    └── train_20180321_003f20d_dataset-mnist_run-2
        ├── args
        ├── git
        ├── git-diff.txt
        ├── git-log.txt
        └── git-status.txt

----

Copyright(c) 2018 Toshinori Hanya
Released under the MIT License
http://opensource.org/licenses/mit-license.php
