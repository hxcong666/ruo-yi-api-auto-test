import requests
import pytest

from api_test import payload


class TestUserManage:
    # 类的初始化，用来存放全局共享的数据
    base_url = "http://localhost:8080"
    headers = {}

    def setup_class(self):
        """
        前置准备工作：在所有测试开始前，先去拿一下token
        """
        print("\n--- 测试开始：自动登录获取 Token ---")
        login_url = f"{self.base_url}/login"
        payload = {"username": "admin", "password": "admin123"}
        res = requests.post(login_url, json=payload).json()

        # 提取 Token 并组装成带 Bearer 的 Headers
        token = res.get("token")
        self.headers = {"Authorization": f"Bearer {token}"}
        print(f"Token 拿到了！")

    def test_02_add_user(self):
        """
        测试用例 1：新增用户
        """
        add_url = f"{self.base_url}/test/user/save?userId=99&username=auto_test&password=password&mobile=1380000001"
        # 假接口要求传啥我们就传啥
        payload = {"userId": 99, "username": "auto_test","password":"password" ,"mobile": "13800000001"}

        response = requests.post(add_url, json=payload, headers=self.headers)

        assert response.json()["code"] == 200
        print("\n新增用户测试通过！")

    def test_03_update_user(self):
        """
        测试用例 2：更新用户
        """
        update_url = f"{self.base_url}/test/user/update"
        payload={
            "userId": 99,
            "username": "auto_test",
            "password": "password",
            "mobile": "13800000001"
        }
        response = requests.put(update_url, json=payload, headers=self.headers)
        assert response.json()["code"] == 200
        print("\n更新用户测试通过！")

    def test_04_delete_user(self):
        """
        测试用例 3：删除用户
        """
        delete_url = f"{self.base_url}/test/user/99"
        response = requests.delete(delete_url, headers=self.headers)
        assert response.json()["code"] == 200
        print("\n删除用户测试通过！")

    def test_05_get_user_info(self):
        """
        测试用例 4：获取用户详细
        """
        info_url = f"{self.base_url}/test/user/2"
        response = requests.get(info_url, headers=self.headers)
        res_json = response.json()
        print(res_json)

        assert response.status_code == 200
        assert res_json["code"] == 200
        assert res_json["msg"] == "操作成功"
        print("\n获取用户信息测试通过！")

    def test_06_get_user_list(self):
        """
        测试用例 5：获取用户列表
        """
        list_url = f"{self.base_url}/test/user/list"
        response = requests.get(list_url, headers=self.headers)
        res_json = response.json()
        print(res_json)

        assert res_json["code"] == 200
        assert res_json["msg"] == "操作成功"
        print("\n获取用户列表测试通过！")