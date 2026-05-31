# common/request_util.py
import requests


class RequestUtil:
    # 建立一个全局的 requests 会话，比普通的 requests.get 更快、更稳定
    session = requests.session()

    def send_request(self, method, url, **kwargs):
        """
        发送请求方法
        """
        print(f"\n========== 开始发送请求: {method.upper()} ==========")
        print(f"请求地址: {url}")

        # 提取参数打印出来
        if "params" in kwargs:
            print(f" URL参数: {kwargs['params']}")
        if "json" in kwargs:
            print(f" Body数据: {kwargs['json']}")

        try:
            # 调用底层的 requests.request 发送网络请求
            res = self.session.request(method, url, timeout=10, **kwargs)

            # 3.响应体
            print(f"响应状态码: {res.status_code}")
            print(f"响应内容: {res.text}")
            print("===================================================\n")

            return res

        except Exception as e:
            # 4. 全局异常兜底：一旦网络断了、超时了，不会直接报错死机，而是拦截
            print(f"警告：接口请求发生异常崩溃 -> {e}")
            print("===================================================\n")
            raise e