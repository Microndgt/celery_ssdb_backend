Celery SSDB Backend
===================

Introduction
------------

Celery's custom result backend for SSDB

The task meta data can be kept in a SSDB key-value.

(Tested with Celery 4.1)

Why not redis backend?
----------------------

using redis as backend will exec some redis commands which ssdb doesn't support. Nevertheless, this SSDB backend is very simple.

Usage
-----

- Copy ssdb_backend.py to your Celery project.
- monkey patch the celery app's `backend_cls` where you create celery app

```
celery = Celery(app.__name__, broker='pyamqp://{}:{}@{}:{}/{}'.format(RM_USER, RM_PWD, RM_HOST, RM_PORT, RM_VHOST))
celery.backend_cls = 'backend.ssdb.SSDBBackend'
```

- Add the following to `celery_settings.py`

```
CELERY_SSDB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 8888,
    "password": "",
    "expires": 0
}
CELERY_RESULT_SERIALIZER = 'json'
```

- Then start your app

Licence
=======

- MIT