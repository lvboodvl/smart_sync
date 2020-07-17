# coding: utf-8
'''
upload data to OSS in aliyun cloud
'''
import oss2
import os
auth = oss2.Auth('', '')
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '')


def oss_upload_img(save_path, objectid, save_flag = True):
    remoteName = objectid
    bucket.put_object_from_file(remoteName, save_path)
    if save_flag == False:
        os.remove(save_path)
    else:
        pass

if __name__ == "__main__":
    save_path = ''
    cjt_objectid = ''
    oss_upload_img(save_path, cjt_objectid)
