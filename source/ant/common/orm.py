
from ant.common.dbapi import *
from ant.common.log import *

class MetaModel(type):

    def __new__(cls, name, parents, attrs):
        cls._table_name_ = name.lower()
        _table_name_ = cls._table_name_
        _pk_field_ = None
        _field_def_ = {}

        for var_name in attrs:
            if var_name.startswith('_'):
                continue
            if isinstance(attrs[var_name], DataBaseField):
                if attrs[var_name].is_pk:
                    _pk_field_ = var_name
                _field_def_[var_name] = attrs[var_name]
        
        attrs['_table_name_'] = _table_name_
        attrs['_pk_field_'] = _pk_field_
        attrs['_field_def_'] = _field_def_

        return type.__new__(cls, name, parents, attrs)

class Model(dict):
    __metaclass__ = MetaModel

    def __init__(self, **keys):
        dict.__init__(self, **keys)
    
    @classmethod
    def to_str(cls):
        return ';'.join([
            'model name={}',
            'fields={}',
        ]).format(cls._table_name_, cls._field_def_)
    
    def insert(self):
        with Connection():
            res = db_insert(self._table_name_, self)

        return res and True or False

    @classmethod
    def create(cls):
        with Connection():
            res = db_create_table(cls._table_name_, cls._field_def_)
        
        if res:
            return True
        else:
            return False
    
    @classmethod
    def _get_condition_expr(cls, key, value_list):
        if isinstance(value_list, list):
            cond_list = ['='.join([key, value.__repr__()]) for value in value_list]
            return '(' + ' OR '.join(cond_list) + ')'
        else:
            return '(' + '='.join([key, value_list.__repr__()]) + ')'

    @classmethod
    def _find_result(cls, **var_dict):
        cond_list = [cls._get_condition_expr(k, v)
                for k, v in var_dict.items()]
        str_condition = ' AND '.join(cond_list)
        col_list = ', '.join(cls._field_def_.keys())

        with Connection():
            res = db_select(cls._table_name_, col_list, str_condition)
        log_debug('orm fetch result: {}'.format(res))
        return res

    @classmethod
    def find_all(cls, **var_dict):
        res = cls._find_result(**var_dict)
        if res == None or len(res) == 0:
            return None

        models = []
        for entry in res:
            cursor = 0
            attrs = {}
            for key in cls._field_def_.keys():
                attrs[key] = entry[cursor]
                cursor += 1
            
            models.append(cls(**attrs))

        return models
    
    @classmethod
    def find_one(cls, **var_dict):
        res = cls._find_result(**var_dict)
        if res == None or len(res) == 0:
            return None
        
        cursor = 0
        attrs = {}
        for key in cls._field_def_.keys():
            attrs[key] = res[0][cursor]
            cursor += 1

        return cls(**attrs)
    
    @classmethod
    def find_with_cond(cls, **var_dict):
        pass
