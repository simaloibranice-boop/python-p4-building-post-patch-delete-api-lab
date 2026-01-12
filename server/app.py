from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(
        bakeries,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery == None:
        response_body = {
            "error": "Bakery not found"
        }
        return make_response(response_body, 404)

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        # Updates the name of the bakery
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        
        db.session.add(bakery)
        db.session.commit()

        return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods, 200)

    elif request.method == 'POST':
        # Creates a new baked good
        new_bg = BakedGood(
            name=request.form.get("name"),
            price=int(request.form.get("price")),
            bakery_id=int(request.form.get("bakery_id"))
        )

        db.session.add(new_bg)
        db.session.commit()

        return make_response(new_bg.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_good_by_id(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if baked_good == None:
        response_body = {
            "error": "Baked good not found"
        }
        return make_response(response_body, 404)
    
    if request.method == 'GET':
        return make_response(baked_good.to_dict(), 200)

    elif request.method == 'DELETE':
        # Deletes the baked good
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "message": "Baked good deleted"
        }
        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)