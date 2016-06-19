from base.handler import apis


class PageApiHandler(object):
    pass


class AdminApiListHandler(PageApiHandler, apis.ApiListHandler):
    pass


class AdminApiDetailHandler(PageApiHandler, apis.ApiDetailHandler):
    pass


class AdminApiPositionHandler(PageApiHandler, apis.ApiPositionHandler):
    pass
