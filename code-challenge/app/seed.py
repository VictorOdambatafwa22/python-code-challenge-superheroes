from random import randint, choice as rc
from faker import Faker
from models import db, Power, Hero, HeroPower
from app import app

fake = Faker()

with app.app_context():

    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    heros = []
    for n in range(25):
        h = Hero(name=fake.name(), super_name=fake.name())  
        heros.append(h)

    db.session.add_all(heros)

    powers = []
    for i in range(25):
        p = Power(name=fake.company(), description=fake.address())
        powers.append(p)

    db.session.add_all(powers)    

    hero_powers = []
    strengths = ["Strong", "Weak", "Average"]
    for i in range(30):
        hp = HeroPower(strength=rc(strengths), hero_id=randint(1, 10), power_id=randint(1, 10))
        hero_powers.append(hp)

    db.session.add_all(hero_powers)   

    db.session.commit()