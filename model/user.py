# -*- coding:utf-8 -*-
import baosteelpipe.model.model as model
import baosteelpipe.libs.utils as utils
from baosteelpipe.libs.utils import options

class UserModel(model.BaseModel,model.Singleton):
    __name = "dxb.user"

    def __init__(self):
        model.BaseModel.__init__(self,UserModel.__name)

    def register(self,mobile,password):
        if mobile is None or password is None:
            raise ValueError(u"用户或者密码为空")
        user = self.coll.find_one({"mobile":mobile})
        if user is not None:
            raise ValueError(u"手机号已被注册！")
        _user = {}
        _user['mobile'] = mobile
        _user['password']=password
        self.coll.save(_user)
        return utils.dump(_user)
