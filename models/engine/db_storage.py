#!/usr/bin/python3
"""DB Storage engine using SQLAlchemy"""
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class_map = {
    'User': User,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review
}


class DBStorage:
    """DBStorage class"""
    __engine: None
    __session: None

    def __init__(self):
        """Initializes DBStorage"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                    .format(user, passwd, host, db),
                                    pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects that are present"""
        if cls is None:
            cls_list = [classes[key] for key in class_map.keys()]
        else:
            cls_list = [cls]

        objects = {}
        for c in cls_list:
            for obj in self.__session.query(c):
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """Add the specified object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session 'obj' if not 'None'"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads objects from the database"""
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Closes current session if active"""
        self.__session.close()
