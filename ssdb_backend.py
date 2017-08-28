from celery.backends.base import KeyValueStoreBackend
from celery.exceptions import ImproperlyConfigured
from celery.utils.time import maybe_timedelta
from kombu.utils import cached_property

try:
    import pyssdb as ps
except ImportError:
    ps = None


class SSDBBackend(KeyValueStoreBackend):
    host = "127.0.0.1"
    port = 8888
    password = ""
    supports_autoexpire = True

    _connection = None

    def __init__(self, *args, **kwargs):
        super(SSDBBackend, self).__init__(*args, **kwargs)
        _get = self.app.conf.get
        if not ps:
            raise ImproperlyConfigured(
                'You need to install the pyssdb_customized library to use the '
                'ssdb backend.')

        config = _get('CELERY_SSDB_BACKEND_SETTINGS')
        if config is not None:
            if not isinstance(config, dict):
                raise ImproperlyConfigured(
                    'SSDB backend settings should be grouped in a dict')
            config = dict(config)  # do not modify original

            self.host = config.pop('host', self.host)
            self.port = config.pop('port', self.port)
            self.password = config.pop('password', self.password)
            self.expires = maybe_timedelta(config.pop('expires', self.app.conf.CELERY_TASK_RESULT_EXPIRES))

    def _get_connection(self):
        if self._connection is None:
            self._connection = ps.Client(host=self.host, port=self.port, password=self.password)

        return self._connection

    def process_cleanup(self):
        if self._connection is not None:
            self._connection.disconnect()
            self._connection = None

    def set(self, key, value):
        if self.expires:
            self.conn.setx(key, value, self.expires)
        else:
            self.conn.set(key, value)

    def get(self, key):
        return self.conn.get(key)

    def delete(self, key):
        self.conn.delete(key)

    def incr(self, key):
        return self.conn.incr(key)

    def expire(self, key, value):
        return self.conn.expire(key, value)

    @cached_property
    def conn(self):
        """Get RethinkDB connection."""
        conn = self._get_connection()
        return conn
