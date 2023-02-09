# from app.logger import logger
# from collections import OrderedDict
# from sqlalchemy.dialects import postgresql
#
#
# def rename_keys(dictionary, mapping):
#     for old_key, new_key in mapping.items():
#         if old_key in dictionary:
#             dictionary[new_key] = dictionary.pop(old_key)
#         # else:
#             # logger.error(f"{old_key} not exists!")
#             # logger.error(dictionary)
#
#     return dictionary
#
#
# def sqlalchemy_object_to_dict(obj):
#     """ Return the object's dict excluding private attributes,
#     sqlalchemy state and relationship attributes.
#     """
#     excl = ('_sa_adapter', '_sa_instance_state')
#     d = OrderedDict({'id': obj.id})
#
#     if 'fbuid' in vars(obj).keys():
#         d.update({'fbuid': obj.fbuid})
#     d.update({k: v for k, v in vars(obj).items() if not k.startswith('_')
#             and k not in ['id', 'fbuid', 'created_at', 'updated_at']
#             and not any(hasattr(v, a) for a in excl)})
#     d.update({'created_at': obj.created_at, 'updated_at': obj.created_at})
#
#     return d
#
# def sqlalchemy_object_repr(obj):
#     delimiter = "\n-----------------------------------------------------\n"
#     params = delimiter.join(f'{k}={v}' for k, v in sqlalchemy_object_to_dict(obj).items())
#     return f"{obj.__class__.__name__}({params})"
#
#
# def debug_sql(query):
#     return print(str(query.statement.compile(dialect=postgresql.dialect())))
