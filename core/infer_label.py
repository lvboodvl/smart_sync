#!/usr/bin/env python
# coding: utf-8
import os
import sys
import random

caffe_path = '../caffe/python/'
sys.path.insert(0, caffe_path)
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from caffe.proto import caffe_pb2
from google.protobuf import text_format
import numpy as np
#import cv2
#import matplotlib.pyplot as plt
import time
from mq_write import dh_infer_label
import oss2
import infer

'''
init oss account, datahub account, caffe prototxt, caffemodel, labelmaps
'''
auth = oss2.Auth('', '')
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '')
#################################################################################

root_googlenet = '../model/'
#deploy_googlenet = root_googlenet + 'deploy.prototxt'
labels_filename = root_googlenet + 'labels.txt'

deploy_googlenet = root_googlenet + 'deploy-googlenet.prototxt'
#labels_filename = root_googlenet + 'labels.txt'
caffe_model_googlenet = root_googlenet + 'googlenet.caffemodel'
googlenet = caffe.Net(deploy_googlenet, caffe_model_googlenet, caffe.TEST)
#################################################################################

def infer_label(path, th = 0.5):
    object_id = path.split('/')[-1]
    object_id = object_id.split('.')[0]
    url = path
    labels_googlenet, score_googlenet, _ = infer.infer_img(googlenet, url)
#    if labels_googlenet == 'normal' and score_googlenet < 0.89:
#        labels_googlenet = 'unk'
#        score_googlenet = 0.66666666
#    else:
#        pass
    dh_infer_label(object_id, labels_googlenet, score_googlenet)
    return object_id, labels_googlenet, score_googlenet

if __name__ == "__main__":
    path = '../model/a.jpg'
    object_id, ai_label, score = infer_label(path)
    print(object_id)
    print(ai_label, score)
