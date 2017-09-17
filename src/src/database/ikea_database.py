# coding:utf-8
'''
Created on 2017/9/3 下午11:08

@author: liucaiquan
'''
import pandas as pd
import global_common_params
import database_params
import re


class IkeaDatabase(object):
    '''
        IKEA数据库管理
    '''

    def __init__(self):
        # 最大的item书面
        self.goods_database_path = global_common_params.project_root_path + '/static/data.csv'
        self.goods_data = pd.read_csv(self.goods_database_path)

        self.location_database_path = global_common_params.project_root_path + '/static/locations.csv'
        self.location_data = pd.read_csv(self.location_database_path)

        self.departments_database_path = global_common_params.project_root_path + '/static/departments.csv'
        self.departments_data = pd.read_csv(self.departments_database_path)

    '''
        位置查询
            intent_name:位置/意图名字
            返回值：位置索引值（整型）和位置的描述信息
    '''

    def find_location(self, intent_name):
        # 返回所有返回值的第一个
        # return self.location_data[self.location_data.location == intent_name][database_params.index].values[0]
        for index in self.departments_data.index:
            departments = self.departments_data.loc[index][database_params.department]
            if departments.find(intent_name) != -1:
                return self.departments_data.loc[index][database_params.index], self.departments_data.loc[index][
                    database_params.description]

            intent = str(self.departments_data.loc[index][database_params.intent])
            # print 'intent= ', intent
            if intent.find(intent_name) != -1:
                return self.departments_data.loc[index][database_params.index], self.departments_data.loc[index][
                    database_params.description]

        # 没有位置正确的位置信息
        return -1, ''

    '''
        以商品是否为最新，是否打折为过滤条件进行商品查找
            goods_name:需要查询的商品名
            filter：商品过滤条件
            返回值：符合条件的商品信息（list）
    '''

    def __find_goods_new_discount(self, goods_name, goods_filter):
        rst = []
        for index in self.goods_data.index:
            row = self.goods_data.loc[index]
            if (row[database_params.goods_name].find(goods_name) != -1):
                # 商品是否为最新的
                if goods_filter == database_params.goods_newest:
                    if row[database_params.goods_newest] == 'False':
                        continue

                # 商品是否为打折的
                if goods_filter == database_params.goods_discount:
                    if row[database_params.goods_discount] == 'False':
                        continue

                item = {}
                item[database_params.goods_name] = row[database_params.goods_name]
                item[database_params.goods_link] = row[database_params.goods_link]
                item[database_params.goods_broad] = row[database_params.goods_broad]
                item[database_params.goods_price] = row[database_params.goods_price]
                rst.append(item)
        return rst

    '''
        以价格高低进行排序，并进行商品查找
            goods_name:需要查询的商品名
            filter：商品过滤条件
            返回值：符合条件的商品信息（list）
    '''

    def __find_goods_price(self, goods_name, goods_filter):
        rst = []
        for index in self.goods_data.index:
            row = self.goods_data.loc[index]
            if (row[database_params.goods_name].find(goods_name) != -1):
                item = {}
                item[database_params.goods_name] = row[database_params.goods_name]
                item[database_params.goods_link] = row[database_params.goods_link]
                item[database_params.goods_broad] = row[database_params.goods_broad]

                price = row[database_params.goods_price]

                print 'type(price):', type(price)
                print 'raw price= ', price
                price = re.sub('[^0-9.,]', '', price)
                price = price.replace(',', '')

                print 'price=', price
                print 'len(price)=', len(price)
                for i in range(len(price)):
                    print'char= ', price[i]

                price_float = float(price)
                item[database_params.goods_price] = price_float
                rst.append(item)

        rst.sort(key=lambda obj: obj.get(database_params.goods_cheap), reverse=False)

        return rst

    '''
        商品信息查询
            goods_name:需要查询的商品名
            filter：商品过滤条件
            返回值：符合条件的商品信息（list）
    '''

    def find_goods(self, goods_name, goods_filter):
        print 'filter= ', filter

        if goods_filter == database_params.goods_cheap:
            return self.__find_goods_price(goods_name, goods_filter)
        else:
            return self.__find_goods_new_discount(goods_name, goods_filter)

    def test(self):
        print type(self.goods_data.category)