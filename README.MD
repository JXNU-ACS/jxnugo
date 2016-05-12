#JXNUGO
www.jxnugo.com

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

#####1、用户登录  【GET】         {此api已实现}
* URL:  www.jxnugo.com/api/get_token
* 描述：用来用户登录验证
* 参数：userName,passWord
* 请求成功返回值：

```
  {
		"expiration"3600,
		"token":"eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2MjkwMTM1MSwiaWF0IjoxNDYyODk3NzUxfQ.eyJpZCI6NX0.zsYFk7rzBi68TIY3PWe_8jwjsvPTghrM80RjeyDQd1k"
		“userId”:40
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
	userId:用户id



#####2、用户注册	【POST】  {此api已实现}
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
*  注册成功返回值，状态码：200

```

  {
  	"registerStatus":"successful"
  }

```





#####3、请求七牛云上传token  【GET】   {此api已实现}
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



#####4、获取一个页面的帖子的信息   【GET】  {此api已实现}
* URL: www.jxnugo.com/api/posts
* 描述：获取固定数量(可指定数量)的帖子信息
* 请求成功返回值：

```
	{
	  "author": "http://127.0.0.1:5000/api/user/25",
      "body": "Suspendisse potenti. Ut tellus.",
      "commentsCount": 0,
      "contact": "1381077326",
      "goodBuyTime": "2016-04-29",
      "goodLocation": "637 Shopko Hill",
      "goodName": "Property & Casualty Insurance",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "postId": 5,
      "photos": null,
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
      "postUserName": "marie80",
      "timestamp": "2016-04-29 00:00:00",
      "url": "http://127.0.0.1:5000/api/posts/1"    },
    {

    },
    {
    }，
    等等
  ]
}
```
* 备注：请求不同页面的请求格式为：
http://127.0.0.1:5000/api/posts?page=3
参数key:page  Value:<int>



#####5、获取某个帖子信息          	【GET】   {此api已实现}
* URL: www.jxnugo.com/api/posts/<int:id>
* 参数：帖子id
* 描述：获取某个帖子的信息
* 返回类型：

```
	{
  {
  "author": "http://127.0.0.1:5000/api/user/43",
  "body": "Curabitur at ipsum ac tellus semper interdum. Morbi a ipsum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.",
  "commentsCount": 0,
  "contact": "1040471275",
  "goodBuyTime": "2016-05-09",
  "goodLocation": "8271 Fair Oaks Road",
  "goodName": "Office Supplies",
  "goodPrice": 1239.12,
  "goodQuality": "9成新",
  "goodTag": 4,
  "photos": null,
  "postId": 5,
  "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
  "postUserName": "ruby90",
  "timestamp": "2016-05-06 00:00:00",
  "url": "http://127.0.0.1:5000/api/posts/5"
}}

```



#####6、获取某个用户发布的帖子 [GET]   {此api已实现}
* URL：www.jxnugo.com/api/user_posts/<int:id>
* 参数：用户id
* 请求成功的返回值


```
{
  "userPosts": [
    {
      "author": "http://127.0.0.1:5000/api/user/40",
      "body": "Nulla mollis molestie lorem. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. In sagittis dui vel nisl.",
      "commentsCount": 0,
      "contact": "1168038514",
      "goodBuyTime": "2016-04-23",
      "goodLocation": "0 Ronald Regan Terrace",
      "goodName": "Beverages - Brewers",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "postId": 55,
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
      "postUserName": "ruth86",
      "timestamp": "2016-05-11 00:00:00",
      "url": "http://127.0.0.1:5000/api/posts/55"
    }

  ]
}
```

#####7、获取某个用户收藏的帖子     【GET】    {此api已实现}
* URL:www.jxnugo.com/api/user_collectionpost/<int:id>
* 参数：用户id
* 请求成功的返回值(后台设置最大返回5个帖子)

```
{
  "collectionPost": [
    {
      "author": "http://127.0.0.1:5000/api/user/82",
      "body": "Nullam varius.",
      "commentsCount": 3,
      "contact": "1302060376",
      "goodBuyTime": "2016-04-22",
      "goodLocation": "5873 Nobel Court",
      "goodName": "Electronics Stores",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "postId": 16,
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
      "postUserName": "kathleen72",
      "timestamp": "2016-05-11 00:00:00",
      "url": "http://127.0.0.1:5000/api/posts/16"
    },
     {
      等等
    }
  ]
}

```

#####8、获取某个帖子的评论  【GET】  {此api已实现}
* URL: www.jxnugo.com/api/comments/<int:id>
* 参数：帖子id
* 请求成功返回值

```
{
  "comments": [
    {
      "author": "ruth86",
      "authorAvatar": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
      "authorId": 40,
      "body": "来评论",
      "timestamp": "2016-05-12 01:34:45"
    },
    {
      "author": "ruth86",
      "authorAvatar": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
      "authorId": 40,
      "body": "再来评论",
      "timestamp": "2016-05-12 01:34:54"
    },
      等等
  ]
}


```


#####9、发表新的帖子  	【POST】    {此api已实现}

* URL: www.jxnugo.com/api/new_post
* 描述：上传数据，发布新帖子
* 上传数据格式


```
	{
		"body":"",
		"timestamp":"",
		"goodName":"",
		"goodPrice":"",
		"goodLocation":"",
		"goodQuality":"",
		"goodBuyTime":"",
		"goodTag":"",      #0生活用品1数码科技2服饰箱包3图书音像4其它,默认其它
		"contact”:“”，
		"photos":"",

	}

```
* 上传成功返回值，返回改篇帖子的全部json信息。



#####10、对帖子发表评论   	【POST】
* URL: www.jxnugo.com/api/new_comment/<int:id>
* 参数：帖子id


#####11、收藏某篇帖子      【POST】
* URL:www.jxnugo.com/api/collect/<int:id>
* 参数：帖子id

#####12、取消收藏某篇帖子   【POST】
* URL:www.jxnugo.com/api/uncollect/<int:id>
* 参数：帖子id



###用户相关
#####13、获取个人用户信息  【GET】    {此api已实现}
* URL: www.jxnugo.com/api/user/<int:id>
* 参数：用户id
* 描述：获取某个用户的信息
* 请求成功返回值：

```
{
  "about_me": "Nulla ac enim.",
  "avatar": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA",
  "followed": 2,
  "followers": 1,
  "last_seen": "2016-05-12 12:02:57",
  "location": "San Clemente",
  "member_since": "2016-05-09 00:00:00",
  "name": "Jane Lane",
  "postCollectionCount": 4,
  "postCount": 1,
  "contactMe": null,
  "sex": "男",
  "userId": 40,
  "userName": "ruth86"
}
```


#####14、获取某个用户关注的人   【GET】   {此api已实现}
* URL：www.jxnugo.com/api/user_followed/<int:id>
* 参数：用户id
* 描述：获取用户关注的人的名字还有指向TA的链接
* 请求成功返回值

```
	{
  "followers": [
    {
      "urlLinkUser": "http://127.0.0.1:5000/api/user/101",
      "userName": "ddragon"
    }
  ]
}
```


#####15、获取某个用户的粉丝     【GET】   {此api已实现}
* URL:www.jxnugo.com/api/user_followers/<int:id>
* 参数：用户id
* 描述：获取用户的粉丝的名字还有指向TA的链接
* 请求成功返回值

```
	{
  "followed": [
    {
      "urlLinkUser": "http://127.0.0.1:5000/api/user/1",
      "userName": "shirley91"
    },
    {
      "urlLinkUser": "http://127.0.0.1:5000/api/user/52",
      "userName": "teresa84"
    },
    {
      等等
    }
  ]
}
```

#####16、获取某个用户发表过的评论   【GET】   {此api已实现}
* URL:www.jxnugo.com/api/user_comments/<int:id>
* 参数：用户id
* 请求成功返回值

```
{
  "userComments": [
    {
      "body": "来评论",
      "postName": "Electronics Stores",
      "timestamp": "2016-05-12 01:34:45",
      "url": "http://127.0.0.1:5000/api/posts/16"
    },
    {
      "body": "再来评论",
      "postName": "Electronics Stores",
      "timestamp": "2016-05-12 01:34:54",
      "url": "http://127.0.0.1:5000/api/posts/16"
    },    等等
  ]
}
```


#####17、关注某个用户   【POST】
* URL: www.jxnugo.com/api/follow/<int:id>
* 参数：被关注用户的id

#####18、取消关注        【POST】
* URL：www.jxnugo.com/api/unfollow/<int:id>
* 参数：被取消关注用户的id

