import os
import urllib.request
import sys
import ssl
import wmi
print("Hyper Tools Kits 1.1pre2 当前为预览版,可能存在bug")

check_directory = "tempfile"#检查tempfile目录是否存在
if not os.path.exists(check_directory):
    try:
        os.makedirs(check_directory)
        print(f"Debug:检测到没有tempfile目录,目录'{check_directory}'已成功创建")
        pass
    except Exception as directory_Error:
        print(f"Error[已保存到日志]:检测到没有tempfile目录,但失败创建目录'{check_directory}': {directory_Error}")
        
else:
    print(f"Debug:目录'{check_directory}'存在")
    pass

check_file = "./tempfile/api.txt"#检测api.txt是否提前存在
if os.path.exists(check_file):
    print("Debug:api.txt已存在,进行删除")
    if os.path.exists(check_file):
        os.remove(check_file)
        print("Debug:文件成功删除,进行下一步操作")
        pass
    else:
        print("Error[已保存到日志]:删除api文件失败")
        
else:
    pass

print("Debug:正在通过ssl协议从官网下载api文件")
# 定义下载文件的 URL
download_api_url = 'https://www.hypertools.com.cn/api/version.txt'
# 定义保存文件的本地路径
api_filename_path = './tempfile/api.txt'
# 创建 SSLContext 对象，用于配置 SSL 验证选项
ssl_context = ssl.create_default_context()
# 设置 SSLContext 对象的验证模式为必须验证
ssl_context.verify_mode = ssl.CERT_REQUIRED
# 设置 SSLContext 对象的主机名验证选项为启用
ssl_context.check_hostname = True
try:
    # 使用 urllib.request.urlretrieve 下载文件，并传入 SSLContext 对象进行 SSL 证书验证
    with urllib.request.urlopen(download_api_url, context=ssl_context) as response, open(api_filename_path, 'wb') as out_file:
        # 读取响应内容并保存到本地文件
        out_file.write(response.read())
    print("Debug:api文件通过 SSL 证书验证下载成功！")
    pass
except Exception as ssl_api_download_Error:
    print(f"Error:api文件在下载过程中发生错误:{ssl_api_download_Error}")
    sys.exit()

saving_api = "./tempfile/api.txt"#读取api
try:
    with open(saving_api, 'r', encoding='utf-8') as file:
        api_verb = file.readline().strip() 
        print("Debug:api文件成功读取")
        pass
except FileNotFoundError:
    print("Error[已保存到日志]:文件不存在(0.00001%遇到这个Error[已保存到日志]=)")
    sys.exit()
except Exception as read_api_Error:
    print("Error[已保存到日志]:打开文件时发生了错误", read_api_Error)
    sys.exit()

if int(api_verb) ==1001:#检测版本
    print("Debug:您的程序是最新版本,正在启动！")
    os.remove(saving_api)
    pass
elif int(api_verb) >1001:
    print("Debug:当前版本不是最新版本")
    update_require = str(input("当前存在新版本，是否更新(请输入Y/N):"))
    if update_require=="Y":
        upgrade_path = "upgrade.py"  # 替换为你的应用程序路径
        try:
            # 使用 os.system() 打开应用程序
            os.system(upgrade_path)
            print("Debug:应用程序已成功打开！")
            sys.exit()
        except Exception as upgrade_app_Error:
            print("Error:打开应用程序时出现错误：", upgrade_app_Error)
            sys.exit()
    elif update_require=="N":
        pass
    else:
        print("无效的指令")
else:
    print("Error[已保存到日志]:遇到未知错误,请发送日志到y3team@outlook.com")
    sys.exit()
    
program_directory = os.getcwd()

def change_dns(dns_1, dns_2):#运用wmi模块修改dns
    # 创建 WMI 对象
    change_dns_u = wmi.WMI()
    try:
        # 获取所有启用的网络适配器配置
        adapters = change_dns_u.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        # 逐一尝试设置 DNS
        for adapter in adapters:
            # 设置 DNS 服务器搜索顺序
            result = adapter.SetDNSServerSearchOrder(DNSServerSearchOrder=[dns_1, dns_2])

            # 检查结果
            if result[0] == 0:
                print(f"DNS 服务器地址成功设置为: {dns_1} 和 {dns_2} 在适配器 {adapter.Description}")
            else:
                print(f"修改 DNS 失败: {result[0]} - {adapter.Description}")
    except Exception as change_dns_Error:
        print(f"发生错误: {change_dns_Error}")
    
def change_hosts(hosts_action, hosts_domain, hosts_ip, hosts_path='C:/Windows/System32/drivers/etc/hosts'):
    # 确保具有足够权限
    if not os.access(hosts_path, os.W_OK):
        raise PermissionError("没有足够的权限修改 hosts 文件。请以管理员权限运行此脚本。")

    # 读取 hosts 文件内容
    with open(hosts_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        if hosts_action == '增加':
            # 添加新的域名到 hosts_ip 映射
            add_try = f"{hosts_ip}\t{hosts_domain}\n"
            if add_try not in lines:
                file.write(add_try)
                print("已添加")
        elif hosts_action == '删除':
            # 删除指定的域名到 hosts_ip 映射
            for line in lines:
                if hosts_domain not in line:
                    file.write(line)
                    print("已删除")
        elif hosts_action == '修改':
            # 更新现有映射
            hosts_updated = False
            for line in lines:
                if hosts_domain in line:
                    file.write(f"{hosts_ip}\t{hosts_domain}\n")
                    print("成功修改")
                    hosts_updated = True
                else:
                    file.write(line)
            if not hosts_updated:  # 如果不存在，就添加
                file.write(f"{hosts_ip}\t{hosts_domain}\n")
                print("成功修改")
        elif hosts_action == "清除所有记录":
            hosts_remove_check = str(input("二次确认:是否确定清除所有hosts记录?(请输入Y/N)"))
            if hosts_remove_check =="Y":
                file.truncate()  # 删除文件中剩余的内容
                print("成功清除所有hosts记录")
            elif hosts_remove_check =="N":
                print("已取消本次操作")
            else:
                print("无效的指令")
        else:
            print("无效的指令")
        
while True:#主要程序
    print("""
==========HTK工具包=============
(1)更改dns     (2)修改hosts  
(exit)退出     (upgrade)检测更新
================================     
          """)
    get_command = str(input("main>>>"))
    if get_command=="1":#修改DNS,调用前面的change_dns
        dns_1 = str(input("请输入主DNS(如114.114.114.114):"))
        dns_2 = str(input("请输入备用DNS(如8.8.8.8):"))
        change_dns(dns_1,dns_2)
        continue
    elif get_command=="2":
        hosts_1 = str(input("请输入您需要执行的操作(增加/删除/修改/清除所有记录):"))
        hosts_2 = str(input("请输入要执行的域名(清除所有记录请回车):"))
        hosts_3 = str(input("请输入要执行的域名ip地址(清除所有记录请回车):"))
        change_hosts(hosts_1,hosts_2,hosts_3)
    elif get_command=="upgrade":
        update_check = str(input("二次确认：确定更新?(请输入Y/N)"))
        if update_check=="Y":
            upgrade_path = "upgrade.py"  # 替换为你的应用程序路径
            try:
                # 使用 os.system() 打开应用程序
                os.system(upgrade_path)
                print("Debug:应用程序已成功打开！")
                sys.exit()
            except Exception as upgrade_app_Error:
                print("Error:打开应用程序时出现错误：", upgrade_app_Error)
                sys.exit()
        elif update_check=="N":
            pass
        else:
            print("无效的指令")
        
    elif get_command=="exit":#退出
        break
    else:
        print("无效的指令")
print("感谢您的使用,按Enter退出程序") 
input("Designed by y3team · HTK 1.1 pre1")