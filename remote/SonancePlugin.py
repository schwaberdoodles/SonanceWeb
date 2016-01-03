from bottle import HTTPError
from SonanceClient import SonanceRemote, SonanceQuery
import inspect

class SonanceQueryPlugin(object):
    ''' This plugin passes an SonanceClient handle to route callbacks. You can override the database
    settings on a per-route basis. '''

    name = 'sonance'
    api = 2

    def __init__(self, host="172.16.1.80", port=7777, keyword='sonance_client'):
        self.host = host
        self.port = port
        self.keyword = keyword
        self.r = SonanceRemote()

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, SonancePlugin): continue
            if other.host == self.host:
                raise PluginError("Found another sonance plugin attached to the same host...")

    def apply(self, callback, context):
        conf = context.config.get('sonance') or {}
        keyword = conf.get('keyword', self.keyword)
        self.r.connect()
        query = SonanceQuery(self.r)
        args = inspect.getargspec(context.callback)[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs['sonance_query'] = query
            try:
                rv = callback(*args, **kwargs)
            except Exception as e:
                raise HTTPError(500, "Sonance Error from class %s" % e.message, e)
            finally:
                self.r.disconnect()
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper
