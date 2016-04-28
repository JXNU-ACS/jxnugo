####天机不可泄露......
数据伪造:

```
#数据库更新后，先删除旧数据表,然后在shell里执行
db.create_all()
User.generate_fake(100)  #伪造用户
Post.generate_fake(100)  #伪造帖子
```