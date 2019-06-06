from flask import session

from info.modules.index import index_blu

@index_blu.route('/')
def index():
    session["name"] = '刘亦菲'
    return "helloWorld"