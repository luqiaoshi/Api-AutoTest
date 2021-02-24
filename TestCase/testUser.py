import requests
import pytest
import json
import allure
import sys
import logging
sys.path.append('../')  #将项目路径加到搜索路径中，使得自定义模块可以引用

from config import config
from common.getData import DoexcleByPandas
from common.getHeader import get_header
from common.logFormat import log_format
from common import commonFunction


@allure.feature('系统账户管理')
class TestUser(object):
    log_format()  #配置日志格式
    # 从文件中读取用例信息
    parametrize = DoexcleByPandas().get_data_for_pytest(filename='../data/data.xlsx', sheet_name='system_user')

    @allure.title('{title}')  # 设置用例标题
    @allure.severity(allure.severity_level.CRITICAL)  # 设置用例优先级
    # 将用例信息以参数化的方式传入测试方法
    @pytest.mark.parametrize('id,url,data, story, title,method,severity,condition,except_result', parametrize)
    def test_user(self, id, url, data, story, title, method, severity, condition, except_result):

        '''
        :param id: 用例编号
        :param url: 用例请求的URL地址
        :param data: 用例使用的请求数据
        :param title: 用例标题
        :param method: 用例的请求方式
        :param severity: 用例优先级
        :param condition: 用例的校验条件
        :param except_result: 用例的预期结果
        '''


        allure.dynamic.story(story)  # 动态生成模块
        allure.dynamic.severity(severity)  # 动态生成用例等级

        # test开头的测试函数
        url = config.url + url
        if method == 'get':
            #测试get方法
            r = requests.get(url, headers=get_header())

        elif method == 'post':
            #测试post方法
            data = eval(data)
            r = requests.post(url, headers=get_header(), data=json.dumps(data))

        elif method == 'put':
            #测试put方法
            data = eval(data)
            r = requests.put(url, headers=get_header(), data=json.dumps(data))

        elif method == 'delete':
            #测试delete方法
            r = requests.delete(url, headers=get_header())

        # 将校验条件和预期结果参数化
        if condition != 'nan':
            condition_new = eval(condition)  # 将字符串转化为表达式
            if isinstance(condition_new, str):
                # 判断表达式的结果是否为字符串，如果为字符串格式，则去掉其首尾的空格
                assert condition_new.strip() == except_result
            else:
                assert condition_new == except_result

            # 将用例中的内容打印在报告中
        print(
            '用例编号: ' + str(id) + '\n'
                                 '用例请求的URL地址: ' + str(url) + '\n'
                                                             '用例使用的请求数据: ' + str(data) + '\n'
                                                                                         '用例模块: ' + story + '\n'
                                                                                                            '用例标题: ' + title + '\n'
                                                                                                                               '用例的请求方式: ' + method + '\n'
                                                                                                                                                      '用例优先级: ' + severity + '\n'
                                                                                                                                                                             '用例的校验条件: ' + str(
                condition) + '\n'
                             '用例的实际结果: ' + str(condition_new) + '\n'
                                                                '用例的预期结果: ' + str(except_result)
        )




    '''
        以下用例由于存在较多的前置条件，不便于从excle中获取信息，故使用一个方法一个用例的方式
    '''
    @allure.story('编辑用户')
    @allure.severity('critical')
    @allure.title('测试修改用户信息')
    def test_edit_user(self):
        user_name = 'wx123'
        email = 'stevewen123@yunify.com'
        commonFunction.create_user(user_name)  #创建用户
        version = commonFunction.get_user_version()  #获取创建用户的resourceVersion
        #编辑用户信息的url地址
        url = config.url + '/kapis/iam.kubesphere.io/v1alpha2/users/' + user_name
        #编辑用户的目标数据
        data = {"apiVersion": "iam.kubesphere.io/v1alpha2",
                "kind": "User",
                "metadata": {"name": user_name,
                             "annotations": {"iam.kubesphere.io/password-encrypted": "true",
                                             "kubesphere.io/creator": "admin",
                                             "kubesphere.io/description": "重新编辑"},
                             "resourceVersion": version},
                "spec": {"email": email}
                }
        r = requests.put(url, headers=get_header(), data=json.dumps(data))  #修改新建用户的邮箱和描述信息
        # print(r.text)
        try:
            assert r.json()['spec']['email'] == email  #验证修改用户后的邮箱信息
            #在日志中输出实际结果
            logging.info('reality_result:' + str(r.json()['spec']['email']))
        finally:
            commonFunction.delete_user(user_name)  #删除新建的用户


if __name__ == "__main__":
    pytest.main(['-s', 'testUser.py'])  # -s参数是为了显示用例的打印信息。 -q参数只显示结果，不显示过程


