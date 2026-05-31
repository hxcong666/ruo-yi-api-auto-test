import pytest
import allure
from api.menu_api import MenuAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars


@allure.epic("若依后台管理系统")
@allure.feature("菜单管理模块")
class TestMenuManage:
    menu_api = MenuAPI()

    def assert_response(self, response, expected_code):
        """通用的断言"""
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("查询菜单列表接口")
    def test_get_menu_list(self, global_token):
        res = self.menu_api.get_menu_list(global_token)
        self.assert_response(res, 200)

    @allure.story("查询菜单详细接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "get_info_cases"))
    def test_get_menu_info(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        target_id = case_data["menuId"]
        res = self.menu_api.get_menu_info(global_token, target_id)
        self.assert_response(res, expected)

    @allure.story("查询菜单下拉树结构接口")
    def test_get_menu_treeselect(self, global_token):
        res = self.menu_api.get_menu_treeselect(global_token)
        self.assert_response(res, 200)

    @allure.story("根据角色ID查询菜单下拉树")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "get_role_menu_cases"))
    def test_get_role_menu_treeselect(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        target_role_id = case_data["roleId"]
        res = self.menu_api.get_role_menu_treeselect(global_token, target_role_id)
        self.assert_response(res, expected)

    @allure.story("新增菜单接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "add_menu_cases"))
    def test_add_menu(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.menu_api.add_menu(global_token, case_data)
        self.assert_response(res, expected)
        # 新增成功后，立刻调用查询接口提取动态 ID
        if expected == 200:
            # 拿到刚才新增的名字 (比如 "自动化大盘_1716382910")
            target_name = case_data["menuName"]
            # 传参给列表查询接口
            query_res = self.menu_api.get_menu_list(global_token, params={"menuName": target_name})
            records = query_res.json().get("data", [])

            if records:
                # 抓取第一条记录的 menuId，存入全局记忆中枢！
                GlobalVars.dynamic_menu_id = records[0]["menuId"]
                print(f"\n成功提取到新生成的菜单 ID: {GlobalVars.dynamic_menu_id}")

    @allure.story("修改菜单接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "update_menu_cases"))
    def test_update_menu(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        # 强行覆盖 YAML 里的死数据
        if case_data.get("menuId") == "DYNAMIC" and GlobalVars.dynamic_menu_id:
            case_data["menuId"] = GlobalVars.dynamic_menu_id
        res = self.menu_api.update_menu(global_token, case_data)
        self.assert_response(res, expected)

    @allure.story("保存菜单排序接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "update_sort_cases"))
    def test_update_menu_sort(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.menu_api.update_menu_sort(global_token, case_data)
        self.assert_response(res, expected)

    @allure.story("删除菜单接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/menu_data.yml", "delete_menu_cases"))
    def test_delete_menu(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        # 用提取到的动态 ID 替换 YAML 里原本的 ID
        target_id = GlobalVars.dynamic_menu_id if case_data.get("menuId") == "DYNAMIC" else case_data["menuId"]
        res = self.menu_api.delete_menu(global_token, target_id)
        self.assert_response(res, expected)