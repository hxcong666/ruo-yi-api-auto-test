import pytest
import allure
from api.user_api import UserAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars


@allure.epic("若依后台管理系统")
@allure.feature("用户管理模块")
class TestUserManage:
    # 实例化武器库
    user_api = UserAPI()

    def assert_response(self, response, expected_code):
        """断言"""
        res_json = response.json()
        print(f"\n接口返回详情: {response.text}")
        assert response.status_code == 200
        assert res_json["code"] == expected_code

    @allure.story("获取用户列表接口")
    @allure.title("测试获取用户列表 - 数据驱动")
    def test_get_user_list(self, global_token):
        """测试用例1：获取用户列表"""
        res = self.user_api.get_user_list(global_token)
        self.assert_response(res, 200)
        print("\n获取用户列表成功！")

    @allure.story("新增用户接口")
    @allure.title("测试新增用户 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/user_data.yml", "add_user_cases"))
    def test_add_user(self, global_token, case_data):
        """测试用例2：新增用户"""
        expected = case_data.pop("expected_code")
        res = self.user_api.add_user(global_token, case_data)
        self.assert_response(res, expected)

        # 新增成功后，提取动态ID
        if expected == 200:
            target_name = case_data["userName"]
            query_res = self.user_api.get_user_list(global_token, params={"userName": target_name})

            json_data = query_res.json()
            records = json_data.get("rows", json_data.get("data", []))

            if records:
                GlobalVars.dynamic_user_id = records[0]["userId"]
                print(f"\n[全链路追踪] 成功提取到新生成的用户 ID: {GlobalVars.dynamic_user_id}")
        print("\n新增用户测试通过！")

    @allure.story("更新用户接口")
    @allure.title("测试更新用户 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/user_data.yml", "update_user_cases"))
    def test_update_user(self, global_token, case_data):
        """测试用例3：更新用户"""
        expected = case_data.pop("expected_code")

        # 拦截暗号，动态覆盖
        if case_data.get("userId") == "DYNAMIC" and GlobalVars.dynamic_user_id:
            case_data["userId"] = GlobalVars.dynamic_user_id

        res = self.user_api.update_user(global_token, case_data)
        self.assert_response(res, expected)
        print("\n更新用户测试通过！")

    @allure.story("删除用户接口")
    @allure.title("测试删除用户 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/user_data.yml", "delete_user_cases"))
    def test_delete_user(self, global_token, case_data):
        """测试用例4：删除用户"""
        expected = case_data.pop("expected_code")

        # 核心修复：精准提取 ID，并识别 DYNAMIC 暗号
        if case_data.get("userId") == "DYNAMIC" and GlobalVars.dynamic_user_id:
            case_data["userId"] = GlobalVars.dynamic_user_id

        res = self.user_api.delete_user(global_token, case_data)
        self.assert_response(res, expected)
        print("\n删除用户测试通过！")

    @allure.story("获取用户信息接口")
    @allure.title("测试获取用户信息 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/user_data.yml", "get_user_info_cases"))
    def test_get_user_info(self, global_token, case_data):
        """测试用例5：获取用户信息"""
        expected = case_data.pop("expected_code")
        res = self.user_api.get_user_info(global_token, case_data["userId"])
        self.assert_response(res, expected)
        print("\n获取用户信息测试通过！")