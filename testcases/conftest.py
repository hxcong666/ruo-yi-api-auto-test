import pytest
from api.login_api import LoginAPI


@pytest.fixture(scope="session")
def global_token():
    """
    全局前置：全自动登录并提取 Token
    """
    print("\n============== [全局前置] 正在全自动获取系统最高权限... ==============")

    # 1. 实例化登录武器
    login_api = LoginAPI()

    # 2. 发送登录请求
    # 验证码和uuid传空即可（前提是后端配置已关闭验证码）
    res = login_api.login(username="admin", password="admin123", code="", uuid="")

    # 3. 提取 Token 核心逻辑
    res_json = res.json()
    if res_json.get("code") == 200:
        # 从响应体中抠出 token
        token = res_json.get("token")
        print(f"已获取动态 Token: {token[:20]}......")

        # 4. 把 Token 发放给所有测试用例
        yield token

    else:
        print(f"提权失败！原因: {res.text}")
        raise Exception("登录失败，自动化测试中止！请检查账号密码或验证码配置。")

    print("\n============== [全局后置] 接口全部测试完毕，正在清理战场... ==============")