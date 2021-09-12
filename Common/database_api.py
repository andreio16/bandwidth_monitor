from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal_with, reqparse, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../net_app.db'

api = Api(app)
db = SQLAlchemy(app)


class ResourceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.String(50), nullable=False)
    mega_bits_per_second = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Resource(Mb/s = {self.mega_bits_per_second}, timestamp = {self.date_created})"


# db.create_all()


# RES_FIELD FOR SERIALIZING THE RETURN RESULT
resource_fields = {
    'id': fields.Integer,
    'date_created': fields.String,
    'mega_bits_per_second': fields.Float
}


resource_put_args = reqparse.RequestParser()
resource_put_args.add_argument("date_created", type=str, help="Resource timestamp is required!", required=True)
resource_put_args.add_argument("mega_bits_per_second", type=float, help="Resource Mb/s is required!", required=True)

resource_update_args = reqparse.RequestParser()
resource_update_args.add_argument("date_created", type=str, help="Resource timestamp is required!")
resource_update_args.add_argument("mega_bits_per_second", type=float, help="Resource Mb/s is required!")


# API CLASS RESOURCE
class ResourceAPI(Resource):

    @marshal_with(resource_fields)
    def get(self, res_id):
        result = ResourceModel.query.filter_by(id=res_id).first()
        if not result:
            abort(404, message="Could not find tuple with id {}".format(res_id))
        return result

    @marshal_with(resource_fields)
    def put(self, res_id):
        args = resource_put_args.parse_args()
        result = ResourceModel.query.filter_by(id=res_id).first()

        if result:
            abort(409, message="Db tuple id taken...")

        new_tuple = ResourceModel(id=res_id, date_created=args['date_created'], mega_bits_per_second=args['mega_bits_per_second'])
        db.session.add(new_tuple)
        db.session.commit()
        return new_tuple, 201

    @marshal_with(resource_fields)
    def patch(self, res_id):
        args = resource_update_args.parse_args()
        result = ResourceModel.query.filter_by(id=res_id).first()

        if not result:
            abort(404, message="Db tuple doesn't exist, cannot update")
        if args['date_created']:
            result.date_created = args["date_created"]
        if args['mega_bits_per_second']:
            result.mega_bits_per_second = args["mega_bits_per_second"]

        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def delete(self, res_id):
        result = ResourceModel.query.filter_by(id=res_id).first()

        if not result:
            abort(404, message="Db tuple doesn't exist, cannot delete")

        db.session.delete(result)
        db.session.commit()
        return result


# REGISTER API
api.add_resource(ResourceAPI, "/resource/<int:res_id>")

if __name__ == "__main__":
    app.run(debug=True)
