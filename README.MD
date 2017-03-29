

# [JxnuGo淘二手](http://www.jxnugo.com)

![jxnugo_logo](http://oj387fyvl.bkt.clouddn.com/jxnugo-logo.png)
江西师范大学二手物品信息交流应用

## 简介
JxnuGo为解决每年毕业季来临,大量的二手物品信息交流不对称的问题开发。项目包含
web端和移动端,于2016年6月正式上线。后端基于Python Flask框架，数据库采用Mysql，图片存储于七牛云，部署于阿里云ECS。


目前包含JxnuGo淘二手项目浏览地址为:

* web端主页: [www.jxnugo.com](http://www.jxnugo.com)
* Android项目仓库:[https://github.com/zpauly/jxnugo-Android](https://github.com/zpauly/jxnugo-Android)
* 师大+(集成了JxnuGo淘二手)项目地址:[https://github.com/MummyDing/Awesome-Campus](https://github.com/MummyDing/Awesome-Campus)

## 关于
[关于JxnoGo淘二手](http://www.jxnugo.com/about_us)

## 技术要点
* 使用jinja2模板引擎，增强前端代码复用。
* 使用MVC设计模式，解耦后端代码，灵活使用第三方库拓展应用功能。
* 基于Restful API设计原则，给多个移动端单独设计应用接口。
* 设计爬虫爬取学校教务系统学生信息，用于用户信息验证。
* 使用Nginx+supervisor+gunicorn+virtualenv进行服务器部署。

## 联系
如果系统有疑问，请联系ddragonever@gmail.com
