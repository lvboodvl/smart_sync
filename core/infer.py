#coding=utf-8

'''
infer module
'''

import sys
caffe_path = '../caffe/python/'
#caffe_path = '/root/caffe/python/'
sys.path.insert(0, caffe_path)
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from caffe.proto import caffe_pb2
from google.protobuf import text_format
import numpy as np
#import cv2

'''
prepare caffemodel proto labelmap etc.
'''
root_googlenet = '../model/'
deploy_googlenet = root_googlenet + 'deploy-googlenet.prototxt'
#labels_filename = root_googlenet + 'labels.txt'
caffe_model_googlenet = root_googlenet + 'googlenet.caffemodel'
googlenet = caffe.Net(deploy_googlenet, caffe_model_googlenet, caffe.TEST)
# labels = np.loadtxt(labels_filename, str, delimiter='\t')
root_alexnet = root_googlenet
#deploy_alexnet = root_alexnet + 'deploy-alex.prototxt'
labels_filename = root_alexnet + 'labels.txt'
#caffe_model_alexnet = root_alexnet + 'snapshot_iter_992.caffemodel'
#alexnet = caffe.Net(deploy_alexnet, caffe_model_alexnet, caffe.TEST)

'''
define infer function with alexnet, googlenet and senet
output parm is prob(score) and class_label respectively
'''

def infer_img(googlenet, url):
    transformer = caffe.io.Transformer({'data': googlenet.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_raw_scale('data', 255)
    transformer.set_channel_swap('data', (2,1,0))
    labels = np.loadtxt(labels_filename, str, delimiter='\t')

#    googlenet.blobs['data'].data[...] = transformer.preprocess('data', tmp)
#    googlenet.forward()
#    prob_googlenet = googlenet.blobs['softmax'].data[0].flatten()
#    order_googlenet = prob_googlenet.argsort()[-1]
#    score_googlenet = np.max(prob_googlenet)
#    labels_googlenet = labels[order_googlenet]
    image = caffe.io.load_image(url)
    googlenet.blobs['data'].data[...] = transformer.preprocess('data', image)
    googlenet.forward()
    prob_googlenet = googlenet.blobs['softmax'].data[0].flatten()
    order_googlenet = prob_googlenet.argsort()[-1]
    score_googlenet = np.max(prob_googlenet)
    labels_googlenet = labels[order_googlenet]

    return labels_googlenet, score_googlenet, prob_googlenet

if __name__ == '__main__':
    url = root_googlenet + 'a.jpg'
    labels_googlenet, score_googlenet, prob_googlenet = infer_img(googlenet, url)

    print(url, labels_googlenet, score_googlenet, prob_googlenet)
