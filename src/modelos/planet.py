import os
from ..db import db


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    climate = db.Column(db.String(50), nullable=True)
    orbital_period = db.Column(db.String(50), nullable=True)
    rotation_period = db.Column(db.String(50), nullable=True)
    diameter = db.Column(db.String(50), nullable=True)
    url_imagen = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Planets %r>' % self.planet_name

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "terrain": self.terrain,
            "population": self.population,
            "climate": self.climate,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "url_imagen": self.url_imagen
        }