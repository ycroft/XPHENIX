---
# XPHENIX
---
[![Build Status](https://travis-ci.org/ycroft/XPHENIX.svg?branch=master)](https://travis-ci.org/ycroft/XPHENIX)

* 目标：一个实用的文档管理系统

* 前身是一个结构混乱不可维的商业项目

* 重新搭积木

* 包含自制的简易WEB框架 **ANT**

* 业余作品，欢迎帮忙

---
## ANT
---

目前支持特性：

* 公共：

    * 通用接口适配常用数据库
    * 支持对象关系映射（ORM）
    * 支持进程部署，待部署Task可注册软狗，Monitor自身使用硬狗

* 模板：

    * HTML内容管理，启动加载
    * 动态内容加载
        * 变量替换：
        
        ```
        {{var name}}
        ```
        
        * 列表替换：
        
        ```
        {{sl name}}
        {{ele A}} ... {{ele B}} ... {{ele C}} ...
        {{el}}
        ```
        
        * 分支语句
        
        ```
        {{sw name}}
        {{case A}}
            ...
        {{case B}}
            ...
        {{es}}
        ```

    * HTML支持组合和继承，支持复用HTML

* 访问控制：

    * 基本的HTTP服务器
    * Server作为Task部署，死循环、异常、无响应、启动失败会被Monitor重新创建，保证可靠性
    * 静态的请求分发，统一配置文件配置url和静态资源、服务资源的映射关系

---
## STUB
---

* 桩服务器请至 *source/server/stub* 路径

```bash
python stub_server.py
```

* 可访问 *http://127.0.0.1:8888/doczone/login* 修改代码进行测试和实验

* 桩服务器没有硬狗，不会导致系统重启

---
## UT
---

* 测试开发可移步 *llt/*

```bash
python run_ut.py
```

* 控制台检查结果

---
## 当前
---
* ANT(90%)

* ANT公共组件开发

