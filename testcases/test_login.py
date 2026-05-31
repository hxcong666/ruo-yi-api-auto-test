import pytest
import allure
from api.login_api import LoginAPI
from common.yaml_util import read_yaml


@allure.epic("若依后台管理系统")
@allure.feature("登录与认证模块")
class TestLoginAuth:
    login_api = LoginAPI()

    def assert_response(self, response, expected_code):
        """通用的断言验尸官"""
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("验证码接口")
    @allure.title("测试获取验证码图片")
    def test_get_code_img(self):
        """虽然关了验证码校验，但接口本身还是能通的"""
        res = self.login_api.get_code_img()
        self.assert_response(res, 200)

    @allure.story("登录系统接口")
    @allure.title("测试多场景登录(含异常登录)")
    @pytest.mark.parametrize("case_data", read_yaml("data/login_data.yml", "login_cases"))
    def test_login(self, case_data):
        expected = case_data.pop("expected_code")

        res = self.login_api.login(
            username=case_data["username"],
            password=case_data["password"],
            code="",
            uuid=""
        )
        self.assert_response(res, expected)

    @allure.story("获取用户信息接口")
    @allure.title("测试获取当前登录人信息")
    def test_get_info(self, global_token):
        """这个接口需要权限，正常使用全局 Token 即可"""
        res = self.login_api.get_info(global_token)
        self.assert_response(res, 200)

    @allure.story("退出系统接口")
    @allure.title("测试安全注销退出")
    def test_logout(self):
        """
        隔离战术：为了保护 global_token 不被销毁，我们在这里临时申请一把一次性的新钥匙
        """
        # 1. 临时造一把新钥匙
        temp_login_res = self.login_api.login("admin", "admin123", "", "")
        temp_token = temp_login_res.json().get("token")

        # 2. 拿这把一次性钥匙去测试退出接口
        res = self.login_api.logout(temp_token)

        # 3. 验证退出是否成功
        self.assert_response(res, 200)

    @allure.story("注册账号接口")
    @allure.title("测试新用户注册(正向与异常)")
    @pytest.mark.parametrize("case_data", read_yaml("data/login_data.yml", "register_cases"))
    def test_register(self, case_data):
        """
        注意：底层的 yaml_util 会自动将 ${TIMESTAMP} 替换为唯一标识，保证每次注册都不会冲突。
        """
        expected = case_data.pop("expected_code")
        res = self.login_api.register(case_data)
        self.assert_response(res, expected)

    @allure.story("解锁屏幕接口")
    @allure.title("测试系统锁屏后的密码验证")
    @pytest.mark.parametrize("case_data", read_yaml("data/login_data.yml", "unlock_screen_cases"))
    def test_unlock_screen(self, global_token, case_data):
        """解锁操作是需要核对【当前登录人】的密码的，所以必须传 Token"""
        expected = case_data.pop("expected_code")

        target_password = case_data["password"]
        res = self.login_api.unlock_screen(global_token, target_password)
        self.assert_response(res, expected)