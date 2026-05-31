import pytest
import allure
from api.role_api import RoleAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars  # 🔴 引入全局记忆中枢


@allure.epic("若依后台管理系统")
@allure.feature("角色管理模块")
class TestRoleManage:
    role_api = RoleAPI()

    def assert_response(self, response, expected_code):
        """断言"""
        res_json = response.json()
        assert response.status_code == 200
        assert res_json["code"] == expected_code

    @allure.story("新增角色接口")
    @allure.title("测试新增角色 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/role_data.yml", "add_role_cases"))
    def test_add_role(self, global_token, case_data):
        """测试用例1：新增角色"""
        expected = case_data.pop("expected_code")
        res = self.role_api.add_role(global_token, case_data)
        self.assert_response(res, expected)

        # 🔴 新增成功后，提取动态ID
        if expected == 200:
            target_name = case_data["roleName"]
            query_res = self.role_api.get_role_list(global_token, params={"roleName": target_name})

            json_data = query_res.json()
            records = json_data.get("rows", json_data.get("data", []))

            if records:
                GlobalVars.dynamic_role_id = records[0]["roleId"]
                print(f"\n[全链路追踪] 成功提取到新生成的角色 ID: {GlobalVars.dynamic_role_id}")
        print("\n新增角色测试成功!")

    @allure.story("获取角色列表接口")
    @allure.title("测试获取角色列表 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/role_data.yml", "get_role_list_cases"))
    def test_get_role_list(self, global_token, case_data):
        """测试用例2：获取角色列表"""
        expected = case_data.pop("expected_code")
        res = self.role_api.get_role_list(global_token)
        self.assert_response(res, expected)
        print("\n获取角色列表测试成功!")

    @allure.story("获取角色信息接口")
    @allure.title("测试获取角色信息 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/role_data.yml", "get_role_info_cases"))
    def test_get_role_info(self, global_token, case_data):
        """测试用例3：获取角色信息"""
        expected = case_data.pop("expected_code")
        res = self.role_api.get_role_info(global_token, case_data["roleId"])
        self.assert_response(res, expected)
        print("\n获取角色信息测试成功!")

    @allure.story("更新角色接口")
    @allure.title("测试更新角色 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/role_data.yml", "update_role_cases"))
    def test_update_role(self, global_token, case_data):
        """测试用例4：更新角色"""
        expected = case_data.pop("expected_code")

        # 🔴 拦截暗号，动态覆盖
        if case_data.get("roleId") == "DYNAMIC" and GlobalVars.dynamic_role_id:
            case_data["roleId"] = GlobalVars.dynamic_role_id

        res = self.role_api.update_role(global_token, case_data)
        self.assert_response(res, expected)
        print("\n更新角色测试成功!")

    @allure.story("删除角色接口")
    @allure.title("测试删除角色 - 数据驱动")
    @pytest.mark.parametrize("case_data", read_yaml("data/role_data.yml", "delete_role_cases"))
    def test_delete_role(self, global_token, case_data):
        """测试用例5：删除角色"""
        expected = case_data.pop("expected_code")

        # 🔴 拦截暗号 (原代码中取的是 case_data["roleId"])
        target_id = GlobalVars.dynamic_role_id if case_data.get("roleId") == "DYNAMIC" else case_data["roleId"]

        res = self.role_api.delete_role(global_token, target_id)
        self.assert_response(res, expected)
        print("\n删除角色测试成功!")