from common.request_util import RequestUtil
from config.setting import BASE_URL


class RoleAPI:
    # 实例化发送器
    req = RequestUtil()

    def get_role_list(self, token, params=None):
        """获取角色列表接口"""
        url = f"{BASE_URL}/system/role/list"
        headers = {"Authorization": f"Bearer {token}"}

        import requests
        return requests.get(url, headers=headers, params=params)

    def add_role(self, token, role_data):
        """新增角色接口"""
        url = f"{BASE_URL}/system/role"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("POST", url, json=role_data, headers=headers)

    def get_role_info(self, token, role_id):
        """获取角色信息接口"""
        url = f"{BASE_URL}/system/role/{role_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def update_role(self, token, role_data):
        """更新角色接口"""
        url = f"{BASE_URL}/system/role"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("PUT", url, json=role_data, headers=headers)

    def delete_role(self, token, role_id):
        """删除角色接口"""
        url = f"{BASE_URL}/system/role/{role_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("DELETE", url, headers=headers)