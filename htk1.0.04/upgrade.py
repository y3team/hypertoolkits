import sys
import urllib.request
import os
import ssl
import time
import hashlib

class LogWriter:
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def create_directory(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Debug:检测到没有{directory}目录，目录'{directory}'已成功创建")
        except Exception as directory_error:
            print(f"Error[已保存到日志]:检测到没有{directory}目录，但失败创建目录'{directory}': {directory_error}")
    else:
        print(f"Debug:目录'{directory}'存在")

def delete_file(file_path):
    if os.path.exists(file_path):
        print(f"Debug:{file_path}已存在，进行删除")
        try:
            os.remove(file_path)
            print("Debug:文件成功删除，进行下一步操作")
        except Exception as delete_error:
            print(f"Error[已保存到日志]:删除文件失败: {delete_error}")

def download_file(url, local_path, ssl_context):
    try:
        with urllib.request.urlopen(url, context=ssl_context) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Debug:文件通过 SSL 证书验证下载成功: {local_path}")
    except Exception as download_error:
        print(f"Error:文件在下载过程中发生错误: {download_error}")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        print("Debug:文件成功读取")
        return [line.strip() for line in lines]
    except FileNotFoundError:
        print("Error[已保存到日志]:文件不存在")
    except Exception as read_error:
        print("Error[已保存到日志]:打开文件时发生了错误", read_error)

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def move_file(source_path, destination_path):
    try:
        os.rename(source_path, destination_path)
        print(f"文件成功从 {source_path} 移动到 {destination_path}")
        upgrade_path = ".\\htk.exe"
        try:
            os.system(upgrade_path)
            print("Debug:应用程序已成功打开！")
            sys.exit()
        except Exception as upgrade_app_error:
            print("Error:打开应用程序时出现错误：", upgrade_app_error)
    except Exception as move_error:
        print(f"移动文件时发生错误: {move_error}")

def main():
    sys.stdout = LogWriter(f"upgrade-log-{time.strftime('%Y%m%d-%H%M%S', time.localtime())}.txt")

    check_directory = "tempfile"
    create_directory(check_directory)

    check_file = ".\\tempfile\\api.txt"
    delete_file(check_file)

    print("Debug:正在通过 SSL 协议从官网下载 api 文件")
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True
        download_file('https://www.hypertools.com.cn/api/version.txt', '.\\tempfile\\api.txt', ssl_context)

        api_info = read_file(check_file)
        api_verb, sha256_str = api_info[0], api_info[1]

        print("Debug:正在验证下载文件的 SHA-256 值")
        update_file_path = ".\\htk.exe"
        if os.path.exists(update_file_path):
            sha256_value = calculate_sha256(update_file_path)
            if sha256_str == sha256_value:
                print("Debug:当前程序已经是最高版本了")
                upgrade_path = ".\\htk.exe"
                try:
                    os.system(upgrade_path)
                    print("Debug:应用程序已成功打开！")
                    sys.exit()
                except Exception as upgrade_app_error:
                    print("Error:打开应用程序时出现错误：", upgrade_app_error)
            else:
                print("Debug:官网更新程序 SHA-256 值为:", sha256_str)
                print("Debug:您的更新程序不是最新版本:", sha256_value)
                os.remove(update_file_path)
        else:
            print("Error:文件不存在:", update_file_path)

        print("Debug:正在通过 SSL 协议从官网下载更新文件")
        download_file('https://www.hypertools.com.cn/api/htk.exe', '.\\tempfile\\htk.exe', ssl_context)

        update_file_path = ".\\tempfile\\htk.exe"
        sha256_value = calculate_sha256(update_file_path)
        print("Debug:正在验证下载文件的 SHA-256 值")
        if sha256_str == sha256_value:
            print("Debug:已验证完毕更新程序")
        else:
            print("Debug:官网更新程序 SHA-256 值为:", sha256_str)
            print("Error:您的更新程序疑似遭到篡改:", sha256_value)
            os.remove(update_file_path)

        print("Debug:原始文件成功删除，进行下一步操作")
        paste_file_path = '.\\htk.exe'
        delete_file(paste_file_path)
        move_file(update_file_path, paste_file_path)
    except Exception as upgrade_file_Error:
        print("出现错误:",upgrade_file_Error)
    print("按Enter退出")
    input("")

if __name__ == "__main__":
    main()