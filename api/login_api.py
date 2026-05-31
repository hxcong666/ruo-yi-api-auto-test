from common.request_util import RequestUtil
from config.setting import BASE_URL

class LoginAPI:
    def __init__(self):
        self.req = RequestUtil()

    def get_code_img(self):
        """1. 获取验证码"""
        url = f"{BASE_URL}/captchaImage"
        return self.req.send_request("GET", url)

    def login(self, username, password, code="", uuid=""):
        """2. 登录方法"""
        url = f"{BASE_URL}/login"
        payload = {
            "username": username,
            "password": password,
            "code": code,
            "uuid": uuid
        }
        return self.req.send_request("POST", url, json=payload)

    def get_info(self, token):
        """3. 获取用户详细信息"""
        url = f"{BASE_URL}/getInfo"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def logout(self, token):
        """4. 退出方法"""
        url = f"{BASE_URL}/logout"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("POST", url, headers=headers)

    def register(self, register_data):
        """5. 注册方法"""
        url = f"{BASE_URL}/register"
        return self.req.send_request("POST", url, json=register_data)

    def unlock_screen(self, token, password):
        """6. 解锁屏幕"""
        url = f"{BASE_URL}/unlockscreen"
        headers = {"Authorization": f"Bearer {token}"}
        # 前端源码显示，这里的 password 是放在 json 里的
        return self.req.send_request("POST", url, json={"password": password}, headers=headers)