# coding = utf-8
"""
@author: zhou
@time:2019/6/25 18:54
"""

import redis


def redis_conn_pool():
    pool = redis.ConnectionPool(host='redis-12143.c8.us-east-1-3.ec2.cloud.redislabs.com', port=12143,
                                decode_responses=True, password='pkAWNdYWfbLLfNOfxTJinm9SO16eSJFx')
    r = redis.Redis(connection_pool=pool)
    return r

