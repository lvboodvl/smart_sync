import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class ZhenziSmsClient(object):
	def __init__(self, apiUrl, appId, appSecret):
		self.apiUrl = apiUrl
		self.appId = appId
		self.appSecret = appSecret

	def send(self, params):
		data = params;
		data['appId'] = self.appId;
		data['appSecret'] = self.appSecret;
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning);
		response = requests.post(self.apiUrl+'/sms/send.do', data=data, verify=False);
		result = str(response.content,'utf-8');
		return result


	def balance(self):
		data = {
		    'appId': self.appId,
		    'appSecret': self.appSecret
		}
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning);
		response = requests.post(self.apiUrl+'/account/balance.do', data=data, verify=False);
		result = str(response.content,'utf-8');
		return result

	def findSmsByMessageId(self, messageId):
		data = {
		    'appId': self.appId,
		    'appSecret': self.appSecret,
		    'messageId': messageId
		}
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning);
		response = requests.post(self.apiUrl+'/smslog/findSmsByMessageId.do', data=data, verify=False);
		result = str(response.content,'utf-8');
		return result


def send_msg():
    apiUrl = 'https://sms_developer.zhenzikj.com'
    appId = '105738'
    appSecret = '852e151b-3f3b-4777-9222-a595076cfb00'
    client = ZhenziSmsClient(apiUrl, appId, appSecret)
    params = {'message':'The testing state of SyncEdge is abnormal!!!!!!!!!!!!!!!', 'number':'18601309707'}
    result = client.send(params) 
    return result   

if __name__ == '__main__': 
    send_msg()    
    print('send short msg!!!!!!!!!!')
