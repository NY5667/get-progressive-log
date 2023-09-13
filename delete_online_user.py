from config.config_utils import get_config
from api.api_utils import delete_user_by_ids, get_online_users

def exit_user():
    """
    这个函数用于登出用户。

    参数:

    返回:
    string: 配置文件数组。
    """
    for config in configurations:
        base_url = config['base_url']
        token = config["token"]
        get_online_users_and_delete(base_url, token)


def get_online_users_and_delete(base_url, token):
    """
    这个函数用于查询登录用户，并强制登出用户。

    参数:
    base_url   (string):         平台的ip和端口相关配置项。
    token      (string):         用于调用接口时的授权验证。

    返回:
    
    """
    data = get_online_users(base_url, token)
    print('获取实时在线用户')
    print(data)

    online_id_array = []
    for item in data["list"]:
        print("id:", item["id"])
        online_id_array.append(item["id"])
    online_id_str = ",".join(str(element) for element in online_id_array)
    delete_user_by_ids(base_url, token, online_id_str)

# 获取配置信息
configurations = get_config()

# 登出用户
exit_user()