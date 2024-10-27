import webview
import os
import shutil
import threading
import requests
import json
import sys
from plyer import notification
import time

'''
作者:y3team
官网:htk.y3team.top
源码采用GNU GPL v3
'''

def show_loading_notification():
    # 显示右下角通知
    notification.notify(
        title="海内存知己，天涯若比邻",
        message="正在加载必要文件。",
        timeout=10,  # 通知显示的时间（秒）
        app_icon="./icon.ico",  # 替换为您的图标文件路径
        app_name="HTK工具箱"  # 替换为您的程序名称
    )

loading_completed = False  # 初始化一个全局变量用于控制加载状态
loading_lock = threading.Lock()  # 创建一个锁用于线程之间的同步

def move_mod_file():
    global loading_completed  # 在这里声明为全局变量
    copy_mod_vanilla_dir = ".\\mod"  
    copy_mod_paste_dir = '.\\resource\\web\\mod'  # 目标目录路径

    try:
        # 检查源目录是否存在
        if not os.path.exists(copy_mod_vanilla_dir):
            raise FileNotFoundError(f"源目录不存在: {copy_mod_vanilla_dir}")

        # 打印调试信息
        print(f"源目录: {copy_mod_vanilla_dir}")
        print(f"目标目录: {copy_mod_paste_dir}")

        # 如果目标目录存在，先删除目标目录中的所有内容
        if os.path.exists(copy_mod_paste_dir):
            print(f"目标目录存在，准备删除: {copy_mod_paste_dir}")
            shutil.rmtree(copy_mod_paste_dir)  # 删除整个目录树
            print("目标目录已删除")

        # 确保目标目录被删除后，再创建目标目录
        os.makedirs(copy_mod_paste_dir)  # 创建目录，包括所有必需的中间目录
        print("目标目录已创建")

        # 复制源目录到目标目录
        shutil.copytree(copy_mod_vanilla_dir, copy_mod_paste_dir, dirs_exist_ok=True)
        print("源目录内容已复制到目标目录")
        
        # 更新标志，表示文件移动完成
        with loading_lock:
            loading_completed = True

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        with loading_lock:
            loading_completed = True  # 设置加载完成的标志

    except Exception as copy_mod_error:
        print(f"发生错误: {copy_mod_error}")
        with loading_lock:
            loading_completed = True  # 设置加载完成的标志

def loading_animation():
    """显示加载动画"""
    print("正在加载，请稍候...")
    while True:
        with loading_lock:
            if loading_completed:
                break
        time.sleep(0.5)  # 模拟加载过程
        print(". ", end="", flush=True)  # 打印加载进度
    print("\n加载完成！")

# 定义本地存储文件路径, 检查用户协议状态
user_agreement_file_path = 'localstorage.json'

def load_localstorage():
    """从文件加载LocalStorage数据"""
    if os.path.exists(user_agreement_file_path):
        try:
            with open(user_agreement_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("加载本地存储时出现JSON解码错误，返回空字典。")
            return {}
        except Exception as e:
            print(f"加载本地存储时发生错误: {e}")
            return {}
    return {}

def save_localstorage(data):
    """将LocalStorage数据保存到文件"""
    try:
        with open(user_agreement_file_path, 'w') as file:
            json.dump(data, file)
        print(f'保存用户协议至 localstorage: {data}')
    except Exception as e:
        print(f"保存用户协议时发生错误: {e}")

# 定义一个函数来获取粉丝数据
def get_follower_data():
    try:
        url = 'https://api.bilibili.com/x/relation/stat?vmid=1215556531'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        print("开始请求粉丝数据...")  # 日志记录请求开始
        bilibili_api_response = requests.get(url, headers=headers)
        bilibili_api_response.raise_for_status()  # 如果响应状态码不是200, 抛出异常

        data = bilibili_api_response.json()  # 解析返回的数据
        print(f"API返回的数据: {data}")  # 打印完整数据

        if 'data' in data and 'follower' in data['data']:
            followers = data['data']['follower']
            print(f"粉丝数量: {followers}")
            # 将数据发送到前端
            webview.windows[0].evaluate_js(f"window.updateFollowerData({json.dumps(data)})")
        else:
            print("返回数据结构不符合预期，无法找到 follower")
            error_message = {"错误代码": -1, "信息": "数据结构不符合预期"}
            webview.windows[0].evaluate_js(f"window.updateFollowerData({json.dumps(error_message)})")
    
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        error_message = {"错误代码": -1, "信息": str(e)}
        webview.windows[0].evaluate_js(f"window.updateFollowerData({json.dumps(error_message)})")
        
    except Exception as e:
        print(f"发生其他错误: {e}")
        error_message = {"错误代码": -1, "信息": str(e)}
        webview.windows[0].evaluate_js(f"window.updateFollowerData({json.dumps(error_message)})")



class Api:
    # 定位绝对位置
    def __init__(self, base_path):
        self.base_path = base_path

    def list_json_files(self):
        """列出目录下的所有 JSON 文件"""
        jsondata_path = os.path.join(self.base_path, 'resource', 'web', 'mod', 'jsondata')
        try:
            json_files = [f for f in os.listdir(jsondata_path) if f.endswith('.json')]
            return json_files
        except FileNotFoundError:
            print(f"JSON 数据目录不存在: {jsondata_path}")
            return []
        except Exception as e:
            print(f"读取JSON数据目录时发生错误: {e}")
            return []

    def get_json_data(self, file_name):
        json_file_path = os.path.join(self.base_path, 'resource', 'web', 'mod', 'jsondata', file_name)
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return "文件未找到"
        except json.JSONDecodeError:
            return "JSON 解码错误"
        except Exception as e:
            return f"发生其他错误: {e}"

    def get_localstorage(self):
        """获取LocalStorage数据"""
        print('加载localStorage数据...')
        return load_localstorage()

    def set_localstorage(self, data):
        """保存LocalStorage数据"""
        print(f'设置localStorage数据: {data}')
        save_localstorage(data)

    def save_localstorage_to_file(self, data_str):
        """保存LocalStorage数据到文件"""
        print(f'保存localStorage数据到文件: {data_str}')
        try:
            data = json.loads(data_str)
            save_localstorage(data)
        except json.JSONDecodeError:
            print("保存本地存储时出现JSON解码错误。")
        except Exception as e:
            print(f"保存本地存储时发生其他错误: {e}")

def start_webview():
    """启动webview窗口"""
    base_path = os.getcwd()  # 使用当前工作目录
    relative_path = os.path.abspath(os.path.join(base_path, 'resource', 'web', 'index.html'))

    try:
        # 创建窗口，并将 Api 实例传递给 js_api
        window = webview.create_window(
            'HyperToolkits GUI', 
            relative_path, 
            js_api=Api(base_path), min_size=(700, 300)
        )
        
        webview.start(debug=True)

    except Exception as e:
        print(f"启动webview窗口时发生错误: {e}")

def main():
    show_loading_notification()  # 显示加载通知
    try:
        global loading_completed

        # 创建并启动加载动画线程
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        
        # 创建并启动文件移动线程
        move_thread = threading.Thread(target=move_mod_file)
        move_thread.start()
        
        # 等待文件移动完成
        move_thread.join()  # 在主线程中等待文件移动完成
        
        with loading_lock:
            loading_completed = True  # 设置加载完成的标志
        
        # 调用获取粉丝数据
        get_follower_data()  # 这里调用获取粉丝数据方法
        
        start_webview()  # 启动 webview 窗口

    except Exception as e:
        print(f"程序发生错误: {e}")
        input("按任意键退出...")  # 暂停以查看错误



if __name__ == '__main__':
    main()
