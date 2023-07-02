import orjson


class Json:
    @classmethod
    def dumps(cls, *args, **kwargs):
        return orjson.dumps(*args, **kwargs).decode('utf-8')

    @classmethod
    def loads(cls, *args, **kwargs):
        return orjson.loads(*args, **kwargs)
