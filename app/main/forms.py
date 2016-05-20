# -*- coding: UTF-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField,SelectField
from wtforms.validators import Required,Email,EqualTo,Length
from ..models import User,Role
from wtforms import ValidationError

class EditProfileForm(Form):
    name=StringField(u'真名',validators=[Length(0,64)])
    location=StringField(u'所在地',validators=[Length(0,64)])
    about_me=TextAreaField(u'关于我')
    mycontact=StringField(u'联系方式')
    avatar=StringField(u'头像')
    submit=SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email=StringField(u'邮箱',validators=[Required(),Length(1,64),Email()])
    username=StringField(u'用户名',validators=[Required(),Length(1,64)])
    confirmed=BooleanField(u'确认激活状态')
    role=SelectField(u'角色',coerce=int)
    name=StringField(u'名字',validators=[Length(0,64)])
    location=StringField(u'位置',validators=[Length(0,64)])
    about_me=TextAreaField(u'关于我')
    mycontact=StringField(u'联系方式')
    submit=SubmitField(u'提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data != self.user.userEmail and User.query.filter_by(userEmail=field.data).first():
            raise ValidationError(u'该邮箱已经注册过')

    def validate_username(self,field):
        if field.data !=self.user.userName and User.query.filter_by(userName=field.data).first():
            raise ValidationError(u'该用户名已经存在')



