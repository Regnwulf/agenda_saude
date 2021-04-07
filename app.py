from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/agenda_saude'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Scheduling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(255))
    profissional = db.Column(db.String(255))
    data = db.Column(db.Integer)
    horario = db.Column(db.Integer)

    def __init__(self, especialidade, profissional, data, horario):
        self.especialidade = especialidade
        self.profissional = profissional
        self.data = data
        self.horario = horario

# Product Schema
class SchedulingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'especialidade', 'profissional', 'data', 'horario')

# Init Schema
scheduling_schema = SchedulingSchema()
schedulings_schema = SchedulingSchema(many=True)

# pesquisar agendamentos
@app.route('/agendamentos', methods=['GET'])
def get_schedulings():
    all_schedulings = Scheduling.query.all()
    result = schedulings_schema.dump(all_schedulings)
    return jsonify(result)

# criar um agendamento
@app.route('/agendamento', methods=['POST'])
def add_scheduling():
    especialidade = request.json['especialidade']
    profissional = request.json['profissional']
    data = request.json['data']
    horario = request.json['horario']
    new_scheduling = Scheduling(especialidade, profissional, data, horario)
    db.session.add(new_scheduling)
    db.session.commit()
    return scheduling_schema.jsonify(new_scheduling)

# pesquisar agendamento por id
@app.route('/agendamento/<id>', methods=['GET'])
def get_scheduling(id):
    scheduling_get = Scheduling.query.get(id)
    return scheduling_schema.jsonify(scheduling_get)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)