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

###登录注册与token
#####用户登录  【GET】       {此api已实现}
* URL:  www.jxnugo.com/api/get_token
* 描述：用来用户登录验证
* 参数：userName,passWord
* 请求成功返回值：

	```
  {
		"expiration"3600,
		"token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2MjkwMTM1MSwiaWF0IjoxNDYyODk3NzUxfQ.eyJpZCI6NX0.zsYFk7rzBi68TIY3PWe_8jwjsvPTghrM80RjeyDQd1k"
  }
	```
* 请求失败情况
  返回：

  ```
  {
  		"error": "unauthorized",
  		"message": "Invalid credentidls"

  }
  ```
* 说明：

	expiration： token的有效期，默认一个小时

	token：加密的签名

	error：错误信息

	message：具体错误信息

#####用户注册	【POST】
* URL: www.jxnugo.com/api/register
* 上传到服务器的信息：

```
	{
		"userName":"",
		"userEmail":"",
		"password":""
	}

```
* 备注：客户端先对数据进行验证再上传

#####请求七牛云上传token  【GET】   {此api已实现}
* URL: www.jxnugo.com/api/get_mobile_token

* 描述：获取七牛云上传的token
* 参数：无
* 请求成功返回值：


	```
	{
  		"uptoken": "BK58FryE-_YddhrnjmpS_phqj3vKrR3k-svdydGB:QFEv3as8vr9qug7eH3qlluADmzw=:eyJzY29wZSI6InRyYWRlIiwiZGVhZGxpbmUiOjE0NjI5MDEyOTF9"
}
	```


###帖子相关

#####获取一个页面的帖子的信息   【GET】  {此api已实现}
* URL: www.jxnugo.com/api/posts
* 描述：获取固定数量(可指定数量)的帖子信息
* 请求成功返回值：

```
	{
	"count":"100",
	"next":"http://127.0.0.1:5000/api/posts?page=3",
	“prev”:"http://127.0.0.1:5000/api/posts?page=1",
  "posts": [
    {
      "author": "http://127.0.0.1:5000/api/user/46",
      "body": "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Maecenas rhoncus aliquam lacus.",
      "contact": "1461526025",
      "gooLocation": "0243 Gina Plaza",
      "goodBuyTime": "2016-05-05",
      "goodName": "Entertainment - Diversified",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "timestamp": "Mon, 02 May 2016 00:00:00 GMT",
      "url": "http://127.0.0.1:5000/api/posts/1"
      "comments":"http://....."
      "comments_count":"http://......"
    },
    {

    },
    {
    }，
    ....等等
  ]
}
```
* 备注：请求不同页面的请求格式为：
http://127.0.0.1:5000/api/posts?page=3
参数key:page  Value:<int>


#####获取某个帖子信息          	【GET】   {此api已实现}
* URL: www.jxnugo.com/api/posts/<int:id>
* 参数：帖子id
* 描述：获取某个帖子的信息
* 返回类型：

```
	{
  "author": "http://127.0.0.1:5000/api/user/79",
  "body": "Nulla nisl. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi.",
  "contact": "1266275125",
  "gooLocation": "3 Toban Pass",
  "goodBuyTime": "2016-05-10",
  "goodName": "Medical Practitioners",
  "goodPrice": 1239.12,
  "goodQuality": "9成新",
  "goodTag": 4,
  "photos": null,
  "timestamp": "Mon, 09 May 2016 00:00:00 GMT",
  "url": "http://127.0.0.1:5000/api/posts/4"
  "comments":"http://",
  "comments_count":"http://"
}

```

#####获取某个用户发布的帖子 [GET]
* URL：www.jxnugo.com/api/user_posts/<int:id>
* 参数：用户id

#####获取某个用户收藏的帖子     【GET】    {此api已实现}
* URL:www.jxnugo.com/api/user_collectionpost/<int:id>
* 参数：用户id
* 请求成功的返回值(后台设置最大返回5个帖子)

```
{
  "collectionPost": [
    {
      "author": "http://127.0.0.1:5000/api/user/52",
      "body": "Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue.",
      "contact": "1265122842",
      "goodBuyTime": "2016-04-22",
      "goodLocation": "24 Sullivan Street",
      "goodName": "Industrial Electrical Equipment",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "timestamp": "Tue, 10 May 2016 00:00:00 GMT",
      "url": "http://127.0.0.1:5000/api/posts/19"
    },
    {
      等等
    }
  ]
}

```

#####获取某个帖子的评论  【GET】
* URL: www.jxnugo.com/api/comments/<int:id>
* 参数：帖子id

#####发表新的帖子  	【POST】
* URL: www.jxnugo.com/api/new_post

#####对帖子发表评论   	【POST】
* URL: www.jxnugo.com/api/new_comment/<int:id>
* 参数：帖子id


#####收藏某篇帖子      【POST】
* URL:www.jxnugo.com/api/collect/<int:id>
* 参数：帖子id

#####取消收藏某篇帖子   【POST】
* URL:www.jxnugo.com/api/uncollect/<int:id>
* 参数：帖子id



###用户相关
#####获取个人用户信息  【GET】
* URL: www.jxnugo.com/api/user/<int:id>
* 参数：用户id
* 描述：获取某个用户的信息
* 请求成功返回值：

```
{
  "about_me": "Sed sagittis.",
  "last_seen": "Wed, 11 May 2016 08:13:17 GMT",
  "location": "Bell",
  "menber_since": "Thu, 21 Apr 2016 00:00:00 GMT",
  "name": "Joyce Crawford",
  "postCount": 1,
  "sex": "男",
  "userName": "ann68"
  "posts":"",
  "collectionPost":"",
  "followed":"",
  "followers":""
}

```

#####获取某个用户关注的人   【GET】
* URL：www.jxnugo.com/api/user_followed/<int:id>
* 参数：用户id

#####获取某个用户的粉丝     【GET】
* URL:www.jxnugo.com/api/user_followers/<int:id>
* 参数：用户id


#####获取某个用户发表过的评论   【GET】
* URL:www.jxnugo.com/api/user_comments/<int:id>
* 参数：用户id

#####关注某个用户   【POST】
* URL: www.jxnugo.com/api/follow/<int:id>
* 参数：被关注用户的id

#####取消关注        【POST】
* URL：www.jxnugo.com/api/unfollow/<int:id>
* 参数：被取消关注用户的id

