from common.request_util import RequestUtil
from config.setting import BASE_URL

class MenuAPI:
    def __init__(self):
        self.req = RequestUtil()

    def get_menu_list(self, token, params=None):
        """1. 查询菜单列表"""
        url = f"{BASE_URL}/system/menu/list"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, params=params, headers=headers)

    def get_menu_info(self, token, menu_id):
        """2. 查询菜单详细"""
        url = f"{BASE_URL}/system/menu/{menu_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def get_menu_treeselect(self, token):
        """3. 查询菜单下拉树结构"""
        url = f"{BASE_URL}/system/menu/treeselect"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def get_role_menu_treeselect(self, token, role_id):
        """4. 根据角色ID查询菜单下拉树结构"""
        url = f"{BASE_URL}/system/menu/roleMenuTreeselect/{role_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("GET", url, headers=headers)

    def add_menu(self, token, menu_data):
        """5. 新增菜单"""
        url = f"{BASE_URL}/system/menu"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("POST", url, json=menu_data, headers=headers)

    def update_menu(self, token, menu_data):
        """6. 修改菜单"""
        url = f"{BASE_URL}/system/menu"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("PUT", url, json=menu_data, headers=headers)

    def update_menu_sort(self, token, menu_data):
        """7. 保存菜单排序"""
        url = f"{BASE_URL}/system/menu/updateSort"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("PUT", url, json=menu_data, headers=headers)

    def delete_menu(self, token, menu_id):
        """8. 删除菜单"""
        url = f"{BASE_URL}/system/menu/{menu_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return self.req.send_request("DELETE", url, headers=headers)