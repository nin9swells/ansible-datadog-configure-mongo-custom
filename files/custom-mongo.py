import os
import time
import sys
import random
import socket
import bson

from pymongo import MongoClient
from checks import AgentCheck

thresholds = [5000000, 15000000, 30000000]
TO_SEC_CONST = 1000000

class MongoDBCustomCheck(AgentCheck):
    def check(self, instance):
        mongo_url = instance['server']
        metrics = {}

        mongo_client = MongoClient(mongo_url)
        db_admin = mongo_client.admin
        db_local = mongo_client.local
        is_master_result = db_admin.command('ismaster')
        if is_master_result:
            if 'setName' in is_master_result:
                tags = [ 'ismaster:' + str(is_master_result['ismaster']), 'replset_name:'+is_master_result['setName'] ]
            else:
                tags = [ 'ismaster:' + str(is_master_result['ismaster']) ]
        else:
            tags = []

        try:
            for threshold in thresholds:
                curr_op = db_admin.current_op()

                def is_long_running(op):
                    return op['op'] != 'none'\
                        and op['ns'] != 'local.oplog.rs'\
                        and op['active'] is True \
                        and op['microsecs_running'] >= threshold

                filtered_curr = filter(is_long_running, curr_op['inprog'])
                conv_threshold = threshold/TO_SEC_CONST
                m_name = 'custom.mongodb.curr_op_' + str(conv_threshold) + 's'
                self.gauge(m_name, len(filtered_curr), tags=tags)
        except bson.errors.InvalidBSON as e:
            self.fail_event('Failed to get current_op data', e)

    def fail_event(message, exception):
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'failure',
            'msg_title': 'Caught exception',
            'msg_text': '%s: %s' % (message, exception)
        })

if __name__ == '__main__':
    check, instances = MongoDBCustomCheck.from_yaml('/etc/dd-agent/conf.d/custom-mongo.yaml')
    for instance in instances:
        print '\nRunning the check for: %s' % (instance['server'])
        check.check(instance)
        if check.has_events():
            print 'Events: %s' % (check.get_events())
        print 'Metrics: %s' % (check.get_metrics())

