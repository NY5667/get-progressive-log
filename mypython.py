import requests
import time
import json
import sys
from api_utils import get_token, delete_user_by_ids, get_pregressive_log, get_online_users

config_file = "configurations.json"

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
    return [config for config in configurations if config['valid']]

def init_token():
    """
    这个函数用于初始化ticket授权。
    
    参数:

    返回:

    """
    for config in configurations:
        name = config['name']
        baseUrl = config['baseUrl']
        username = config['username']
        password = config['password']
        print(f"获取该配置项的token:{config['name']}：")
        # config["token"] = get_token(name, baseUrl, username, password)
        token_data = get_token(name, baseUrl, username, password)
        
        # 处理报错相关字段
        print(token_data)
        if 'error' in token_data:
            print(token_data)
            print()
            print(f"Configuration: {name} - The 'error' field exists.")
            print()
            return
        config["token"] = token_data.get("ticket")
        

def run_task():
    """
    这个函数用于运行调度任务。
    
    参数:

    返回:
    string: 配置文件数组。
    """
    while True:
        for config in configurations:
            name = config['name']
            baseUrlMs = config['baseUrlMs']
            token = config["token"]
            progressive_log = get_pregressive_log(name, baseUrlMs, token)
            
            # 处理报错返回结果
            if 'error' in progressive_log:
                print()
                print(f"Configuration: {name} - The 'error' field exists.")
                print()
                continue

            point = progressive_log["data"]["point"]
            message = progressive_log["data"]["message"]
            print(message)
            print()

            if point == 100:
                print(f"Configuration: {name} - Point is 100 - Success!")
            else:
                print(f"Configuration: {name} - Point: {point}")
            print()
        time.sleep(5)  # Pause for 5 seconds before checking again

def exit_user():
    """
    这个函数用于登出用户。

    参数:

    返回:
    string: 配置文件数组。
    """
    for config in configurations:
        baseUrl = config['baseUrl']
        token = config["token"]
        get_online_users_and_delete(baseUrl, token)

def get_online_users_and_delete(base_url, token):
    """
    这个函数用于查询登录用户，并强制登出用户。

    参数:
    base_url   (string):         平台的ip和端口相关配置项。
    token      (string):         用于调用接口时的授权验证。

    返回:
    
    """
    get_online_users(base_url, token)
    print('获取实时在线用户')
    print(data)

    if response.status_code == 200:
        online_id_array = []
        for item in data["list"]:
            print("id:", item["id"])
            online_id_array.append(item["id"])
        online_id_str = ",".join(str(element) for element in online_id_array)
        delete_user_by_ids(base_url, token, online_id_str)
        
    else:
        print("Error:", response.status_code)

configurations = read_configurations()

# 获取命令行参数
args = sys.argv[1:]

# 获取授权
init_token()

# 判断参数并执行相应操作或强制退出
if "-run" in args:
    run_task()
    # 执行脚本的逻辑代码

elif "-exit" in args:
    exit_user()

else:
    print("未提供有效参数")