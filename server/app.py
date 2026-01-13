from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, Customer # Assuming your model is named Customer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Customers(Resource):
    def get(self):
        customers = [c.to_dict() for c in Customer.query.all()]
        return make_response(jsonify(customers), 200)

    def post(self):
        data = request.get_json()
        try:
            new_customer = Customer(
                name=data.get('name'),
                email=data.get('email'),
                age=int(data.get('age'))
            )
            db.session.add(new_customer)
            db.session.commit()
            return make_response(new_customer.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 422)

api.add_resource(Customers, '/customers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)