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

#####1、用户登录  【GET】
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



#####2、用户注册	【POST】
* URL: www.jxnugo.com/api/register
* 上传到服务器的信息（json格式）如下：

```
	{
  "passWord": "123",
  "userEmail": "jxnuacs@qq.com",
  "userName": "test"
	}
```
* 备注：客户端先对数据进行验证再上传
*  注册成功返回值，状态码：200

```

  {
  	"registerStatus":"successful"
  }

```





#####3、请求七牛云上传token  【GET】
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



#####4、获取一个页面的帖子的信息   【GET】
* URL: www.jxnugo.com/api/posts
* 描述：获取固定数量(可指定数量)的帖子信息
* 请求成功返回值：

```
	{
  "count": 100,
  "next": "http://127.0.0.1:5000/api/posts?page=2",
  "prev": null，
  "posts": [
    {
      "author": "http://127.0.0.1:5000/api/user/2",
      "body": "Pellentesque viverra pede ac diam. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.",
      "commentsCount": 0,
      "contact": "1144728202",
      "goodBuyTime": "2016-04-26",
      "goodLocation": "78 Anhalt Parkway",
      "goodName": "Rental & Leasing Services",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "postId": 1,
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
      "postUserName": "nicole71",
      "timestamp": "2016-05-07 00:00:00",
      "url": "http://127.0.0.1:5000/api/posts/1"
    },
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



#####5、获取某个帖子信息          	【GET】
* URL: www.jxnugo.com/api/posts/<int:id>
* 参数：帖子id
* 描述：获取某个帖子的信息
* 返回类型：

```
	{
  "author": "http://127.0.0.1:5000/api/user/2",
  "body": "Pellentesque viverra pede ac diam. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.",
  "commentsCount": 0,
  "contact": "1144728202",
  "goodBuyTime": "2016-04-26",
  "goodLocation": "78 Anhalt Parkway",
  "goodName": "Rental & Leasing Services",
  "goodPrice": 1239.12,
  "goodQuality": "9成新",
  "goodTag": 4,
  "photos": null,
  "postId": 1,
  "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
  "postUserName": "nicole71",
  "timestamp": "2016-05-07 00:00:00",
  "url": "http://127.0.0.1:5000/api/posts/1"
}

```



#####6、获取某个用户发布的帖子 [GET]
* URL：www.jxnugo.com/api/user_posts/<int:id>
* 参数：用户id
* 请求成功的返回值


```
{
  "userPosts": [
    {
      "author": "http://127.0.0.1:5000/api/user/2",
      "body": "Pellentesque viverra pede ac diam. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.",
      "commentsCount": 0,
      "contact": "1144728202",
      "goodBuyTime": "2016-04-26",
      "goodLocation": "78 Anhalt Parkway",
      "goodName": "Rental & Leasing Services",
      "goodPrice": 1239.12,
      "goodQuality": "9成新",
      "goodTag": 4,
      "photos": null,
      "postId": 1,
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
      "postUserName": "nicole71",
      "timestamp": "2016-05-07 00:00:00",
      "url": "http://127.0.0.1:5000/api/posts/1"
    }
  ]
}
```

#####7、获取某个用户收藏的帖子     【GET】
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
      "postUserAvator": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
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

#####8、获取某个帖子的评论  【GET】
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


#####9、发表新的帖子  	【POST】

* URL: www.jxnugo.com/api/new_post
* 描述：上传数据，发布新帖子
* 上传数据格式


```
{		"userId":"1",
        "body":"二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，成色非常好，见鲁大师，见鲁大师二手笔记本，",
        "goodName":"戴尔灵越5537",
        "goodNum":"1",
        "goodPrice":"2000",
        "goodLocation":"一栋N204",
        "goodQuality":"7成新",
        "goodBuyTime":"2014年6月",
        "goodTag":"1",
        "contact":"13361640744",
        "photos":[
            {
                "key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
            },
            {
                "key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
            },
            {
              "key":"84BE7838-E41C-4E60-A1B8-CA95DBEE326B"
            }

            ]

}
```
* 上传成功返回值(json)

```
	{
		"postStatus":"successful"
	}
```



#####10、对帖子发表评论   	【POST】
* URL: www.jxnugo.com/api/new_comment
* 参数：帖子id


```
    {
  	"userId":"58",
  	"postId": "16",
  	"body":"api来测试评论"
}

```
* 上传成功返回值  http状态码200

```
{
  "commentStatus": "successful"
}

```


#####11、收藏某篇帖子      【POST】
* URL:www.jxnugo.com/api/collect
* 参数：无
* 数据上传格式（json）用户自身id（selfId）和帖子的id

```
{
  "userId": "27",
  "postId": "58"
}

```
* 上传成功的返回值   http状态码200

```
{
  "collectStatus": "successful"
}

```




#####12、取消收藏某篇帖子   【POST】
* URL:www.jxnugo.com/api/uncollect
* 参数：无
 * 数据上传格式（json）用户自身id（selfId）和帖子的id

```
{
  "userId": "27",
  "postId": "58"
}

```
* 上传成功的返回值   http状态码200

```
{
  "uncollectStatus": "successful"
}

```

####13、判断用户是否已经收藏过某篇帖子  【POST】
* URL:www.jxnugo.com/api/judge_collect
* 参数：无
* 数据上传格式（json）用户自身的id和帖子id

```
{
  "userId": "101",
  "postId": "58"
}

```
* 请求成功返回值(json)  1代表用户已经关注过该帖子，0代表未关注

```
{
  "collectInfo": 0
}
```






###用户相关
#####14、获取个人用户信息  【GET】
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
  "contactMe": null,
  "postCount": 1,
  "sex": "男",
  "userId": 40,
  "userName": "ruth86"
}
```


#####15、获取某个用户关注的人   【GET】
* URL：www.jxnugo.com/api/user_followed/<int:id>
* 参数：用户id
* 描述：获取用户关注的人的名字还有指向TA的链接
* 请求成功返回值

```
	{
  "followed": [
    {
      "aboutMe": "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.",
      "urlLinkUser": "http://127.0.0.1:5000/api/user/37",
      "userAvatar": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
      "userId": 37,
      "userName": "nancy90"
    },
    等等
  ]
}
```


#####16、获取某个用户的粉丝     【GET】
* URL:www.jxnugo.com/api/user_followers/<int:id>
* 参数：用户id
* 描述：获取用户的粉丝的名字还有指向TA的链接
* 请求成功返回值

```
	{
  "followers": [
    {
      "aboutMe": "Proin interdum mauris non ligula pellentesque ultrices.",
      "urlLinkUser": "http://127.0.0.1:5000/api/user/27",
      "userAvatar": "http://7xrkww.com1.z0.glb.clouddn.com/84BE7838-E41C-4E60-A1B8-CA95DBEE326B.png",
      "userId": 27,
      "userName": "ddragon"
    }
  ]
}
```

#####17、获取某个用户发表过的评论   【GET】
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


#####18、关注某个用户   【POST】
* URL: www.jxnugo.com/api/follow
* 参数：无
* 上传的数据（json）：包含自己的id和关注用户的id

```
	{
 	 "userId": "101",
  	 "followedId": "58"
	}
```
* 返回数据（json） 返回http状态码200

```
	{
  		"followStatus": "successful"
	}

```

#####19、取消关注        【POST】
* URL：www.jxnugo.com/api/unfollow
* 参数：无
* 上传的的数据(json)，包含自己的id和被取消用户的id

```
	{
 	 "userId": "101",
  	 "unfollowedId": "58"
	}

```
* 返回的数据   成功后返回的http状态吗200


```
{
  "unfollowStatus": "successful"
}

```

#####20、判断用户是否已经关注了某个用户   [GET]
* URL: www.jxnugo.com/api/judge_follow
* 参数：无
* 上传的数据格式（json），包含自己的id还有其它用户的id

```
{
  "userId": "101",
  "followerId": "59"
}
```
* 请求成功数据返回格式  1代表已经关注过该用户，0代表未关注过

```
{
  "judgeInfo": 0
}

```

#####21、更新用户个人信息
* URL: www.jxnugo.com/api/update_userInfo   [POST]
* 参数：无
* 上传的数据格式（json）

```
{
        "userId":"17",
        "name":"haha",
        "location":"江西南昌",
        "sex":"女",
        "contact":"13312312123",
        "about_me":"七牛云存储",
        "avatar":"http://7xrkww.com1.z0.glb.clouddn.com/Frkrfg7cCZ3xO3mwmKXCfbdQ-FQ0"

}

```

* 返回的数据

```
{
  "updateStatus": "successful"
}
```

#####22、删除帖子
* URL:www.jxnugo.com/api/post_delete  [DELETE]
* 参数：无
* 上传的数据格式（json）

```
	{
		"userId":"123",
		"postId":"12"
	}

```
* 删除成功返回值  状态码

```
{
  "deleteStatus": "successful delete post"
}

```