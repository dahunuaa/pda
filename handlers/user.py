# -*- coding:utf-8 -*-
from baosteelpipe.handler import APIHandler
import baosteelpipe.libs.utils as utils
import baosteelpipe.model.user as user_model

class UserHandler(APIHandler):
    _model = "user.UserModel"
    def post(self):
        result = utils.init_response_data()
        user_model_obj = user_model.UserModel()
        try:
            user_id = self.get_argument("user_id","")
            password = self.get_argument("password","")
            user=user_model_obj.register(user_id,password)
            result["data"]=utils.dump(user)
        except Exception as e:
            result = utils.reset_response_data(0,str(e))
        self.finish(result)

handlers = [(r"/api/user/register",UserHandler)

            ]



