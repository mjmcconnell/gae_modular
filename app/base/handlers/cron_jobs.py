# local imports
from base.handlers.common import BaseHandler
from base.handlers.common import SecurityError


class BaseCronHandler(BaseHandler):
    """Base handler for servicing Cron requests.
    """

    def dispatch(self):
        """Ensure the "X-Appengine-Cron" header is set to "true"

        Ref: (https://cloud.google.com/appengine/docs/python/config/cron
        #securing_urls_for_cron)
        """
        header = self.request.headers.get('X-AppEngine-Cron', 'false')
        if header != 'true':
            raise SecurityError('X-AppEngine-Cron header missing')
        super(BaseCronHandler, self).dispatch()
