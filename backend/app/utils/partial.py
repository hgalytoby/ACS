import inspect

from pydantic import BaseModel


def optional(*fields):
    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
            if _cls.__fields__[field].default:
                _cls.__fields__[field].default = None
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)
    return dec
