#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    POSTGRES = {
    'user': 'admin',
    'pw': 'admin',
    'db': 'testdb',
    'host': '192.168.99.100',
    'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES