from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
#from flask_restful import Resource,Api
from models import db, Power, Hero, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return make_response(
        jsonify({"msg":"hero powers"}), 200)


@app.route("/heroes")
def Heroes():
    heroes = [{
            "id":hero.id,
            "name":hero.name,
            "super_name":hero.super_name,
        } for hero in Hero.query.all()]
    return make_response(jsonify({"Heroes": heroes}), 200)

            
@app.route("/powers")
def power():
    powers = [{
            "id":power.id,
            "name":power.name,
            "description":power.description,           
        } for power in Power.query.all()]
    return make_response(jsonify({"Powers": powers}), 200)

@app.route("/heroes/<int:id>",methods=["GET", "DELETE"])
def hero_view(id):
    if request.method =="GET":
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            powers = [{"id": power.id, "name": power.name, "description": power.description} for power in hero.powers]
            response = {
                "id":hero.id,
                "name":hero.name,
                "address":hero.address,
                "powers": powers
            }
            return make_response(jsonify(response), 200 )
        else: 
            return make_response(jsonify({"error": "hero not found"}), 404 )
   
    elif request.method =="DELETE":
        hero = Hero.query.filter_by(id=id).first() 
        if hero:
            HeroPower.query.filter_by(hero_id=id).delete()
            db.session.delete(hero)
            db.session.commit()
            return make_response("", 204 )
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404 )




@app.route("/hero_powers", methods=["GET", "POST"])
def hero_powers_view():
    if request.method =="GET":
        hero_powers = [{
            "id":heropower.id,
            "strength":heropower.strength,
            "hero_id":heropower.hero_id,
            "power_id":heropower.power_id,
            "created_at":str(heropower.created_at),
            "updated_at":str(heropower.updated_at),
        } for heropower in HeroPower.query.all()]
        return make_response(jsonify({"Rero_powers": hero_powers}), 200)
    elif request.method =="POST":
        try:
            data = request.get_json()
            hp = HeroPower(
                strength=data["strength"],
                hero_id=data["hero_id"],
                power_id=data["power_id"]
            )
            db.session.add(hp)
            db.session.commit()
            power = Power.query.filter_by(id=data["power_id"]).first()
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            response = make_response(jsonify(power_dict), 201)

            return response
        except ValueError as e:
            response = make_response(jsonify({"errors": e.args}), 400)
            return response
        except Exception as e:
            response = make_response(jsonify({"errors": e.args}), 400)
            return response

   
if __name__ == '__main__':
    app.run(port=5555,debug=True)