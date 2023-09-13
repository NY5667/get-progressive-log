import time
from api.api_utils import get_pregressive_log
from config.config_utils import get_config

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
            base_url_ms = config['base_url_ms']
            token = config["token"]
            progressive_log = get_pregressive_log(base_url_ms, token)
            
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

configurations = get_config()

run_task()