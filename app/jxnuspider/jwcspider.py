# usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
from itertools import izip
from json import dumps


class JwcSpider(object):
    def __init__(self):
        super(JwcSpider, self).__init__()
        self.login_url='http://jwc.jxnu.edu.cn/Default_Login.aspx?preurl='
        self.stu_timetable_url='http://jwc.jxnu.edu.cn/User/default.aspx?&&code=111&uctl=MyControl%5cxfz_kcb.ascx&MyAction=Personal'
        self.stu_info_url='http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=All_StudentInfor.ascx&UserType=Student&UserNum=1408095013'
        self.stu_grade_url='http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=xfz_cj.ascx&Action=Personal'
        self.stu_exam_schedule_url='http://jwc.jxnu.edu.cn/User/default.aspx?&code=129&&uctl=MyControl%5cxfz_test_schedule.ascx'
        self.cookie=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

    def get_cookie(self):
        post_data = urllib.urlencode({
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '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',
        '__EVENTVALIDATION': '/wEWSALmpfLnDgLr6+/kCQK3yfbSBAKDspbeCQL21fViApC695MMAsjQmpEOAsjQpo4OAv3S2u0DAv3S9t4DAqPW8tMDAv3S6tEDAqPW3ugDArWVmJEHAr/R2u0DAqrwhf4KAsjQtoIOAsjQooMOAv3S3ugDArfW7mMC/dL+0AMCvJDK9wsC/dLy0wMCr9GugA4C8pHSiQwC6dGugA4C+dHq0QMC3NH61QMCjtCenA4CntDm2gMCxrDmjQ0CyNCqhQ4Co9b+0AMCvJDaiwwC3NHa7QMCv9Hi3wMC/dLu3AMC3NHm2gMCjtCyhw4CpbHqgA0CyNCugA4C/dLm2gMC3NHq0QMCjtCigw4C/dLi3wMCjtC+hA4CqvCJ9QoC3NHu3AMC3NHi3wMC6dGenA4C3NHy0wMCjtC6mQ4CjtCugA4C3NH+0AMCntDa7QMC/dL61QMCw5bP/gICv9He6AMC8pHaiwwCr9Gyhw4CyNC+hA4CyNCenA4C3NH23gMCr9GqhQ4C3NHe6AMCjtC2gg4Co9bm2gMC+euUqg4C2tqumwgC0sXgkQ8CuLeX+QECj8jxgApGWHvI+6JCz5fmeO13a+NOvECIdDdppxCPzhkFMfBb2Q==',
        'ddlCollege': '180     ',
        'rblUserType': 'Student',
        'StuNum': 1408095013,
        'TeaNum': '',
        'Password': 8571001,
        'login': '登录'
        })
        req = urllib2.Request(
        self.login_url,
        data=post_data
        )
        result = self.opener.open(req)

    def get_stu_info(self):
        stu_info = {}
        stu_info_result=self.opener.open(self.stu_info_url)
        stu_info_html = stu_info_result.read()
        stu_info_soup = BeautifulSoup(stu_info_html, "html.parser")
        class_name = stu_info_soup.find(id="_ctl0_lblBJ")
        stu_id = stu_info_soup.find(id="_ctl0_lblXH")
        stu_name = stu_info_soup.find(id="_ctl0_lblXM")
        stu_sex = stu_info_soup.find(id="_ctl0_lblXB")
        stu_info["class_name"] = str(class_name.contents).decode("unicode_escape")
        stu_info["stu_id"] = str(stu_id.contents).decode("unicode_escape")
        stu_info["stu_name"] = str(stu_name.contents).decode("unicode_escape")
        stu_info["stu_sex"] = str(stu_sex.contents).decode("unicode_escape")
        return stu_info

    def get_stu_grade(self):
        count = 0
        each_sum = 0           # 计算学期起始位置时候用
        title_list_key = ["academy","specialty","class","stu_id","stu_name","credits"]
        title_list_value = []  # 创建保存学院专业姓名等标题栏基本信息的list
        semester_list = []     # 用于保存多少个学期的list
        course_count_list = []    # 用于保存每个学期各有多少门课的list
        courses_list = []     # 保存课程等杂乱信息列表
        title_dict = {}      # 保存标题栏信息
        semester_position = []   # 记录courses_list中保存学期的位置
        course_dict = {"course":[]}
        stu_grade_result = self.opener.open(self.stu_grade_url)  # 返回学生成绩界面html
        grade_html_page = stu_grade_result.read()
        grade_soup = BeautifulSoup(grade_html_page,"html.parser")
        grade_title = grade_soup.find_all("u")# 处理成绩界面标题栏
        for i in grade_title:
            i = str(i.contents).decode("unicode_escape")
            title_list_value.append(i)
        for x, y in izip(title_list_key,title_list_value):   # 将信息保存在字典里面，用了itertools中的izip迭代两个对象
            title_dict[x] = y
        grade_semester = grade_soup.find_all("td",valign="middle") # 处理学期的成绩
        for z in grade_semester:                              # 对学期进行遍历
            z = str(z.contents).decode("unicode_escape") # 打印含有font的学期信息print z
            grade_semester_soup = BeautifulSoup(z,"html.parser")  #提取有多少个学期
            semester = grade_semester_soup.find_all("font")
            for k in semester:
                k = str(k.contents).decode("unicode_escape")
                semester_list.append(k)
        grade_itmes = grade_soup.find_all("font",color="#330099")   # 提取课程的详细信息（未除去学期信息）
        for g in grade_itmes:
            g = str(g.contents).decode("unicode_escape")       # 打印成绩的信息
            courses_list.append(g)
        td_tag = grade_soup.select('td[rowspan]')     # 提取每个学期有多少门课
        for t in td_tag:
            course_count_list.append(int(t['rowspan']))
        while count<len(course_count_list):            # 获取每个学期每个课程的起始位置
            if count == 0:
                each_sum = course_count_list[count]*7
                step = 0
            else:
                step = each_sum+count
                each_sum = each_sum+course_count_list[count]*7
            count = count+1
            semester_position.append(step)            # 添加位置
        new_count = 0                                   # 将起止位置的数据删除
        for pos in semester_position:
            p = pos-new_count
            del courses_list[p]
            new_count = new_count+1
        for course in range(0,len(courses_list),7):
            course_item = dict()
            course_item['course_id'] = courses_list[course]
            course_item['course_name'] = courses_list[course+1]
            course_item['course_point'] = courses_list[course+2]
            course_item['course_grade'] = courses_list[course+3]
            course_item['twice_course_grade'] = courses_list[course+4]
            course_item['weighted_grade'] = courses_list[course+5]
            course_item['note'] = courses_list[course+6]
            course_dict["course"].append(course_item)
        title_dict["courses"] = course_dict["course"]
        return title_dict

    def get_stu_timetable(self):
        stu_timetable = {"course":[]}  # 存储学生课表的字典
        timetable_list = []          # 存储课程id，课程名，班级和老师姓名的字典
        timetable_tag_list = []      # 存储含义<a></a>的字典
        timetable_data = urllib.urlencode({
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJNzIzMTk0NzYzD2QWAgIBD2QWCgIBDw8WAh4EVGV4dAUfMjAxNuW5tDbmnIgy5pelIOaYn+acn+WbmyZuYnNwO2RkAgUPDxYCHwAFGOW9k+WJjeS9jee9ru+8muivvueoi+ihqGRkAgcPDxYCHwAFLSAgIOasoui/juaCqO+8jCgxNDA4MDk1MDEzLFN0dWRlbnQpIOi1lumBk+m+mWRkAgoPZBYEAgEPDxYCHghJbWFnZVVybAVDLi4vTXlDb250cm9sL0FsbF9QaG90b1Nob3cuYXNweD9Vc2VyTnVtPTE0MDgwOTUwMTMmVXNlclR5cGU9U3R1ZGVudGRkAgMPFgIfAAW2IzxkaXYgaWQ9J21lbnVQYXJlbnRfMCcgY2xhc3M9J21lbnVQYXJlbnQnIG9uY2xpY2s9J21lbnVHcm91cFN3aXRjaCgwKTsnPuaIkeeahOS/oeaBrzwvZGl2PjxkaXYgaWQ9J21lbnVHcm91cDAnIGNsYXNzPSdtZW51R3JvdXAnPjxEaXYgY2xhc3M9J21lbnVJdGVtT24nIHRpdGxlPSfor77nqIvooagnPjxhIGhyZWY9ImRlZmF1bHQuYXNweD8mY29kZT0xMTEmJnVjdGw9TXlDb250cm9sXHhmel9rY2IuYXNjeCZNeUFjdGlvbj1QZXJzb25hbCIgdGFyZ2V0PSdwYXJlbnQnPuivvueoi+ihqDwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+WfuuacrOS/oeaBryc+PGEgaHJlZj0iLi5cTXlDb250cm9sXFN0dWRlbnRfSW5mb3JDaGVjay5hc3B4IiB0YXJnZXQ9J19ibGFuayc+5Z+65pys5L+h5oGvPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5L+u5pS55a+G56CBJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTEwJiZ1Y3RsPU15Q29udHJvbFxwZXJzb25hbF9jaGFuZ2Vwd2QuYXNjeCIgdGFyZ2V0PSdwYXJlbnQnPuS/ruaUueWvhueggTwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+WtpuexjemihOitpic+PGEgaHJlZj0iamF2YXNjcmlwdDpPcGVuV2luZG93KCd4ZnpfYnlzaC5hc2N4JkFjdGlvbj1QZXJzb25hbCcpOyIgdGFyZ2V0PScnPuWtpuexjemihOitpjwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+aWsOeUn+WvvOW4iCc+PGEgaHJlZj0iZGVmYXVsdC5hc3B4PyZjb2RlPTIxNCYmdWN0bD1NeUNvbnRyb2xcc3R1ZGVudF9teXRlYWNoZXIuYXNjeCIgdGFyZ2V0PSdwYXJlbnQnPuaWsOeUn+WvvOW4iDwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+ivvueoi+aIkOe7qSc+PGEgaHJlZj0iamF2YXNjcmlwdDpPcGVuV2luZG93KCd4ZnpfY2ouYXNjeCZBY3Rpb249UGVyc29uYWwnKTsiIHRhcmdldD0nJz7or77nqIvmiJDnu6k8L2E+PC9kaXY+PERpdiBjbGFzcz0nbWVudUl0ZW0nIHRpdGxlPScyMDE25bm05LiK5Y2K5bm057uT5Lia6KGl6ICD5oql5ZCNJz48YSBocmVmPSJqYXZhc2NyaXB0Ok9wZW5XaW5kb3coJ0pZQktfWFNfSW5kZXguYXNjeCcpOyIgdGFyZ2V0PScnPjIwMTblubTkuIrljYrlubTnu5PkuJrooaXogIPmiqXlkI08L2E+PC9kaXY+PERpdiBjbGFzcz0nbWVudUl0ZW0nIHRpdGxlPSfmiYvmnLrlj7fnoIEnPjxhIGhyZWY9Ii4uXE15Q29udHJvbFxQaG9uZS5hc3B4IiB0YXJnZXQ9J19ibGFuayc+5omL5py65Y+356CBPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5a626ZW/55m75b2VJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MjAzJiZ1Y3RsPU15Q29udHJvbFxKel9zdHVkZW50c2V0dGluZy5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5a626ZW/55m75b2VPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5Y+M5LiT5Lia5Y+M5a2m5L2N6K++56iL5a6J5o6S6KGoJz48YSBocmVmPSIuLlxNeUNvbnRyb2xcRGV6eV9rYi5hc3B4IiB0YXJnZXQ9J19ibGFuayc+5Y+M5LiT5Lia5Y+M5a2m5L2N6K++56iL5a6J5o6S6KGoPC9hPjwvZGl2PjwvZGl2PjxkaXYgaWQ9J21lbnVQYXJlbnRfMScgY2xhc3M9J21lbnVQYXJlbnQnIG9uY2xpY2s9J21lbnVHcm91cFN3aXRjaCgxKTsnPuWFrOWFseacjeWKoTwvZGl2PjxkaXYgaWQ9J21lbnVHcm91cDEnIGNsYXNzPSdtZW51R3JvdXAnPjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5Z+55YW75pa55qGIJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTA0JiZ1Y3RsPU15Q29udHJvbFxhbGxfanhqaC5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5Z+55YW75pa55qGIPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n6K++56iL5L+h5oGvJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTE2JiZ1Y3RsPU15Q29udHJvbFxhbGxfY291cnNlc2VhcmNoLmFzY3giIHRhcmdldD0ncGFyZW50Jz7or77nqIvkv6Hmga88L2E+PC9kaXY+PERpdiBjbGFzcz0nbWVudUl0ZW0nIHRpdGxlPSflvIDor77lronmjpInPjxhIGhyZWY9Ii4uXE15Q29udHJvbFxQdWJsaWNfS2thcC5hc3B4IiB0YXJnZXQ9J19ibGFuayc+5byA6K++5a6J5o6SPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5a2m55Sf5L+h5oGvJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTE5JiZ1Y3RsPU15Q29udHJvbFxhbGxfc2VhcmNoc3R1ZGVudC5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5a2m55Sf5L+h5oGvPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5pWZ5bel5L+h5oGvJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTIwJiZ1Y3RsPU15Q29udHJvbFxhbGxfdGVhY2hlci5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5pWZ5bel5L+h5oGvPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n55+t5L+h5bmz5Y+wJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTIyJiZ1Y3RsPU15Q29udHJvbFxtYWlsX2xpc3QuYXNjeCIgdGFyZ2V0PSdwYXJlbnQnPuefreS/oeW5s+WPsDwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+aVmeWupOaVmeWtpuWuieaOkic+PGEgaHJlZj0iLi5cTXlDb250cm9sXHB1YmxpY19jbGFzc3Jvb20uYXNweCIgdGFyZ2V0PSdfYmxhbmsnPuaVmeWupOaVmeWtpuWuieaOkjwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+acn+acq+aIkOe7qeafpeivoic+PGEgaHJlZj0iamF2YXNjcmlwdDpPcGVuV2luZG93KCd4ZnpfVGVzdF9jai5hc2N4Jyk7IiB0YXJnZXQ9Jyc+5pyf5pyr5oiQ57up5p+l6K+iPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5pyf5pyr5oiQ57up5p+l5YiG55Sz6K+3Jz48YSBocmVmPSJqYXZhc2NyaXB0Ok9wZW5XaW5kb3coJ0Nmc3FfU3R1ZGVudC5hc2N4Jyk7IiB0YXJnZXQ9Jyc+5pyf5pyr5oiQ57up5p+l5YiG55Sz6K+3PC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n6KGl57yT6ICD5a6J5o6SJz48YSBocmVmPSJqYXZhc2NyaXB0Ok9wZW5XaW5kb3coJ3hmel9UZXN0X0JISy5hc2N4Jyk7IiB0YXJnZXQ9Jyc+6KGl57yT6ICD5a6J5o6SPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5a2m5Lmg6Zeu562UJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTU5JiZ1Y3RsPU15Q29udHJvbFxBbGxfU3R1ZHlfTGlzdC5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5a2m5Lmg6Zeu562UPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5Y+M5a2m5L2N6K++56iL5oiQ57upJz48YSBocmVmPSJqYXZhc2NyaXB0Ok9wZW5XaW5kb3coJ2RlenlfY2ouYXNjeCZBY3Rpb249UGVyc29uYWwnKTsiIHRhcmdldD0nJz7lj4zlrabkvY3or77nqIvmiJDnu6k8L2E+PC9kaXY+PERpdiBjbGFzcz0nbWVudUl0ZW0nIHRpdGxlPSfmr5XkuJrnlJ/lm77lg4/ph4fpm4bkv6Hmga/moKHlr7knPjxhIGhyZWY9Ii4uXE15Q29udHJvbFxUWENKX0luZm9yQ2hlY2suYXNweCIgdGFyZ2V0PSdfYmxhbmsnPuavleS4mueUn+WbvuWDj+mHh+mbhuS/oeaBr+agoeWvuTwvYT48L2Rpdj48L2Rpdj48ZGl2IGlkPSdtZW51UGFyZW50XzInIGNsYXNzPSdtZW51UGFyZW50JyBvbmNsaWNrPSdtZW51R3JvdXBTd2l0Y2goMik7Jz7mlZnlrabkv6Hmga88L2Rpdj48ZGl2IGlkPSdtZW51R3JvdXAyJyBjbGFzcz0nbWVudUdyb3VwJz48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9J+e9keS4iuivhOaVmSc+PGEgaHJlZj0iamF2YXNjcmlwdDpPcGVuV2luZG93KCdwal9zdHVkZW50X2luZGV4LmFzY3gnKTsiIHRhcmdldD0nJz7nvZHkuIror4TmlZk8L2E+PC9kaXY+PERpdiBjbGFzcz0nbWVudUl0ZW0nIHRpdGxlPSfmlZnliqHmhI/op4HnrrEnPjxhIGhyZWY9Ii4uL0RlZmF1bHQuYXNweD9BY3Rpb249QWR2aXNlIiB0YXJnZXQ9J19ibGFuayc+5pWZ5Yqh5oSP6KeB566xPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n5pyf5pyr6ICD6K+V5a6J5o6SJz48YSBocmVmPSJkZWZhdWx0LmFzcHg/JmNvZGU9MTI5JiZ1Y3RsPU15Q29udHJvbFx4ZnpfdGVzdF9zY2hlZHVsZS5hc2N4IiB0YXJnZXQ9J3BhcmVudCc+5pyf5pyr6ICD6K+V5a6J5o6SPC9hPjwvZGl2PjxEaXYgY2xhc3M9J21lbnVJdGVtJyB0aXRsZT0n6L6F5L+u5Y+M5LiT5Lia5Y+M5a2m5L2N5oql5ZCNJz48YSBocmVmPSJqYXZhc2NyaXB0Ok9wZW5XaW5kb3coJ0RlenlfYm0uYXNjeCcpOyIgdGFyZ2V0PScnPui+heS/ruWPjOS4k+S4muWPjOWtpuS9jeaKpeWQjTwvYT48L2Rpdj48RGl2IGNsYXNzPSdtZW51SXRlbScgdGl0bGU9JzIwMTXnuqfmnKznp5HlrabnlJ/ovazkuJPkuJrmiqXlkI0nPjxhIGhyZWY9Ii4uXE15Q29udHJvbFx6enlfc3R1ZGVudF9zcS5hc3B4IiB0YXJnZXQ9J19ibGFuayc+MjAxNee6p+acrOenkeWtpueUn+i9rOS4k+S4muaKpeWQjTwvYT48L2Rpdj48L2Rpdj5kAgwPZBYCZg9kFgwCAQ8PFgIfAAUe5rGf6KW/5biI6IyD5aSn5a2m5a2m55Sf6K++6KGoZGQCAw8PFgIfAAVq54+t57qn5ZCN56ew77yaPFU+MTTnuqfnvZHnu5zlt6XnqIsy54+tPC9VPuOAgOOAgOWtpuWPt++8mjxVPjE0MDgwOTUwMTM8L3U+44CA44CA5aeT5ZCN77yaPHU+6LWW6YGT6b6ZPC91PmRkAgUPEA8WBh4NRGF0YVRleHRGaWVsZAUM5a2m5pyf5ZCN56ewHg5EYXRhVmFsdWVGaWVsZAUM5byA5a2m5pel5pyfHgtfIURhdGFCb3VuZGdkEBUIDzE2LTE356ysMeWtpuacnw8xNS0xNuesrDLlrabmnJ8PMTUtMTbnrKwx5a2m5pyfDzE0LTE156ysMuWtpuacnw8xNC0xNeesrDHlrabmnJ8PMTMtMTTnrKwy5a2m5pyfDzEzLTE056ysMeWtpuacnw8xMi0xM+esrDLlrabmnJ8VCBAyMDE2LzkvMSAwOjAwOjAwEDIwMTYvMy8xIDA6MDA6MDAQMjAxNS85LzEgMDowMDowMBAyMDE1LzMvMSAwOjAwOjAwEDIwMTQvOS8xIDA6MDA6MDAQMjAxNC8zLzEgMDowMDowMBAyMDEzLzkvMSAwOjAwOjAwEDIwMTMvMy8xIDA6MDA6MDAUKwMIZ2dnZ2dnZ2dkZAIJDw8WAh4HVmlzaWJsZWhkZAIKDzwrAAsBAA8WCB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQC/////w8eFV8hRGF0YVNvdXJjZUl0ZW1Db3VudAL/////Dx4JUGFnZUNvdW50ZmRkAgsPPCsACwEADxYIHwYWAB8HAv////8PHwgC/////w8fCWZkZGQYo/QDJNl6+jawimOt+oAqcXu4/ulE9WaZGEAFJLL7Ng==',
            '__EVENTVALIDATION': '/wEWCwLgvpr/AwKKhuW9AQLeg/vmBAL9g+OSAgLeg4+HCQL9g/eyBwLItunkDwLvttGQDQLItv0EAu+25bAOAubhijOeabfLoNNKZd7TCMkIVzgdeNtfa33HaTykcWvlFUT6fw==',
            '_ctl1:ddlSterm': '2016/9/1 0:00:00',
            '_ctl1:btnSearch': '确定'
                })
        stu_timetable_req = urllib2.Request(
            self.stu_timetable_url,
            data=timetable_data
            )
        stu_timetable_result = self.opener.open(stu_timetable_req)
        timetable_html_page = stu_timetable_result.read()
        timetable_soup = BeautifulSoup(timetable_html_page, "html.parser")
        timetable_info = timetable_soup.find_all("font", color="#330099")
        for i in range(0, len(timetable_info), 6):          # 将里面的<a></a>标签内容去除
            timetable_tag_list.append(timetable_info[i])
            timetable_tag_list.append(timetable_info[i+1])
            timetable_tag_list.append(timetable_info[i+2])
            timetable_tag_list.append(timetable_info[i+3])
        for y in timetable_tag_list:
            for child in y.children:
                timetable_list.append(child)
        for info in range(0, len(timetable_list), 4):
            timetable = {}
            timetable["course_id"] = timetable_list[info]
            timetable["course_name"] = timetable_list[info+1]
            timetable["class"] = timetable_list[info+2]
            timetable["teacher"] = timetable_list[info+3]
            stu_timetable["course"].append(timetable)
        return stu_timetable

    def get_stu_exem_schedule(self):
        exam_dict = {"exam_schedule":[]}
        exam_schedule_list = []
        stu_exam_schedule_result = self.opener.open(self.stu_exam_schedule_url)
        exam_schedule_html = stu_exam_schedule_result.read()
        exam_soup = BeautifulSoup(exam_schedule_html, "html.parser")
        exam_info = exam_soup.find_all("font", color="#330099")
        for i in exam_info:
            for child in i.children:
                exam_schedule_list.append(str(child.contents).decode("unicode_escape"))
        for subject in range(0, len(exam_schedule_list), 7):
            subject_item = dict()
            subject_item["course_id"] = exam_schedule_list[subject]
            subject_item["course_name"] = exam_schedule_list[subject+1]
            subject_item["stu_id"] = exam_schedule_list[subject+2]
            subject_item["exam_time"] = exam_schedule_list[subject+3]
            subject_item["class_room"] = exam_schedule_list[subject+4]
            subject_item["class_position"] = exam_schedule_list[subject+5]
            subject_item["exam_note"] = exam_schedule_list[subject+6]
            exam_dict["exam_schedule"].append(subject_item)
        return exam_dict