from flask import Flask, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import sys
import flask

app = Flask(__name__)
api_key = '145ffb0b8bafafdae1cfc3d97a7d4132'
api_form = f'api.openweathermap.org/data/2.5/weather?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

db = SQLAlchemy(app)




class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name

if 'weather.db' not in os.listdir():
    db.create_all()
# print(City.query.all())
def create_post(city_name):
    """Create data about weather on city name"""
    get_weather = r'http://' + api_form + f'q={city_name}&appid={api_key}&units=metric'
    # print(str(city_name))
    re = requests.get(get_weather)
    weather_data = re.json()
    dict_with_weather_info = [
        str(city_name).upper(),
        int(weather_data['main']['temp']) if 'main' in weather_data.keys() else '',
        weather_data['weather'][0]['main'] if 'weather' in weather_data.keys() else ''
    ]
    return dict_with_weather_info


def handle_query():
    """Simple handle query from user"""
    return request.form.get('city_name')

@app.route('/delete' , methods=['POST'])
def delete_card():
    deleted_card_id = int(request.form.get('id'))
    query = City.query.all()
    # print(query)
    db.session.query(City).filter(City.name == f'{query[deleted_card_id]}').delete()
    db.session.commit()
    return redirect('/')

@app.route('/', methods=['POST'])
def add_city():
    print(request.method)
    if request.method == 'POST':
        # dict_with_weather_info = create_post()
        city_name = handle_query()
        list_cities = City.query.all()
        city = [str(i) for i in list_cities]
        if create_post(city_name)[1] != '' and city_name not in city and city_name != None:
            post_to_db = City(name=city_name)
            db.session.add(post_to_db)
            db.session.commit()
        elif create_post(city_name)[1] == '' or create_post(city_name)[2] == '':
            flash("The city doesn't exist!")
        elif city_name in city:
            flash('The city has already been added to the list!')
        return redirect('/')


@app.route('/')
def index():
    """Create start page with default cities and almost created in database"""
    if request.method == 'GET':

        list_cities = City.query.all()

        if list_cities != []:
            dict_with_weather_info = [create_post(city) for city in list_cities]
            for i, tup in enumerate(dict_with_weather_info):
                dict_with_weather_info[i].append(i)
            # print(dict_with_weather_info)
        else:
            dict_with_weather_info = ''
        return flask.render_template('index.html', weather=dict_with_weather_info)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
