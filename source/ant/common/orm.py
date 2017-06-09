
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
    
    def insert(self):
        with Connection():
            res = db_insert(self._table_name_, self)

        return res and True or False
    
    @classmethod
    def _get_condition_expr(cls, key, value_list):
        if isinstance(value_list, list):
            cond_list = ['='.join([key, value.__repr__()]) for value in value_list]
            return '(' + ' OR '.join(cond_list) + ')'
        else:
            return '(' + '='.join([key, value_list.__repr__()]) + ')'

    @classmethod
    def get(cls, **var_dict):

        cond_list = [cls._get_condition_expr(k, v)
                for k, v in var_dict.items()]
        str_condition = ' AND '.join(cond_list)
        col_list = '*'

        with Connection():
            res = db_select(cls._table_name_, col_list, str_condition)
        log_debug('orm fetch result: {}'.format(res))

    
    @classmethod
    def get_with_cond(cls, **var_dict):
        pass
