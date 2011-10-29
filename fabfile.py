# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function

"""
fab stop_all udpate_code start_all
"""
from datetime import datetime
import sys
import os

from fabric.api import *

DEPLOY_DIR = '~/citypk'

env.hosts = ['']
env.user = 'ubuntu'

def deploy():
  with cd(DEPLOY_DIR):
    with prefix('source ~/envs/citypk/bin/activate'):
        run('supervisorctl stop all')
        run('git pull --rebase')
        run('supervisorctl reload')
        run('supervisorctl status')



