import requests

def get_token(base_url, username, password):
    """
    这个函数用于获取token用于接口授权请求。

    参数:
    base_url (string): 网站部署地址。
    username (string): 登录的用户名。
    password (string): 登录的密码。

    返回:
    string: 授权的ticket。
    """
    url = f"{base_url}/inter-api/auth/login"
    params = {
        "password": password,
        "userName": username,
        "forceLogin": False
    }
    response = requests.post(url, json=params)
    data = response.json()
    return data

def get_pregressive_log(base_url_ms, token):
    """
    这个函数用于获取服务启动状态。

    参数:
    base_url_ms  (string):         平台的msService，是nginx反向代理出来的。
    token      (string):         用于调用接口时的授权验证。

    返回:
    string: 授权的ticket。
    """
    url = base_url_ms + "/servicemanager/msModule/getProgressiveLog"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    data = response.json()
    return data

def get_online_users(base_url, token):
    """
    这个函数用于查询登录用户，并强制登出用户。

    参数:
    base_url   (string):         平台的ip和端口相关配置项。
    token      (string):         用于调用接口时的授权验证。

    返回:
    
    """
    url = f"{base_url}/inter-api/auth/v1/online-user?current=1&pageSize=200"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def delete_user_by_ids(base_url, token, ids):
    """
    这个函数用于强制登出用户。

    参数:
    base_url   (string):         平台的ip和端口相关配置项。
    token      (string):         用于调用接口时的授权验证。

    返回:
    
    """
    url = f"{base_url}/inter-api/auth/v1/online-user"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": ids
    }

    response = requests.delete(url, headers=headers, params=params)

    if response.status_code == 200:
        print("Delete request successful.")
    else:
        print("Error:", response.status_code)