#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import sys

def set_log_format():
    logging.basicConfig(level=logging.DEBUG,
                format='%(threadName)-12s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='task_manager.log',
                filemode='a')

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(filename)-12s line:%(lineno)d: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    console_err = logging.StreamHandler(sys.stderr)
    console_err.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(filename)-12s line:%(lineno)d: %(levelname)-8s %(message)s')
    console_err.setFormatter(formatter)
    logging.getLogger('').addHandler(console_err)