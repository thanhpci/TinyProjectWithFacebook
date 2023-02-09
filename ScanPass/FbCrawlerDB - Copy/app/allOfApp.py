import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging import getLogger, StreamHandler, INFO, Formatter
from collections import OrderedDict
from sqlalchemy.dialects import postgresql
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TEXT
from sqlalchemy_utils import UUIDType

# ====================
from sqlalchemy.dialects.postgresql import UUID



dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, verbose=True)



flask_app = Flask(__name__)

# Configurations
BASE_DIR = os.path.abspath(os.curdir)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI") # set config postgres

flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
flask_app.config["flask_profiler"] = {
    "enabled": True,
    "storage": {
        "engine": "sqlalchemy",
        "db_url": os.environ.get("SQLALCHEMY_DATABASE_URI")
    },
    "ignore": [
        "^/static/.*"
    ]
}

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db, compare_type=True)

# Import models to create tables


logger = getLogger("json2postgres")
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

def rename_keys(dictionary, mapping):
    for old_key, new_key in mapping.items():
        if old_key in dictionary:
            dictionary[new_key] = dictionary.pop(old_key)
        # else:
            # logger.error(f"{old_key} not exists!")
            # logger.error(dictionary)

    return dictionary


def sqlalchemy_object_to_dict(obj):
    """ Return the object's dict excluding private attributes,
    sqlalchemy state and relationship attributes.
    """
    excl = ('_sa_adapter', '_sa_instance_state')
    d = OrderedDict({'id': obj.id})

    if 'fbuid' in vars(obj).keys():
        d.update({'fbuid': obj.fbuid})
    d.update({k: v for k, v in vars(obj).items() if not k.startswith('_')
            and k not in ['id', 'fbuid', 'created_at', 'updated_at']
            and not any(hasattr(v, a) for a in excl)})
    d.update({'created_at': obj.created_at, 'updated_at': obj.created_at})

    return d

def sqlalchemy_object_repr(obj):
    delimiter = "\n-----------------------------------------------------\n"
    params = delimiter.join(f'{k}={v}' for k, v in sqlalchemy_object_to_dict(obj).items())
    return f"{obj.__class__.__name__}({params})"


def debug_sql(query):
    return print(str(query.statement.compile(dialect=postgresql.dialect())))



class FbCrawler(db.Model):
    __tablename__ = 'ebds_fb_crawler'
    id = db.Column(UUIDType(binary=False), primary_key=True, server_default=db.func.uuid_generate_v4())
    # UUIDType.cache_ok = False
    postId = db.Column(VARCHAR, unique=True)
    groupId = db.Column(VARCHAR, nullable=True, default=None)
    url = db.Column(TEXT, nullable=True, default=None)
    isCrawled = db.Column(INTEGER, default=0)
    createdAtPost = db.Column(db.DateTime, nullable=True, default=None)
    contentPost = db.Column(VARCHAR, nullable=True, default=None)

    tag = db.Column(VARCHAR, default=None)
    # version = db.Column(JSONB, nullable=True, default=None)
    status = db.Column(INTEGER, default=0)

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return sqlalchemy_object_repr(self)

    @classmethod
    def query_all_by(cls, filter_data):
        try:
            obj = db.session.query(FbCrawler)
            for field, value in filter_data.items():
                obj = obj.filter(getattr(FbCrawler, field) == value)
            obj = obj.all()
            db.session.commit()
            return obj
        except Exception as e:
            logger.error('Catched SQLAlchemyError')
            error = str(e.__dict__['orig'])
            logger.error(error)
            db.session.rollback()
            return None

    @classmethod
    def query_by(cls, filter_data):
        try:
            field = [*filter_data.keys()][0]
            obj = db.session.query(FbCrawler).filter(getattr(FbCrawler, field) == filter_data[field]).first()
            db.session.commit()
            return obj
        except:
            db.session.rollback()
            return None

    @classmethod
    def insert(cls, data):
        try:
            with flask_app.app_context():
                # print('data in insert:', data)
                fb_post = db.session.query(FbCrawler).filter(FbCrawler.postId == data['postId']).first()
                # print('fb_post', fb_post)
                if fb_post is not None:
                    for k in data.keys():
                        if k == 'status':
                            if data.get(k) == 1 and getattr(fb_post, k) == 0:
                                setattr(fb_post, k, data[k])
                        if getattr(fb_post, k) is None and data.get(k) is not None:
                            setattr(fb_post, k, data[k])
                    db.session.commit()
                    logger.info(f"Updated fb crawler")
                    return fb_post.id
                try:
                    fb_post = cls(**data)
                except:
                    return True
                db.session.add(fb_post)
                db.session.commit()
        except SQLAlchemyError as e:  # UniqueViolation
            logger.error('Catched SQLAlchemyError')
            # error = str(e.__dict__['orig'])
            logger.error(e)
            db.session.rollback()
            return
        except Exception as e:
            logger.error(str(e))
            return
        logger.info(f"Imported fb crawler")
        # fb_post_obj = FbCrawler.query_by({'fbId': data['fbId']})
        return True




    def update_content_post(cls, data):
        try:
            with flask_app.app_context():
                fb_post = db.session.query(FbCrawler).filter(FbCrawler.postId == data['postId']).first()
                if fb_post is not None:
                    content = 'contentPost'
                    updatedAt = 'updatedAt'
                    flag = 'isCrawled'
                    if getattr(fb_post, content) is not None and data.get(k) is not None:
                        setattr(fb_post, flag, data[flag])
                        setattr(fb_post, content, data[content])
                        setattr(fb_post, updatedAt, data[updatedAt])

                        logger.info(f"Updated fb crawler")

                    if getattr(fb_post, content) is None and data.get(content) is not None:
                        setattr(fb_post, flag, data[flag])
                        setattr(fb_post, content, data[content])
                        setattr(fb_post, updatedAt, data[updatedAt])

                        logger.info(f"Imported fb crawler")
                    db.session.commit()
        except SQLAlchemyError as e:  # UniqueViolation
            logger.error('Catched SQLAlchemyError')
            # error = str(e.__dict__['orig'])
            logger.error(e)
            db.session.rollback()
            return
        except Exception as e:
            logger.error(str(e))
            return
        # return True



    @classmethod
    def insert_or_update(cls, data):
        try:
            fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
            if fb_post_obj.extracted == 1:
                return fb_post_obj.id
            try:
                profile = cls(**data)
            except:
                return True
            db.session.add(profile)
            db.session.commit()
        except SQLAlchemyError as e:  # UniqueViolation
            logger.error('Catched SQLAlchemyError')
            error = str(e.__dict__['orig'])
            logger.error(error)
            db.session.rollback()
            fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
            return fb_post_obj.id
        except Exception as e:
            logger.error(str(e))
            return
        logger.info(f"Imported fb crawler")
        return profile.id

    @classmethod
    def create_or_update_from_json(cls, profile_json):
        try:
            fbuid = list(profile_json)[0]
            data = profile_json[fbuid]
            mapping = {'id': 'fbuid'}
            data = rename_keys(data, mapping)
            if 'fbuid' not in data:
                data['fbuid'] = fbuid
            try:
                profile = cls(**data)
            except:
                return True
            db.session.add(profile)
            db.session.commit()
        except SQLAlchemyError as e:  # UniqueViolation
            logger.error('Catched SQLAlchemyError')
            error = str(e.__dict__['orig'])
            logger.error(error)
            db.session.rollback()
            return
        except Exception as e:
            logger.error(str(e))
            return
        logger.info(f"Imported profile #{profile.id} ({profile.fbuid})")
        return True

    # thuytt
    @classmethod
    def update_status(cls, data):
        try:
            fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.id == data['id']).first()
            fb_post_obj.update().values(status=data['status'])

            db.session.commit()
        except SQLAlchemyError as e:  # UniqueViolation
            logger.error('Catched SQLAlchemyError')
            error = str(e.__dict__['orig'])
            logger.error(error)
            db.session.rollback()
            fb_post_obj = db.session.query(FbCrawler).filter(FbCrawler.fbId == data['fbId']).first()
            return fb_post_obj.id
        except Exception as e:
            logger.error(str(e))
            return
        logger.info(f"Update status fb crawler")
        return fb_post_obj.id
