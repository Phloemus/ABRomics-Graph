
## Competency question routes
##
## All the routes that respond to prewritten competency questions. 
## A competency question is a question of interest that has been asked for by a biologist
##
## routes:
##


from flask_cors import CORS, cross_origin
from flask import jsonify, request

## Config imports
from config.config import *
from config.constants import *

## Util imports
from utils.query import Query

## Competency questions
