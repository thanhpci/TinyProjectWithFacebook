# from datetime import datetime
# from uuid import UUID
#
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.dialects.postgresql.json import JSONB
# from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TEXT
# from sqlalchemy_utils import UUIDType
#
# from app import db
# import app.utils as utils
# from app.logger import logger
#
#
# class FbCrawler(db.Model):
#     __tablename__ = 'ebds_fb_crawler'
#     id = db.Column(UUIDType(binary=False), primary_key=True, server_default=db.func.uuid_generate_v4())
#     postId = db.Column(VARCHAR, unique=True)
#     groupId = db.Column(VARCHAR, nullable=True, default=None)
#     url = db.Column(TEXT, nullable=True, default=None)
#     isCrawled = db.Column(INTEGER, default=0)
#     createdAtPost = db.Column(db.DateTime, nullable=True, default=None)
#
#     # tag = db.Column(JSONB, nullable=True, default=None)
#     # version = db.Column(JSONB, nullable=True, default=None)
#     status = db.Column(INTEGER, default=0)
#
#     createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return utils.sqlalchemy_object_repr(self)
#
#     @classmethod
#     def query_all_by(cls, filter_data):
#         try:
#             obj = db.session.query(FbCrawler)
#             for field, value in filter_data.items():
#                 obj = obj.filter(getattr(FbCrawler, field) == value)
#             obj = obj.all()
#             db.session.commit()
#             return obj
#         except Exception as e:
#             logger.error('Catched SQLAlchemyError')
#             error = str(e.__dict__['orig'])
#             logger.error(error)
#             db.session.rollback()
#             return None
#
#     @classmethod
#     def query_by(cls, filter_data):
#         try:
#             field = [*filter_data.keys()][0]
#             obj = db.session.query(FbCrawler).filter(getattr(FbCrawler, field) == filter_data[field]).first()
#             db.session.commit()
#             return obj
#         except:
#             db.session.rollback()
#             return None
#
#     @classmethod
#     def insert(cls, data):
#         try:
#             # print('data in insert:', data)
#             fb_post = db.session.query(FbCrawler).filter(FbCrawler.postId == data['postId']).first()
#             # print('fb_post', fb_post)
#             if fb_post is not None:
#                 for k in data.keys():
#                     if k == 'status':
#                         if data.get(k) == 1 and getattr(fb_post, k) == 0:
#                             setattr(fb_post, k, data[k])
#                     if getattr(fb_post, k) is None and data.get(k) is not None:
#                         setattr(fb_post, k, data[k])
#                 db.session.commit()
#                 logger.info(f"Updated fb crawler")
#                 return fb_post.id
#             try:
#                 fb_post = cls(**data)
#             except:
#                 return True
#             db.session.add(fb_post)
#             db.session.commit()
#         except SQLAlchemyError as e:  # UniqueViolation
#             logger.error('Catched SQLAlchemyError')
#             # error = str(e.__dict__['orig'])
#             logger.error(e)
#             db.session.rollback()
#             return
#         except Exception as e:
#             logger.error(str(e))
#             return
#         logger.info(f"Imported fb crawler")
#         # fb_post_obj = FbCrawler.query_by({'fbId': data['fbId']})
#         return True
#
#     @classmethod
#     def insert_or_update(cls, data):
#         try:
#             fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
#             if fb_post_obj.extracted == 1:
#                 return fb_post_obj.id
#             try:
#                 profile = cls(**data)
#             except:
#                 return True
#             db.session.add(profile)
#             db.session.commit()
#         except SQLAlchemyError as e:  # UniqueViolation
#             logger.error('Catched SQLAlchemyError')
#             error = str(e.__dict__['orig'])
#             logger.error(error)
#             db.session.rollback()
#             fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
#             return fb_post_obj.id
#         except Exception as e:
#             logger.error(str(e))
#             return
#         logger.info(f"Imported fb crawler")
#         return profile.id
#
#     @classmethod
#     def create_or_update_from_json(cls, profile_json):
#         try:
#             fbuid = list(profile_json)[0]
#             data = profile_json[fbuid]
#             mapping = {'id': 'fbuid'}
#             data = utils.rename_keys(data, mapping)
#             if 'fbuid' not in data:
#                 data['fbuid'] = fbuid
#             try:
#                 profile = cls(**data)
#             except:
#                 return True
#             db.session.add(profile)
#             db.session.commit()
#         except SQLAlchemyError as e:  # UniqueViolation
#             logger.error('Catched SQLAlchemyError')
#             error = str(e.__dict__['orig'])
#             logger.error(error)
#             db.session.rollback()
#             return
#         except Exception as e:
#             logger.error(str(e))
#             return
#         logger.info(f"Imported profile #{profile.id} ({profile.fbuid})")
#         return True
#
#     # thuytt
#     @classmethod
#     def update_status(cls, data):
#         try:
#             fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.id == data['id']).first()
#             fb_post_obj.update().values(status=data['status'])
#
#             db.session.commit()
#         except SQLAlchemyError as e:  # UniqueViolation
#             logger.error('Catched SQLAlchemyError')
#             error = str(e.__dict__['orig'])
#             logger.error(error)
#             db.session.rollback()
#             fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
#             return fb_post_obj.id
#         except Exception as e:
#             logger.error(str(e))
#             return
#         logger.info(f"Update status fb crawler")
#         return fb_post_obj.id
