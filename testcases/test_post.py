import pytest
import allure
from api.post_api import PostAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars  # 🔴 引入全局记忆中枢


@allure.epic("若依后台管理系统")
@allure.feature("岗位管理模块")
class TestPostManage:
    post_api = PostAPI()

    def assert_response(self, response, expected_code):
        """通用的断言验尸官"""
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("查询岗位列表接口")
    @allure.title("测试查询所有岗位")
    def test_get_post_list(self, global_token):
        res = self.post_api.get_post_list(global_token)
        self.assert_response(res, 200)
        print("\n查询所有岗位测试成功!")

    @allure.story("查询岗位详细接口")
    @allure.title("测试获取单个岗位信息")
    @pytest.mark.parametrize("case_data", read_yaml("data/post_data.yml", "get_post_info_cases"))
    def test_get_post_info(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        target_id = case_data["postId"]
        res = self.post_api.get_post_info(global_token, target_id)
        self.assert_response(res, expected)
        print("\n获取岗位信息测试成功!")

    @allure.story("新增岗位接口")
    @allure.title("测试新增岗位")
    @pytest.mark.parametrize("case_data", read_yaml("data/post_data.yml", "add_post_cases"))
    def test_add_post(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.post_api.add_post(global_token, case_data)
        self.assert_response(res, expected)

        # 🔴 新增成功后，提取动态ID
        if expected == 200:
            target_code = case_data["postCode"]
            query_res = self.post_api.get_post_list(global_token, params={"postCode": target_code})

            json_data = query_res.json()
            records = json_data.get("rows", json_data.get("data", []))

            if records:
                GlobalVars.dynamic_post_id = records[0]["postId"]
                print(f"\n[全链路追踪] 成功提取到新生成的岗位 ID: {GlobalVars.dynamic_post_id}")
        print("\n新增岗位测试成功!")

    @allure.story("修改岗位接口")
    @allure.title("测试修改岗位")
    @pytest.mark.parametrize("case_data", read_yaml("data/post_data.yml", "update_post_cases"))
    def test_update_post(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 🔴 拦截暗号，动态覆盖
        if case_data.get("postId") == "DYNAMIC" and GlobalVars.dynamic_post_id:
            case_data["postId"] = GlobalVars.dynamic_post_id

        res = self.post_api.update_post(global_token, case_data)
        self.assert_response(res, expected)
        print("\n修改岗位测试成功!")

    @allure.story("删除岗位接口")
    @allure.title("测试删除岗位")
    @pytest.mark.parametrize("case_data", read_yaml("data/post_data.yml", "delete_post_cases"))
    def test_delete_post(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 🔴 拦截暗号
        target_id = GlobalVars.dynamic_post_id if case_data.get("postId") == "DYNAMIC" else case_data["postId"]

        res = self.post_api.delete_post(global_token, target_id)
        self.assert_response(res, expected)
        print("\n删除岗位测试成功!")