from common.request_util import RequestUtil
from config.setting import BASE_URL

class DeptAPI:
    def __init__(self):
        self.req = RequestUtil()

    def get_dept_list(self, token, params=None):
        """1. 查询部门列表"""
        url = f"{BASE_URL}/system/dept/list"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, params=params, headers=headers)

    def add_dept(self, token, dept_data):
        """2. 新增部门"""
        url = f"{BASE_URL}/system/dept"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("POST", url, json=dept_data, headers=headers)

    def update_dept(self, token, dept_data):
        """3. 修改部门"""
        url = f"{BASE_URL}/system/dept"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("PUT", url, json=dept_data, headers=headers)

    def delete_dept(self, token, dept_id):
        """4. 删除部门"""
        url = f"{BASE_URL}/system/dept/{dept_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("DELETE", url, headers=headers)