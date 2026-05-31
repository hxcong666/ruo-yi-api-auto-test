import pytest
import allure
from api.notice_api import NoticeAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars


@allure.epic("若依后台管理系统")
@allure.feature("公告管理模块")
class TestNoticeManage:
    notice_api = NoticeAPI()

    def assert_response(self, response, expected_code):
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("查询公告列表接口")
    def test_get_notice_list(self, global_token):
        res = self.notice_api.get_notice_list(global_token)
        self.assert_response(res, 200)

    @allure.story("查询公告详细接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "get_info_cases"))
    def test_get_notice_info(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.notice_api.get_notice_info(global_token, case_data["noticeId"])
        self.assert_response(res, expected)

    @allure.story("新增公告接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "add_notice_cases"))
    def test_add_notice(self, global_token, case_data):
        expected = case_data.pop("expected_code")
        res = self.notice_api.add_notice(global_token, case_data)
        self.assert_response(res, expected)

        # 新增成功后，提取动态ID
        if expected == 200:
            target_title = case_data["noticeTitle"]
            query_res = self.notice_api.get_notice_list(global_token, params={"noticeTitle": target_title})

            json_data = query_res.json()
            records = json_data.get("rows", json_data.get("data", []))

            if records:
                GlobalVars.dynamic_notice_id = records[0]["noticeId"]
                print(f"\n[全链路追踪] 成功提取到新生成的公告 ID: {GlobalVars.dynamic_notice_id}")

    @allure.story("修改公告接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "update_notice_cases"))
    def test_update_notice(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 拦截暗号，动态覆盖
        if case_data.get("noticeId") == "DYNAMIC" and GlobalVars.dynamic_notice_id:
            case_data["noticeId"] = GlobalVars.dynamic_notice_id

        res = self.notice_api.update_notice(global_token, case_data)
        self.assert_response(res, expected)

    @allure.story("删除公告接口")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "delete_notice_cases"))
    def test_delete_notice(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        target_id = GlobalVars.dynamic_notice_id if case_data.get("noticeId") == "DYNAMIC" else case_data["noticeId"]

        res = self.notice_api.delete_notice(global_token, target_id)
        self.assert_response(res, expected)

    @allure.story("首页顶部公告列表")
    def test_list_notice_top(self, global_token):
        res = self.notice_api.list_notice_top(global_token)
        self.assert_response(res, 200)

    @allure.story("单条标记公告已读")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "mark_read_cases"))
    def test_mark_notice_read(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 兼容标记已读接口的动态ID测试
        target_id = GlobalVars.dynamic_notice_id if case_data.get("noticeId") == "DYNAMIC" else case_data["noticeId"]

        res = self.notice_api.mark_notice_read(global_token, target_id)
        self.assert_response(res, expected)

    @allure.story("批量标记公告已读")
    @pytest.mark.parametrize("case_data", read_yaml("data/notice_data.yml", "mark_read_all_cases"))
    def test_mark_notice_read_all(self, global_token, case_data):
        expected = case_data.pop("expected_code")

        # 兼容批量标记接口（如果用例里传了 DYNAMIC，则转为字符串处理）
        target_ids = str(GlobalVars.dynamic_notice_id) if case_data.get("ids") == "DYNAMIC" else case_data["ids"]

        res = self.notice_api.mark_notice_read_all(global_token, target_ids)
        self.assert_response(res, expected)

    @allure.story("查询公告已读用户列表")
    def test_list_notice_read_users(self, global_token):
        res = self.notice_api.list_notice_read_users(global_token)
        self.assert_response(res, 200)