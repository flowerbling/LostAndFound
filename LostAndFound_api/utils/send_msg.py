import requests


class Message(object):

    def __init__(self, api_key):
        # 账号的唯一标识
        self.api_key = api_key
        # 单条发送短信的接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        """
        短信发送的实现
        手机号
        验证码
        """
        params = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【张晚恒】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        req = requests.post(self.single_send_url, data=params)
        print(req)
