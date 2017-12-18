# -*- coding: utf-8 -*-


import json


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+') as f:
        f.write(s)


def load(path):
    with open(path, 'r') as f:
        s = f.read()
        return json.loads(s)


class Model(object):

    @classmethod
    def db_path(cls):
        subject = cls.__name__
        path = 'data/%s.txt' % subject
        return path

    @classmethod
    def all(cls, thing):
        path = cls.db_path()
        models = load(path)
        ms = models['%s' % thing]
        return ms