from common.request_util import RequestUtil
from config.setting import BASE_URL

class ConfigAPI:
    def __init__(self):
        self.req = RequestUtil()
        self.base_url = f"{BASE_URL}/system/config"

    def get_config_list(self, token, params=None):
        """1. 查询参数列表"""
        return self.req.send_request("GET", f"{self.base_url}/list", params=params, headers={"Authorization": f"Bearer {token}"})

    def get_config_info(self, token, config_id):
        """2. 查询参数详细"""
        return self.req.send_request("GET", f"{self.base_url}/{config_id}", headers={"Authorization": f"Bearer {token}"})

    def get_config_key(self, token, config_key):
        """3. 根据参数键名查询参数值"""
        return self.req.send_request("GET", f"{self.base_url}/configKey/{config_key}", headers={"Authorization": f"Bearer {token}"})

    def add_config(self, token, config_data):
        """4. 新增参数配置"""
        return self.req.send_request("POST", self.base_url, json=config_data, headers={"Authorization": f"Bearer {token}"})

    def update_config(self, token, config_data):
        """5. 修改参数配置"""
        return self.req.send_request("PUT", self.base_url, json=config_data, headers={"Authorization": f"Bearer {token}"})

    def delete_config(self, token, config_id):
        """6. 删除参数配置"""
        return self.req.send_request("DELETE", f"{self.base_url}/{config_id}", headers={"Authorization": f"Bearer {token}"})

    def refresh_cache(self, token):
        """7. 刷新参数缓存"""
        return self.req.send_request("DELETE", f"{self.base_url}/refreshCache", headers={"Authorization": f"Bearer {token}"})