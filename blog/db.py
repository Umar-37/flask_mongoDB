#!/usr/bin/env python

from pymongo import MongoClient
from flask import current_app, g

def get_db(collection):
   if "db" not in g:
      g.db = MongoClient(current_app.config["DATABASE"])
   return g.db["blog"][collection]
