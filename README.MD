## 搭建本地开发环境

```
pip install -r requirements/develop.txt
cp config/config_sample.py config/config.py
vim config/config.py  # 编辑config/config.py or 找其他同学要一份复制
python manage.py runserver
```


数据伪造:

```
##数据库更新后，先删除旧数据表,然后在shell里执行
db.create_all()
Role.insert_roles()      #增加角色
User.generate_fake(100)  #伪造用户
Post.generate_fake(100)  #伪造交易帖子
```


restful api约定

```
domain/api/get_token         #登陆账号,获取token  首部添加账号和密码
domain/api/get_mobile_key    #获取七牛云上传key
domain/api/get_mobile_token  #获取七牛云上传的token
domain/api/get_upload_token  #调试  同时获取token和key

```

