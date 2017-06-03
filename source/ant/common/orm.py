
class ModelMeta(type):
    def __new__(cls, name, parents, attrs):
        print attrs
        attrs['test'] = 1000
        return type.__new__(cls, name, parents, attrs)

class Model(dict):
    __metaclass__ = ModelMeta

    def __init__(self, **keys):
        dict.__init__(self, **keys)

class User(Model):
    a = 1

if __name__ == '__main__':
    print User.a, User.test
    u = User()
    print u.a, u.test
