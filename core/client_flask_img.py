# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 20:00:24 2019

@author: Bo Lv
"""
#coding:utf-8
import os 
import requests
import pic_snapshots
import time
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

while(1):
    file_name = pic_snapshots.snapshot_fun()
    path=os.path.join(BASE_DIR,'snapshots_imgs',file_name) 
    img = {'image01': (file_name,open(path,'rb'),'image/jpg')}
    r = requests.post("http://xx.xx.xx.xx:1234", files = img)
    print(file_name)
    time.sleep(5)