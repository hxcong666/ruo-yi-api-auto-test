import requests

# ==========================================
# 第一步：去前台拿房卡（登录获取 Token）
# ==========================================
login_url = "http://localhost:8080/login"
payload = {
    "username": "admin",
    "password": "admin123"
}

print("1. 正在向服务器发送登录请求...")
res_login = requests.post(url=login_url, json=payload, timeout=5)
login_data = res_login.json()

# 从返回的 JSON 字典里，把 token 的值单独提取出来
token = login_data.get("token")
print(f"✅ 成功拿到房卡！Token前十位: {token[:10]}...\n")


# ==========================================
# 第二步：把房卡挂在脖子上（构造鉴权 Headers）
# ==========================================
# ⚠️ 核心考点：若依的 Token 必须带 'Bearer ' 前缀（注意有个空格）
headers = {
    "Authorization": "Bearer " + token
}


# ==========================================
# 第三步：开门进房间（请求受保护的业务接口）
# ==========================================
# 我们去请求若依自带的获取当前用户信息的接口：/getInfo
info_url = "http://localhost:8080/getInfo"

print("2. 正在带着房卡，尝试访问受保护的房间(/getInfo)...")
# 注意：这是一个 GET 请求，且必须带上刚才组装好的 headers
res_info = requests.get(url=info_url, headers=headers, timeout=5)

print("\n3. 房间(服务器)放行！返回的最终数据：")
print(res_info.json())