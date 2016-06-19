# local imports
from base.handlers.common import BaseHandler
from base.handlers.common import SecurityError


class BaseTaskHandler(BaseHandler):
    """Base handler for task requests.
    """

    def dispatch(self):
        """Ensure a valid "X-Appengine-Cron" header is passed in the requests

        Ref: (https://cloud.google.com/appengine/docs/python/taskqueue/push/
        creating-handlers#securing_task_handler_urls)
        """
        header = self.request.headers.get('X-AppEngine-QueueName', None)
        if not header:
            raise SecurityError('X-AppEngine-QueueName header missing')
        super(BaseTaskHandler, self).dispatch()
