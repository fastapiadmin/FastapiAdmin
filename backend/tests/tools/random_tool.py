# -*- coding: utf-8 -*-

import string
import random
import datetime
from faker import Faker
from dateutil.relativedelta import relativedelta


class ContextPack:
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @property
    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    @property
    def get_id_number(self) -> int:
        """

        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    @property
    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_male()
        return female_name

    @property
    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_female()
        return male_name

    @property
    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

    @property
    def merchantSelfOperatedShop(self) -> int:
        """

        :return: 商家端自营店铺ID
        """
        SelfOperatedShop = 515
        return SelfOperatedShop

    @property
    def get_secend_time(self)->datetime:
        """
        计算当前时间: 年-月-日 时:分:秒:毫秒
        :return:
        """
        return datetime.datetime.now()

    @property
    def get_day_time(self)->str:
        """
        计算当前时间: 年-月-日
        :return:
        """
        return datetime.datetime.now().strftime('%Y-%m-%d')
    
    def generate_bank_card(self):
        """
        生成随机银行卡号
        """
        return self.faker.credit_card_number()

    def generate_email(self):
        """
        生成随机邮箱号
        """
        return self.random_str(4) + self.faker.free_email()

    @property
    def generate_company(self):
        """
        生成随机公司名称
        """
        return self.faker.company_prefix() + self.random_str(5) + '测试' + self.faker.company_suffix()

    @property
    def generate_name(self):
        """
        生成随机姓名
        """
        return self.faker.name()

    @property
    def generate_unreal_phone(self):
        """
        生成不存在的手机号
        """
        phone = random.choice(['100', '110', '120']) + \
            ''.join(random.choice('0123456789') for _ in range(8))
        return phone

    def random_str(self, str_len: int) -> str:
        """从a-zA-Z0-9生成制定数量的随机字符

        :param str_len: 字符串长度
        :return:
        """
        try:
            str_len = int(str_len)
        except ValueError:
            raise Exception("调用随机字符失败，[ %s ]长度参数有误！" % str_len)
        strings = ''.join(random.sample(string.hexdigits, +str_len))
        return strings

    def random_int(self, scope) -> int:
        """获取随机整型数据

        :param scope: 数据范围
        :return:
        """
        try:
            start_num, end_num = scope.split(",")
            start_num = int(start_num)
            end_num = int(end_num)
        except ValueError:
            raise Exception("调用随机整数失败，[ %s ]范围参数有误！" % str(scope))
        if start_num <= end_num:
            number = random.randint(start_num, end_num)
        else:
            number = random.randint(end_num, start_num)
        return number

    def random_float(self, data) -> float:
        """获取随机浮点数据

        :param data: 数组
        :return:
        """
        try:
            start_num, end_num, accuracy = data.split(",")
            start_num = int(start_num)
            end_num = int(end_num)
            accuracy = int(accuracy)
        except ValueError:
            raise Exception("调用随机浮点数失败，[ %s ]范围参数或精度有误！" % data)

        if start_num <= end_num:
            number = random.uniform(start_num, end_num)
        else:
            number = random.uniform(end_num, start_num)
        number = round(number, accuracy)
        return number

    def random_choice(self, data):
        """获取数组随机值

        :param data: 数组
        :return:
        """
        _list = data.split(",")
        each = random.choice(_list)
        return each

    def get_date_mark(self, now, mark, num):
        if 'y' == mark:
            return now + relativedelta(years=num)
        elif 'm' == mark:
            return now + relativedelta(months=num)
        elif 'd' == mark:
            return now + relativedelta(days=num)
        elif 'h' == mark:
            return now + relativedelta(hours=num)
        elif 'M' == mark:
            return now + relativedelta(minutes=num)
        elif 's' == mark:
            return now + relativedelta(seconds=num)
        else:
            raise Exception("日期字段标识[ %s ]错误, 请使用[年y,月m,日d,时h,分M,秒s]标识!" % mark)

    def generate_date(self, expr=''):
        """生成日期对象(不含时分秒)

        :param expr: 日期表达式，如"d-1"代表日期减1
        :return:
        """
        today = datetime.date.today()
        if expr:
            try:
                mark = expr[:1]
                num = int(expr[1:])
            except (TypeError, NameError):
                raise Exception("调用生成日期失败，日期表达式[ %s ]有误！" % expr)
            return self.get_date_mark(today, mark, num)
        else:
            return today

    def generate_datetime(self, expr=''):
        """生成日期时间对象(含时分秒)

        :param expr: 日期表达式，如"d-1"代表日期减1
        :return:
        """
        now = datetime.datetime.now().replace(microsecond=0)
        if expr:
            try:
                mark = expr[:1]
                num = int(expr[1:])
            except (TypeError, NameError):
                raise Exception("调用生成日期失败，日期表达式[ %s ]有误！" % expr)
            return self.get_date_mark(now, mark, num)
        else:
            return now

    def generate_timestamp(self, expr='') -> int:
        """生成时间戳(13位)

        :param expr: 日期表达式，如"d-1"代表日期减1
        :return:
        """
        datetime_obj = self.generate_datetime(expr)
        return int(datetime.datetime.timestamp(datetime_obj)) * 1000

    def generate_guid(self) -> str:
        """基于MAC地址+时间戳+随机数来生成GUID

        :param:
        :return:
        """
        import uuid
        return str(uuid.uuid1()).upper()

    def generate_wxid(self):
        """基于AUTO标识+26位英文字母大小写+数字生成伪微信ID

        :param:
        :return:
        """
        return 'AUTO' + ''.join(random.sample(string.ascii_letters + string.digits, 24))

    def generate_noid(self, expr=''):
        """基于6位随机数字+出生日期+4位随机数生成伪身份证

        :param expr: 日期表达式，如"d-1"代表日期减1
        :return:
        """
        # birthday = generate_date(expr)
        # birthday = str(birthday).replace('-', '')
        # return int(str(random.randint(100000, 999999)) + birthday + str(random.randint(1000, 9999)))
        faker = Faker(locale='zh_CN')
        return faker.ssn()

    def generate_phone(self):
        """基于三大运营商号段+随机数生成伪手机号

        :param:
        :return:
        """
        ctcc = [133, 153, 173, 177, 180, 181, 189, 191, 193, 199]
        cucc = [130, 131, 132, 155, 156, 166, 175, 176, 185, 186, 166]
        cmcc = [134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198]
        begin = 10 ** 7
        end = 10 ** 8 - 1
        prefix = random.choice(ctcc + cucc + cmcc)
        return str(prefix) + str(random.randint(begin, end))
