
class ModelMeta(type):
    def __new__(cls, name, parents, attrs):
        print attrs
        attrs['test'] = 1000
        return type.__new__(cls, name, parents, attrs)

class Model(dict):
    __metaclass__ = ModelMeta

    def __init__(self, **keys):
        dict.__init__(self, **keys)

class DemoEmployee(Model):
    __table_name__ = 'demo_employee'
    name = StringField()

if __name__ == '__main__':
    print User.a, User.test
    u = User(111)
    print u.a, u.test
