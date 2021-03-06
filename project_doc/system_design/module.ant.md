#模块说明
---
##1 访问控制
---
###1.1 背景
访问控制是整个系统的消息入口和出口，是内部所有模块的对外屏障，也是模板模块和组件模块的“中间人”。它既保障了请求资源的定位，也实现了对静态资源和动态资源的整合和出口。

###1.2 功能概述

####1.2.1 一个TCP服务器
* 封装python标准库中的TCPServer即可，加入多线程mixin，为每个连接创建线程。


####1.2.2 一个HTTP请求处理器
* 仍然可以通过继承使用python的BaseHTTPHandler，处理对应类型的HTTP请求。
* 请求对象的加工：这里需要对外部的请求做一次封装。拥有结构统一的内部对象很重要。
* 下发请求：调用分发器的接口进行请求的下达。


####1.2.3 一个分发/路由者
* 请求的资源定位：将请求映射到具体的模板标识和组件标识。
* 请求的下发：调用模板管理模块和组件管理模块进行模板的拼装收集和动态资源的请求。


####1.2.4 一个合并者
* 对请求返回资源的合法性检查。
* 动态资源和静态资源的融合：将组件返回的动态资源和模板返回的静态资源进行拼装。
* 响应对象的加工和返回，将组合后的结果加工成可以返回的报文，封装并返回。


####1.2.5 一个循环任务触发器
* 负责一些循环任务和定时任务的执行。
* 向组件管理和模板管理下发内部请求并收集状态。


###1.3 特性分析列表
###1.4 类型分析列表
####[类型]CommonRequest
* 公共成员
    + request_type
    + request_args
    + response
* 公共接口
    + write_response(rsp)
    
####[类型]ComponentRequest(CommonRequest)
* 公共成员
    + component_name
* 公共接口
    + write_response(rsp)
    
####[类型]TemplateRequest(CommonRequest)
* 公共成员
    + template_name
* 公共接口
    + write_response(rsp)
    
####[类型]TcpServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer)
* 公共接口
    + \_\_init\_\_(server_config)
    + serve()
    + distroy()

####[类型]RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler)
* 公共成员
    + dist
    + merger
* 公共接口
    + \_\_init\_\_(handler_config)
    + handle_request()

####[类型]InternalTask
* 公共成员
    + task_name
    + request_list
    + result_stack
    + fail_num
    + task_type
    + timer_info
* 公共接口
    + \_\_init\_\_(task_config)
    + push_result(response)
    
####[类型]CyclicTaskManager
* 公共成员
    + task_list
    + cyclic_status
    + dist
* 公共接口
    + \_\_init\_\_(manager_config)
    + start_all_task()
    + reg_task(task_l)
    + rmv_task(task_name)
    + get_status(task_name)

####[类型]Dispatcher
* 公共成员
    + tm_handler
    + tmpl_map
    + cm_handler
    + cmpt_map
* 公共接口
    + \_\_init\_\_(tmpl_conf_f, cmpt_map_f)
    + dispatch(comm_request)

####[类型]SmMerger
* 公共接口
     + merge(tmpl_req, cmpt_req)

###1.5 周边模块关系
---
##2 模板管理
---
###2.1 背景
模板管理是系统中用来管理所有服务器静态资源的模块。这些静态资源主要指可继承的HTML文件（继承的目的和实现见详2.2），还包括CSS文件、JavaScript代码文件、多媒体文件等等。它的存在既是为了分离静态资源，让前端设计成为完全独立的工作，也是为了最大化静态资源的复用率（这里主要指HTML模板）。
###2.2 功能概述

####2.2.1 什么是模板文件
* 模板文件是带有特殊标记的HTML文件。这些特殊标记包括：变量（动态内容）、模板引用、模板关系说明语句等。

####2.2.2 什么是模板的继承和引用
* 模板的一对一继承：为了减少前端代码的冗余，允许对于重复使用的包围式HTML标记块儿进行复合。例如悬浮面板对于整个网站均有效，可以将它作为复用的父模板，需要复用这段代码的模板只需要在文件开始引入父亲模板的名字即可（这里仅考虑一对一关系）。如下面的例子，注意{ac}标记和{from "..."}标记。
~~~html
<html>
    <title>Welcome home!</title>
    <body>
        <div class="fui_upper_fixed">
            <div class="fui_box_search">
                ...
            </div>
            <div class="fui_box_btn_pnl">
                ...
            </div>
            <!--a lot of components here-->
        </div>
        <div class="fui_panel_front">
            <!--main content-->
            {ac}
        </div>
    </body>
</html>
~~~

*子模板A：*
~~~html
{from "base ui"}
<div class="fui_box_news">
    <p>
    ...
</div>
~~~

*子模板B：*
~~~html
{from "base ui"}
<div class="fui_box_comm">
    <p>
    ...
</div>
~~~
* 模板的引用：允许模板引用的目的仍然是提高代码的复用。对于一些重复使用的标记片段，例如按钮、分割线等可以视作公共组件。如下，注意{insert "..."}标签。

*公共组件*
~~~html
<div class="fui_box_comm">
    ...
</div>
<div class="fui_btn_comm">
    ...
</div>
~~~

*模板引用*
~~~html
<div class="fui_panel_comm">
    {insert "icon button"}
</div>
~~~

####2.2.3 什么是模板对象
* 首先，为了支撑继承和引用的特性，每个模板需要一个唯一可标识的名字
* 模板对象是对模板文件的抽象，模板的文本不必常驻内存中，但模板的名字和模板间关系是重要的内涵。设计模板对象的目的就是要对某个模板的身份和其周边关系进行记录，方便管理模块进行搜索和定位。

####2.2.4 模板中的变量
* 为了分离动态内容，模板中需要引用“变量”来占位，这些变量最后会通过访问控制模块的合并功能被服务器动态资源替换。
* 单一变量的标记：{var "..."},例如
~~~html
<div>
Today is {var "date_d"}
</div>
~~~
*  列表变量的组合标记：{sl "..."} ... {ele "..."} ... {el}。被列表语法包括的内容在与服务侧资源合并时会被重复，重复次数是列表长度（由组件返回值决定），ele标记指代列表中的元素，可以有多个。例如
~~~html
<div>NEWS</div>
{sl "notice_list"}
<div class="fui_lst_comm">
    <div class="fui_lst_ele">{ele "date"}</div>
    <div class="fui_lst_ele">{ele "title"}</div>
    <div class="fui_lst_ele">{ele "read_num"}</div>
</div>
{el}
~~~

####2.2.5 标记和检查
* 模板语法检查：检查是否有非法标记，标记的使用方法是否正确。
* 模板关系的检查：检查是否有非法的继承和包含关系。
* 标记的文本级别：标记独立于HTML语句规则，可在HTML文本任意地方使用，解析这些特殊标记时不考虑HTML标记的规则。
* 标记的转义：**单独的"{"和"}"并不属于特殊标记**，标记是完整的语句匹配，如果想不解析这些特殊语句，如显示{ac}，则在HTML文本中书写“{{ac}}”形式即可。
* 语法检查和关系检查称为一致性检查，一般在模板模块初始化时进行，在执行请求时也会进行基本的关系检查。

###2.3 特性分析列表
###2.4 类型分析列表
###2.5 周边模块关系
---
##3 组件管理
---
###3.1 背景
组件可以看作服务器上最小单位的服务提供者，一个组件提供一系列同类型的服务，一个服务器提供的所有服务就是所有组件功能的集合。组件管理模块将用户对动态资源的请求（调用来自访问控制模块）下发到各个组件来收集计算结果。
###3.2 功能概述
###3.3 特性分析列表
###3.4 类型分析列表
###3.5 周边模块关系
---
##4 公共模块列表
---
###4.1 日志模块[rsp_log]
####[类型]Logger
* 描述
    + 文件日志系统
    + 对logging模块的封装
* 公共接口
    + init_logger(conf)
        + 初始化日志模块
        + 输入conf：文件路径、日志规模、默认等级等
    + set_level(lvl)
        + 改变日志等级
        + 等级设置复用logging模块：NOTSET、DEBUG、INFO、WARNING、ERROR、CRITICA
    + log_except(lvl, mod_name, trace_info, fmt_cxt)
        + 用于打印日志
        + 输入：日志等级，模块名称，调用点信息，格式化后字符串，不支持Formatter对象。
        + 日志格式内部固定，不作为输入。
    + compress_check()
        + 检查当前日志文件大小是否超限，超限则压缩打包，并以日期后缀重命名。
    + scan(lvl)
        + 扫描当前日志文件的日志等级计数
        + 输入lvl表示统计lvl以上等级日志
        + 返回数目

