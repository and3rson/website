from redis import TimeoutError
from redis.client import Redis


def publish(key, values):
    client = Redis()
    client.lpush(key, values)
    # print 'Publishing', key
    # client.publish(key, values)
    # pubsub = client.pubsub()
    # client.lpush(key, values)


def expect(key, timeout=15):
    client = Redis(socket_timeout=timeout)
    client.lpush(key, None)
    client.delete(key)
    print 'Expecting', key
    try:
        return client.brpop(key, timeout)
    except TimeoutError:
        return None
    # pubsub = client.pubsub()
    # pubsub.subscribe(key)
    # try:
    #     for item in pubsub.listen():
    #         if item['type'] == 'message':
    #             pubsub.unsubscribe()
    #             return item['data']
    # except TimeoutError:
    #     return None


def clear(key):
    return
    # client = Redis()
    # print 'Clearing', key
    # client.delete(key)
