#JXNUGO
查看jxnugo Android app[请戳这里](https://github.com/JXNU-ACS/jxnugo-Android)

#快速导航
###搭建本地开发环境

```
pip install -r requirements/develop.txt
cp config/config_sample.py config/config.py
vim config/config.py  # 编辑config/config.py or 找其他同学要一份复制
python manage.py runserver
```

##数据伪造（测试）:

```
##数据库更新后，先删除旧数据表,然后在shell里执行
python manage.py shell
db.drop_all()
db.create_all()
Role.insert_roles()      #增加角色
User.generate_fake(100)  #伪造用户
Post.generate_fake(100)  #伪造交易帖子
```


##restful api约定

* www.jxnugo.com/api/get_token

  描述：登陆账号的时候,获取有效期一个小时的token  在请求首部添加用户账号和密码

  返回类型：json

```
	{
   		 "expiration":" ",
    	 "token":" "
	}
```

* www.jxnugo.com/api/get_mobile_token

  描述：获取七牛云上传的token

  返回类型：json

```
	{
	    "token":" "
	}
```


