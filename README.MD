## 搭建本地开发环境

```
pip install -r requirements/develop.txt
cp config/config_sample.py config/config.py
vim config/config.py  # 编辑config/config.py or 找其他同学要一份复制
python manage.py runserver
```


## 天机不可泄露......

数据伪造:

```
#数据库更新后，先删除旧数据表,然后在shell里执行
db.create_all()
User.generate_fake(100)  #伪造用户
Post.generate_fake(100)  #伪造帖子
```