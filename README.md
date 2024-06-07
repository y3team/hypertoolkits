
# HTK工具箱使用说明书
版本V1.0.04 更新于2024-5-26 作者:y3team
## 本程序是基于python编写的工具脚本
1.[点击跳转软件官网](https://www.hypertools.com.cn)<br>
2.[点击跳转源代码开源网站](https://github.com/y3team/hypertoolskit)<br>
3.本应用完全免费，不会收取您的任何费用<br>
4.本应用只会在官网和B站发布。并使用蓝奏云/123网盘链接，请认准正版，避免您的数据遭到侵害！<br>
5.本应用不存在任何广告<br>
6.本应用开源采用GPL 3.0协议<br>
7.预览版如果有BUG，请反馈至y3team@outlook.com,up是学生，可能不能及时处理您的日志！<br>
祝您使用愉快！

> v1.0.04预览版更新内容：
* 增加拖拽文件打开查看基本信息和sha-256
* 整理代码逻辑
* 修复已知问题
* [软件下载](https://resource.hypertools.com.cn/htk/htk-setup-1.0.04.exe)

> v1.0.03预览版更新内容：
* 增加hwid查询
* 整理代码逻辑
* 增加开机自启动功能
* 改进了更新功能

> v1.0.02-fix预览版更新内容：
* 提高运行安全性
* 修复已知可解决BUG
* 改善程序逻辑性
* 改善更新系统机制

> v1.0.02预览版更新内容：
* 增加hosts(增加/删去/修改)功能
* 优化了DNS服务器修改功能
* 解决了修改DNS服务器时的报毒问题
* <b>因版本存在缺陷，不提供下载渠道</b>

> v1.0.01预览版内容：
* 增加修改DNS服务器功能
* 初版更新模块上线
* <b>因版本存在缺陷，不提供下载渠道</b>

## 我们如何保护您使用本软件的安全
* 打开软件自动从官网查询版本号和最新版本的哈希值(sha-256)
* 通过SSL协议下载更新文件并通过验证哈希值(sha-256)来确保您的更新包是完整的且没有被篡改
* 开源，在著名开源平台Github上上传了源代码(无删改)

> 部分代码展示
```python
def change_dns(interface_alias, primary_dns, secondary_dns):
    # 构建 PowerShell 命令
    ps_command = f'Set-DnsClientServerAddress -InterfaceAlias "{interface_alias}" -ServerAddresses {primary_dns},{secondary_dns}'
    
    # 执行 PowerShell 命令
    try:
        subprocess.run(["powershell", "-Command", ps_command], check=True)
        print(f"DNS服务器成功更改为: {primary_dns}, {secondary_dns}。")
    except subprocess.CalledProcessError as e:
        print(f"更改DNS服务器失败: {e}")
```
## 关于日志
* 日志是开发者开发必要的辅助文件。主要用于BUG修复和版本调试。一般情况下，本软件不会上传任何本地日志。后续会开放日志上传通道，用于BUG漏洞反馈。

## 源代码编译(Python编写版本)
```
pyinstaller index.py -i logo.ico --name=htk --uac-admin --onefile
pyinstaller upgrade.py -i logo.ico --name=upgrade --uac-admin --onefile
```
## 如何联系我们
* 通过邮件：team@hypertools.com.cn
* 通过QQ用户群：318483304 [加入链接](https://qm.qq.com/q/NoCSaxyZs4)

## 如何加入我们
* 通过QQ用户群：318483304 [加入链接](https://qm.qq.com/q/NoCSaxyZs4)，联系群主询问
* 通过发送邮件给team@hypertools.com.cn进行询问

