#!/usr/bin/env python2.7

from gevent import monkey

monkey.patch_all()

from psycogreen.gevent import patch_psycopg

patch_psycopg()

from orig_manage import main

main()
