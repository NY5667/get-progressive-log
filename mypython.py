import requests
import time
import json

config_file = "configurations.json"

def get_ticket(base_url, username, password):
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
    ticket = data.get("ticket")
    return ticket

def check_response(name, baseUrlMs, bearer_token):
    """
    这个函数用于获取服务启动状态。

    参数:
    name (string):           对应配置的名称。
    baseUrlMs (string):      平台的msService，是nginx反向代理出来的。
    bearer_token (string):   用于调用接口时的授权验证。

    返回:
    string: 授权的ticket。
    """
    url = baseUrlMs + "/servicemanager/msModule/getProgressiveLog"

    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.post(url, headers=headers)
    data = response.json()
    if 'error' in data:
        print()
        print(f"Configuration: {name} - The 'error' field exists.")
        print()
        return

    point = data["data"]["point"]
    message = data["data"]["message"]
    print(message)
    print()

    if point == 100:
        print(f"Configuration: {name} - Point is 100 - Success!")
    else:
        print(f"Configuration: {name} - Point: {point}")
    print()

def read_configurations():
    """
    这个函数用于获取配置文件。

    参数:

    返回:
    string: 配置文件数组。
    """
    with open(config_file) as file:
        configurations = json.load(file)
    for config in configurations:
        if config['valid'] == False:
            continue
        baseUrl = config['baseUrl']
        baseUrlMs = config['baseUrlMs']
        # 替换为正常请求的地址
        baseUrlMs = baseUrlMs.replace("{{baseUrl}}", baseUrl)
        config['baseUrlMs'] = baseUrlMs
    return configurations

configurations = read_configurations()

# 定义一个字符串到字符串的映射
my_token_map = {}

for config in configurations:
    if config['valid'] == False:
        continue
    baseUrl = config['baseUrl']
    username = config['username']
    password = config['password']
    print(f"获取该配置项的ticket:{config['name']}：")
    config["ticket"] = get_ticket(baseUrl, username, password)

while True:
    for config in configurations:
        if config['valid'] == False:
            continue
        name = config['name']
        baseUrlMs = config['baseUrlMs']
        ticket = config["ticket"]
        check_response(name, baseUrlMs, ticket)
    time.sleep(5)  # Pause for 5 seconds before checking again