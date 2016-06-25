from base.handler import apis


class AdminApiHandler(object):
    pass


class ListHandler(AdminApiHandler, apis.ApiListHandler):
    pass


class DetailHandler(AdminApiHandler, apis.ApiDetailHandler):
    pass


class PositionHandler(AdminApiHandler, apis.ApiPositionHandler):
    pass
