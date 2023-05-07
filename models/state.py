#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    bck_ref = backref('state', cascade='all, delete-orphan')
    cities = relationship('City', backref=bck_ref)

    @property
    def cities(self):
        """
        Returns the list of 'City' instances with state_id
        equal to the current State.id
        """
        city_list = []
        city_values = models.storage.all('City').values()
        for city in city_values:
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
