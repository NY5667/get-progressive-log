import json
from api.api_utils import get_token

def read_configurations():
    """
    这个函数用于获取配置文件。

    参数:

    返回:
    string: 配置文件数组。
    """
    config_file = "configurations.json"
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

def init_token(configurations):
    """
    这个函数用于初始化ticket授权。
    
    参数:

    返回:    配置项

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
        print('token:')
        print(config["token"])
    return configurations

def get_config():
    """
    这个函数对外调用获取 配置项，并且会把授权也放进来。
    
    参数:

    返回:

    """
    configurations = read_configurations()
    # 获取授权
    return init_token(configurations)