import requests
from config.setting import BASE_URL

class UserAPI:
    """
    用户管理模块的所有接口 (武器库)
    """

    def login(self, username, password):
        """登录接口，负责拿到并返回 Token"""
        url = f"{BASE_URL}/login"
        payload = {"username": username, "password": password}
        response = requests.post(url, json=payload)
        # 直接把 token 挖出来返回出去
        return response.json().get("token")

    def get_user_list(self, token,params=None):
        """获取用户列表接口"""
        url = f"{BASE_URL}/system/user/list"
        headers = {"Authorization": f"Bearer {token}"}
        # 只负责发请求，把完整的响应结果扔回给前线
        import requests
        return requests.get(url, headers=headers, params=params)

    def add_user(self, token, user_data):
        """新增用户接口 (这里把固定的数据替换成了活的 user_data)"""
        url = f"{BASE_URL}/system/user"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.post(url, json=user_data, headers=headers)

    def update_user(self, token, user_data):
        """更新用户接口"""
        url = f"{BASE_URL}/system/user"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.put(url, json=user_data, headers=headers)

    def delete_user(self, token, user_data):
        """删除用户接口"""
        url = f"{BASE_URL}/system/user/{user_data['userId']}"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(url, headers=headers)

    def get_user_info(self, token, user_id):
        """获取用户信息接口"""
        url = f"{BASE_URL}/system/user/{user_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url, headers=headers)
