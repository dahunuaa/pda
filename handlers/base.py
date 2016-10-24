# -*- coding: utf-8 -*-

"""
    author : youfaNi
    date : 2016-08-24
"""

import json,pdb
import datetime
import tornado
import urllib,copy
from dxb.handler import TokenAPIHandler
from baosteelpipe.handler import APIHandler
import baosteelpipe.libs.utils as utils
import baosteelpipe.libs.reportlib as reportlib
from baosteelpipe import status

class ListCreateAPIHandler(APIHandler):#method post
    mp_require_params = []
    mp_default_params = {}
    mp_query_parmas = [] #联合主键
    mp_update_or_raise = "update" #如果存在则更新，“raise”:如果存在则抛出异常

    response_extra_params = []  # 返回数据额外字段

    def initialize(self):
        # method get
        self.mg_query_params = {}

        super(ListCreateAPIHandler, self).initialize()

    def get(self):
        result = utils.init_response_data()
        self.model.extra_params = self.response_extra_params
        try:
            page = self.get_argument("page", 1)
            page_size = self.get_argument("page_size", 10)
            time_desc = self.get_argument("time_desc", "all")
            start_time = self.get_argument("start_time", None)
            end_time = self.get_argument("end_time", None)
            if time_desc != "all":
                start_time, end_time = self._get_search_time(time_desc, start_time, end_time)
                self.mg_query_params.update({
                    "add_time": {
                        "$gte": str(start_time),
                        "$lte": str(end_time),
                    }
                })
            objs, pager = self.model.search_list(page=page, page_size=page_size, query_params=self.mg_query_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)

    def post(self):
        result = utils.init_response_data()
        self.model.extra_params = self.response_extra_params
        try:
            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()
            exec("""request_params = self.mp_default_params.update(%s)"""%request_params)
            request_params = self.mp_default_params
            query_params = {}
            for key in self.mp_query_params:
                query_params.update({
                    key:request_params[key],
                })

            if query_params == {} or not self.model.is_exists(query_params):
                obj = self.model.create(**request_params)
                result["data"] = utils.dump(obj)
            else:
                if self.mp_update_or_raise == "update":
                    obj = self.model.search(query_params)
                    query_params = {"_id":utils.create_objectid(obj["_id"])}
                    result["data"] = self.model.update(query_params,request_params)
                else:
                    raise Exception("已存在！")
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class RetrieveUpdateDestroyAPIHandler(APIHandler):
    mg_extra_params = [] # 返回数据额外字段
    mp_require_params = []  # put 方法必要参数
    mp_update_params = []  # put 方法允许参数

    def initialize(self):
        self.mp_query_params = {}
        super(RetrieveUpdateDestroyAPIHandler, self).initialize()

    def get(self):
        result = utils.init_response_data()
        self.model.extra_params = self.mg_extra_params
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)
            ret = self.model.search({"_id": _id})
            if ret:
                result["data"] = ret
            else:
                result["data"] = {}
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def put(self):
        result = utils.init_response_data()
        try:
            id = self.get_argument("id")
            _id = utils.create_objectid(id)
            self.mp_query_params.update({
                "_id":_id,
            })

            self.check_request_params(self.mp_require_params)
            request_params = self.format_request_params()

            update_params = {}
            exec ("""update_params.update(%s)""" % request_params)
            self.check_update_params(update_params)
            update_params["_id"] = _id
            del update_params["id"]

            ret = self.model.update(query_params=self.mp_query_params, update_params=update_params)
            result['data'] = ret
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

    def check_update_params(self,update_params):
            update_params_keys = update_params.keys()
            for param in update_params:
                if param not in self.mp_update_params:
                    raise Exception("无法修改：%s!"%param)

    def delete(self):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                self.model.update({"_id": utils.create_objectid(_id)}, {"order_status": status.ORDER_STATUS_DELETE})
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class DestroyAPIHandler(APIHandler):

    def delete(self):
        result = utils.init_response_data()
        try:
            ids = json.loads(self.get_argument("ids"))
            _ids = [utils.create_objectid(id) for id in ids]
            for _id in _ids:
                self.model.update({"_id":utils.create_objectid(_id)},{"order_status":status.ORDER_STATUS_DELETE})
        except Exception, e:
            result = utils.reset_response_data(0, str(e))

        self.finish(result)

class ListAPIHandler(APIHandler):
    response_extra_params = []  # 返回数据额外字段

    def initialize(self):
        # method get
        self.mg_query_params = {}

        super(ListAPIHandler, self).initialize()

    def get(self):
        result = utils.init_response_data()
        self.model.extra_params = self.response_extra_params
        try:
            page = self.get_argument("page", 1)
            page_size = self.get_argument("page_size", 10)
            time_desc = self.get_argument("time_desc", "all")
            start_time = self.get_argument("start_time", None)
            end_time = self.get_argument("end_time", None)
            if time_desc != "all":
                start_time, end_time = self._get_search_time(time_desc, start_time, end_time)
                self.mg_query_params.update({
                    "add_time": {
                        "$gte": str(start_time),
                        "$lte": str(end_time),
                    }
            })
            objs, pager = self.model.search_list(page=page,page_size=page_size,query_params=self.mg_query_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)
    def post(self):
        raise Exception("method not access")

class ListISOAPIHandler(APIHandler):
    response_extra_params = []  # 返回数据额外字段

    def initialize(self):
        # method get
        self.mg_query_params = {}

        super(ListISOAPIHandler, self).initialize()

    def get(self):
        result = utils.init_response_data()
        self.model.extra_params = self.response_extra_params
        try:
            page = self.get_argument("page", 1)
            page_size = self.get_argument("page_size", 10)
            time_desc = self.get_argument("time_desc", "all")
            start_time = self.get_argument("start_time", None)
            end_time = self.get_argument("end_time", None)
            if time_desc != "all":
                start_time, end_time = self._get_search_time(time_desc, start_time, end_time)
                self.mg_query_params.update({
                    "add_time": {
                        "$gte": start_time,
                        "$lte": end_time,
                    }
            })
            objs, pager = self.model.search_list(page=page,page_size=page_size,query_params=self.mg_query_params)
            result["data"] = objs
            result["pager"] = pager
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.finish(result)
            return
        self.finish(result)
    def post(self):
        raise Exception("method not access")

class ReportHandler(APIHandler):
    _model = "order.OrderModel"
    mg_query_params = {} # get 方法查询参数
    mg_sort_params = {}  # get 方法排序字段
    namelist = [u'序号'] # 报表表头
    column_list = [] #报表表头字段
    report_name = "报表" #报表名

    def get(self):
        try:
            obj_list, pager = self.model.search_list(query_params=self.mg_query_params, pager_flag=False)
            namelist = self.namelist
            column_list = self.column_list
            if len(namelist) != len(column_list) + 1:
                raise Exception("namelist and column_list 长度不一致")
            elif len(column_list) == 0 and len(namelist) == 1:
                if len(obj_list) > 0:
                    obj = obj_list[0]
                    namelist = self.namelist + obj.keys()
                    column_list = obj.keys()

            curr_time = str(datetime.datetime.now())
            report_china_name = "%s%s" % (
                self.report_name, curr_time.replace(".", "-").replace(" ", "-").replace(":", "-"))
            format_column_list = ["%s:None"%column for column in column_list]
            column_dict = {}
            map(lambda x: column_dict.setdefault(x.split(':')[0], x.split(':')[1]), format_column_list)
            temp_column_dict = column_dict
            export_list = []
            for obj in obj_list:
                for column in column_list:
                    if obj.has_key(column):
                        temp_column_dict[column] = obj[column]
                    else:
                        try:
                            temp_column_dict[column] = getattr(self.model, "get_%s" % column)(obj)
                        except:
                            temp_column_dict[column] = ""

                export_list.append(copy.copy(temp_column_dict))
                temp_column_dict = column_dict
            if len(export_list) > 0:
                fieldlist = column_list
            else:
                fieldlist = []
            result = reportlib.export_excel(report_china_name=[report_china_name], namelist=[namelist],
                                              result=[export_list], fieldlist=[fieldlist], )
            file_names = result['filename']
            file_paths = result["file_path"]
            report_data = result["report_data"]
        except Exception, e:
            result = utils.reset_response_data(0, str(e))
            self.write(result)
            self.finish()
            return
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_names[0])
        with open(file_paths[0], 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        self.finish()
