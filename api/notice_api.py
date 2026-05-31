from common.request_util import RequestUtil
from config.setting import BASE_URL

class NoticeAPI:
    def __init__(self):
        self.req = RequestUtil()
        self.base_url = f"{BASE_URL}/system/notice"

    def get_notice_list(self, token, params=None):
        """1. 查询公告列表"""
        return self.req.send_request("GET", f"{self.base_url}/list", params=params, headers={"Authorization": f"Bearer {token}"})

    def get_notice_info(self, token, notice_id):
        """2. 查询公告详细"""
        return self.req.send_request("GET", f"{self.base_url}/{notice_id}", headers={"Authorization": f"Bearer {token}"})

    def add_notice(self, token, notice_data):
        """3. 新增公告"""
        return self.req.send_request("POST", self.base_url, json=notice_data, headers={"Authorization": f"Bearer {token}"})

    def update_notice(self, token, notice_data):
        """4. 修改公告"""
        return self.req.send_request("PUT", self.base_url, json=notice_data, headers={"Authorization": f"Bearer {token}"})

    def delete_notice(self, token, notice_id):
        """5. 删除公告"""
        return self.req.send_request("DELETE", f"{self.base_url}/{notice_id}", headers={"Authorization": f"Bearer {token}"})

    def list_notice_top(self, token):
        """6. 首页顶部公告列表（带已读状态）"""
        return self.req.send_request("GET", f"{self.base_url}/listTop", headers={"Authorization": f"Bearer {token}"})

    def mark_notice_read(self, token, notice_id):
        """7. 标记公告已读 (这是 POST 请求，但参数是在 URL query 里)"""
        return self.req.send_request("POST", f"{self.base_url}/markRead", params={"noticeId": notice_id}, headers={"Authorization": f"Bearer {token}"})

    def mark_notice_read_all(self, token, ids):
        """8. 批量标记已读 (参数是逗号分隔的字符串)"""
        return self.req.send_request("POST", f"{self.base_url}/markReadAll", params={"ids": ids}, headers={"Authorization": f"Bearer {token}"})

    def list_notice_read_users(self, token, params=None):
        """9. 查询公告已读用户列表"""
        return self.req.send_request("GET", f"{self.base_url}/readUsers/list", params=params, headers={"Authorization": f"Bearer {token}"})