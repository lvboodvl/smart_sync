#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import traceback
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from datahub import DataHub
from datahub.exceptions import ResourceExistException, DatahubException
from datahub.models import FieldType, RecordSchema, TupleRecord, BlobRecord, CursorType, RecordType

access_id = ''
access_key = ''
endpoint = 'https://dh-cn-beijing.aliyuncs.com'

dh = DataHub(access_id, access_key, endpoint)

# =====================  create project =====================
project_name = 'caict_smart_sync'
comment = 'smart_sync'
try:
    dh.create_project(project_name, comment)
    print("create project success!")
    print("=======================================\n\n")
except ResourceExistException:
    print("project already exist!")
    print("=======================================\n\n")
except Exception as e:
    print(traceback.format_exc())
    sys.exit(-1)

# =====================  create topic =====================

# --------------------- wild_label topic ---------------------
tuple_topic = "smart_sync_infer"
shard_count = 1
life_cycle = 7
record_schema = RecordSchema.from_lists(
    ['object_id', 'ai_label', 'score'],
    [FieldType.STRING, FieldType.STRING, FieldType.DOUBLE])

try:
    dh.create_tuple_topic(project_name, tuple_topic, shard_count, life_cycle, record_schema, comment)
    print("create traffic topic success!")
    print("=======================================\n\n")
except ResourceExistException:
    print("topic already exist!")
    print("=======================================\n\n")
except Exception as e:
    print(traceback.format_exc())
    sys.exit(-1)

# ===================== get topic =====================
topic_result = dh.get_topic(project_name, tuple_topic)
print(topic_result)
print(topic_result.record_schema)

# ===================== list shard =====================
shards_result = dh.list_shard(project_name, tuple_topic)
print(shards_result)

# ===================== put tuple records =====================
def dh_infer_label(object_id , ai_label, score):
    try:

        dh.wait_shards_ready(project_name, tuple_topic)
        # print("shards all ready!!!")
        # print("=======================================\n\n")

        topic_result = dh.get_topic(project_name, tuple_topic)
#        print(topic_result)
        if topic_result.record_type != RecordType.TUPLE:
            print("topic type illegal!")
            sys.exit(-1)
#        print("=======================================\n\n")

        record_schema = topic_result.record_schema
        #
        records0 = []


        record1 = TupleRecord(schema=record_schema)
        record1.set_value('object_id', object_id)
        record1.set_value('ai_label', ai_label)
        record1.set_value('score', float(score))
        record1.hash_key = '4FFFFFFFFFFFFFFD7FFFFFFFFFFFFFFD'
        records0.append(record1)

        dh.put_records(project_name, tuple_topic, records0)

    except DatahubException as e:
        print(e)
        sys.exit(-1)


if __name__=='__main__' :
    object_id = '2020-7-16'
    ai_label = 'unk'
    score = 0.99
    dh_infer_label(object_id, ai_label, score)
    print ('well done!')
