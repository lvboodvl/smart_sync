#coding:utf-8
from flask import Flask, request
import json
import os
import time
import oss_upload_img
import infer_label
import send_email
import send_msg
app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def my_json(): 
    upload_file = request.files['image01']
    old_file_name = upload_file.filename
    ai_label = 'unk'
#    print(old_file_name)
    if upload_file:
        file_path = os.path.join('../upload/', old_file_name)
        upload_file.save(file_path)
        objectid = 'upload/' + old_file_name
        oss_upload_img.oss_upload_img(file_path, objectid, save_flag = False)
        object_id, ai_label, score = infer_label.infer_label(file_path)
        print('---------------------------------------------')
        print(object_id, ai_label, score)
        print('---------------------------------------------')
        if ai_label == 'abnormal':
            send_email.SendSSLEmail(file_path, object_id)
            send_msg.send_msg()
            print('//////////////////////////////////')
            print('abnormal!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('//////////////////////////////////')            
            time.sleep(60)
        
        return 'save successful'   
 
if __name__ == '__main__': 
    app.run("0.0.0.0", port=1234)
