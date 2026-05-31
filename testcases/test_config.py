import pytest
import allure
from api.config_api import ConfigAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars  # 🔴 引入全局记忆中枢


@allure.epic("若依后台管理系统")
@allure.feature("参数设置模块")
class TestConfigManage:
    config_api = ConfigAPI()

    def assert_response(self, response, expected_code):
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("查询参数列表接口")
    def test_get_config_list(self, global_token):
        res = self.config_api.get_config_list(global_token)
        self.assert_response(res, 200)

    @allure.story("查询参数详细接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/config_data.yml", "get_info_cases"))
    def test_get_config_info(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.config_api.get_config_info(global_token, case_data["configId"])
        self.assert_response(res, expected)

    @allure.story("根据键名查询参数接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/config_data.yml", "get_config_key_cases"))
    def test_get_config_key(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.config_api.get_config_key(global_token, case_data["configKey"])
        self.assert_response(res, expected)

    @allure.story("新增参数接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/config_data.yml", "add_config_cases"))
    def test_add_config(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.config_api.add_config(global_token, case_data)
        self.assert_response(res, expected)

        # 新增成功后提取动态ID
        if expected == 200:
            target_key = case_data["configKey"]
            # 参数列表查询接口支持按 configKey 查询
            query_res = self.config_api.get_config_list(global_token, params={"configKey": target_key})

            json_data = query_res.json()
            # 若依列表通常放在 rows，有些放在 data，这里用双重保险
            records = json_data.get("rows", json_data.get("data", []))

            if records:
                GlobalVars.dynamic_config_id = records[0]["configId"]
                print(f"\n[全链路追踪] 成功提取到新生成的参数 ID: {GlobalVars.dynamic_config_id}")

    @allure.story("修改参数接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/config_data.yml", "update_config_cases"))
    def test_update_config(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 🔴 核心拦截：遇到暗号才用提取到的全局动态 ID 覆盖
        if case_data.get("configId") == "DYNAMIC" and GlobalVars.dynamic_config_id:
            case_data["configId"] = GlobalVars.dynamic_config_id

        res = self.config_api.update_config(global_token, case_data)
        self.assert_response(res, expected)

    @allure.story("删除参数接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/config_data.yml", "delete_config_cases"))
    def test_delete_config(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 🔴 核心拦截：识别 DYNAMIC 暗号
        target_id = GlobalVars.dynamic_config_id if case_data.get("configId") == "DYNAMIC" else case_data["configId"]

        res = self.config_api.delete_config(global_token, target_id)
        self.assert_response(res, expected)

    @allure.story("刷新参数缓存接口")
    def test_refresh_cache(self, global_token):
        """刷新缓存是一个没有任何传参的 DELETE 请求"""
        res = self.config_api.refresh_cache(global_token)
        self.assert_response(res, 200)