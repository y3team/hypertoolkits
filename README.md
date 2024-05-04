# HTK工具箱使用说明书

## 本程序基于python编写的工具脚本
<p>
1.[点击跳转官网](https://www.hypertools.com.cn)
2.本应用完全免费，不会收取您的任何费用<br>
3.本应用只会在官网和B站发布。并使用蓝奏云/123网盘链接，请认准正版，避免您的数据遭到侵害！<br>
4.本应用不存在任何广告<br>
5.本应用开源采用GPL 3.0协议<br>
6.预览版如果有BUG，请反馈至y3team@outlook.com,up是学生，可能不能及时处理您的日志！<br>
祝您使用愉快！

> v1.0.02-fix预览版更新内容：
* 提高运行安全性
* 修复已知可解决BUG
* 改善程序逻辑性
* 改善更新系统机制

> v1.0.02预览版更新内容：
* 增加hosts(增加/删去/修改)功能
* 优化了DNS服务器修改功能
* 解决了修改DNS服务器时的报毒问题

> v1.0.01预览版内容：
* 增加修改DNS服务器功能
* 初版更新模块上线

## 编译

```
pyinstaller index.py -i logo.ico --name=htk --uac-admin --onefile
pyinstaller upgrade.py -i logo.ico --name=upgrade --uac-admin --onefile
```
