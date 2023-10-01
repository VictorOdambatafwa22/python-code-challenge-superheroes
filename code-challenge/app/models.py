from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer(), primary_key=True)
    strength= db.Column(db.String)
    hero_id = db.Column(db.Integer(), db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer(), db.ForeignKey('powers.id'))
    created_at= db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

    @validates("strength")
    def validate_strength(self, key, strength):
        strengths = ["Strong", "Weak", "Average"]
        if strength not in strengths:
            raise ValueError("Invalid strength")
        return strength
 

    def __repr__(self):

        return f'hero_powers(id={self.id}'
         

class Hero(db.Model):
    __tablename__ = 'heros'


    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String,unique=True)
    super_name= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship(
        "Power", secondary="hero_powers", back_populates="heros"
    )

    def __repr__(self):
        return f'Hero {self.name}'
    


class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    description= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("description")
    def validate_description(self, key, description):
        if description =="":
            raise ValueError("description can not be blank")
        return description

    heros = db.relationship(
        "Hero", secondary="hero_powers", back_populates="powers"
    )

    def __repr__(self):
        return f'Power {self.name}'