from common.request_util import RequestUtil
from config.setting import BASE_URL

class PostAPI:
    def __init__(self):
        self.req = RequestUtil()

    def get_post_list(self, token, params=None):
        """1. 查询岗位列表"""
        url = f"{BASE_URL}/system/post/list"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, params=params, headers=headers)

    def get_post_info(self, token, post_id):
        """2. 查询岗位详细"""
        url = f"{BASE_URL}/system/post/{post_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def add_post(self, token, post_data):
        """3. 新增岗位"""
        url = f"{BASE_URL}/system/post"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("POST", url, json=post_data, headers=headers)

    def update_post(self, token, post_data):
        """4. 修改岗位"""
        url = f"{BASE_URL}/system/post"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("PUT", url, json=post_data, headers=headers)

    def delete_post(self, token, post_id):
        """5. 删除岗位"""
        url = f"{BASE_URL}/system/post/{post_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("DELETE", url, headers=headers)