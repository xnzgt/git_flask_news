from info import redis_store
from info.modules.index import index_blu


@index_blu.route('/')
def index():
    redis_store.set("name","刘亦菲")
    return "helloWorld"