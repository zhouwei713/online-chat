# online-chat
本项目是一个在线的 IM 系统，打开网页即用，非常方便，项目采用 Flask 搭建。
>这里先给出 Demo 地址，[https://www.luobodazahui.top](https://www.luobodazahui.top)   

# tips
由于本人水平、时间有限，很多辅助功能还没有完成，比如用户管理，权限管理，页面布局等等。项目后续会持续更新，
不断的完善各项功能。

同时当前的数据初始化工作也是使用比较简单粗暴的处理方式，后续会着重修复。

# 整体效果
登陆页面

![1.png](https://i.loli.net/2019/07/18/5d30206a2d8e916608.png)
>项目整体前端采用的是 bootstrap 框架，这个登陆页面取自模板网站（http://www.bootstrapmb.com/）。

其他辅助页面
>这里其他的辅助页面，由于时间的原因，都还比较粗糙，只能再慢慢搞了。

**登陆后首页**

![2.png](https://i.loli.net/2019/07/18/5d3025a2d5f7b29456.png)
>四个 button，分别对应不同的功能页。

**聊天室列表页面**

![3.png](https://i.loli.net/2019/07/18/5d3026122dc7842005.png)
>可以创建聊天室，也可以加入到已有的聊天室中。

**聊天室**

![4.png](https://i.loli.net/2019/07/18/5d3026f008e8b91057.png)

也可以切换聊天皮肤

![5.png](https://i.loli.net/2019/07/18/5d303bd2e3fbd37095.png)

**聊天室用户管理**

![6.png](https://i.loli.net/2019/07/18/5d303c29118eb48674.png)
>可以做禁言，踢人等操作

# 技术栈
1. flask
2. flask_login
3. redis
4. SQLite
5. flask_socketio

还有些其他技术，不再一一列举。

# 快速部署
1. clone项目到本地```git@github.com:zhouwei713/online-chat.git``` 
2. 运行项目下面 manage.py 文件

# 设计说明
这里罗列了个人开发过程中的思路和方法，供小伙伴们探讨
1. [搭建整体框架](https://mp.weixin.qq.com/s?__biz=MzU5NDcyOTg4MA==&mid=2247484401&idx=1&sn=1e3048eb37b340c355aa3e6090f23195&chksm=fe7d8d06c90a041045ab9077db1d314008e5ba2abbd6772bfe2d8ab6f58574462b6ffafeb957&token=416699675&lang=zh_CN#rd)  
2. [实现即时通讯](https://mp.weixin.qq.com/s?__biz=MzU5NDcyOTg4MA==&mid=2247484409&idx=1&sn=cf5ab9dee87e2b048b3185ae531caaa0&chksm=fe7d8d0ec90a04182b52971e46d12aa3f528650cedf9316b1e6de8727d3a84ae42367fa80e91&token=416699675&lang=zh_CN#rd)
3. [调整项目结构](https://mp.weixin.qq.com/s?__biz=MzU5NDcyOTg4MA==&mid=2247484414&idx=1&sn=00425a51c3c50947b98cf855c7a4ee96&chksm=fe7d8d09c90a041fda112ac1ae9a2dbcd7ed642a610a689b79d93ce6718a938e8d008911afc2&token=416699675&lang=zh_CN#rd)
4. [完善相关功能](https://mp.weixin.qq.com/s?__biz=MzU5NDcyOTg4MA==&mid=2247484425&idx=1&sn=a22149cfb1e7cbe99e595e45fc9276be&chksm=fe7d8afec90a03e86cb5c5cb7e34c1f7e917efcf178fa5f0ec201a6c9ca090a2e88a25215881&token=416699675&lang=zh_CN#rd)
5. [完整版](https://juejin.im/post/5d1deaf55188255d5e4c5bab)

# TODO
1. 用户权限功能完善
2. 项目初始化完善
3. 辅助页面优化
4. 其他

# License
MIT