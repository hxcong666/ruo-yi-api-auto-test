import pytest
import allure
from api.dept_api import DeptAPI
from common.yaml_util import read_yaml
from common.global_vars import GlobalVars


@allure.epic("若依后台管理系统")
@allure.feature("部门管理模块")
class TestDeptManage:
    dept_api = DeptAPI()

    def assert_response(self, response, expected_code):
        """通用的断言"""
        assert response.status_code == 200
        assert response.json()["code"] == expected_code

    @allure.story("查询部门接口")
    @allure.title("测试查询部门列表")
    def test_get_dept_list(self, global_token):
        """测试用例1:获取部门列表"""
        res = self.dept_api.get_dept_list(global_token)
        self.assert_response(res, 200)

    @allure.story("新增部门接口")
    @allure.title("测试新增部门")
    @pytest.mark.parametrize("case_data", read_yaml("data/dept_data.yml", "add_dept_cases"))
    def test_add_dept(self, global_token, case_data):
        """测试用例2:新增部门"""
        expected = case_data.pop("expected_code")
        res = self.dept_api.add_dept(global_token, case_data)
        self.assert_response(res, expected)
        #新增成功后提取动态ID
        if expected == 200:
            target_name = case_data["deptName"]
            query_res = self.dept_api.get_dept_list(global_token, params={"deptName": target_name})

            # 兼容处理若依可能存在的 data 或 rows 返回格式
            json_data = query_res.json()
            records = json_data.get("data", json_data.get("rows", []))

            if records:
                GlobalVars.dynamic_dept_id = records[0]["deptId"]
                print(f"\n[全链路追踪] 成功提取到新生成的部门 ID: {GlobalVars.dynamic_dept_id}")

    @allure.story("修改部门接口")
    @allure.title("测试修改部门")
    @pytest.mark.parametrize("case_data", read_yaml("data/dept_data.yml", "update_dept_cases"))
    def test_update_dept(self, global_token, case_data):
        """测试用例3:更新部门"""
        expected = case_data.pop("expected_code")
        if case_data.get("deptId") == "DYNAMIC" and GlobalVars.dynamic_dept_id:
            case_data["deptId"] = GlobalVars.dynamic_dept_id
        res = self.dept_api.update_dept(global_token, case_data)
        self.assert_response(res, expected)

    @allure.story("删除部门接口")
    @allure.title("测试删除部门")
    @pytest.mark.parametrize("case_data", read_yaml("data/dept_data.yml", "delete_dept_cases"))
    def test_delete_dept(self, global_token, case_data):
        """测试用例4:删除部门"""
        expected = case_data.pop("expected_code")
        target_id = GlobalVars.dynamic_dept_id if case_data.get("deptId") == "DYNAMIC" else case_data["deptId"]
        res = self.dept_api.delete_dept(global_token, target_id)
        self.assert_response(res, expected)