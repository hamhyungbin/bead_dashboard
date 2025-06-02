from flask import Blueprint, request, jsonify
from .models import Widget, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests # For OpenWeatherMap API
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@api_bp.route('/widgets', methods=['GET'])
@jwt_required()
def get_widgets():
    user_id = get_jwt_identity()
    widgets = Widget.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": w.id,
        "type": w.widget_type,
        "config": w.config,
        "layout": w.layout
    } for w in widgets]), 200

@api_bp.route('/widgets', methods=['POST'])
@jwt_required()
def add_widget():
    user_id = get_jwt_identity()
    data = request.get_json()
    # Ensure layout has i, x, y, w, h
    if not all(k in data.get('layout', {}) for k in ['i', 'x', 'y', 'w', 'h']):
        return jsonify({"msg": "Layout requires i, x, y, w, h"}), 400

    new_widget = Widget(
        id=data['layout']['i'], # Use client-generated ID from layout.i
        user_id=user_id,
        widget_type=data['type'],
        config=data.get('config', {}),
        layout=data['layout']
    )
    db.session.add(new_widget)
    db.session.commit()
    return jsonify({
        "id": new_widget.id,
        "type": new_widget.widget_type,
        "config": new_widget.config,
        "layout": new_widget.layout
    }), 201

@api_bp.route('/widgets/<string:widget_id>', methods=['PUT'])
@jwt_required()
def update_widget(widget_id):
    user_id = get_jwt_identity()
    widget = Widget.query.filter_by(id=widget_id, user_id=user_id).first_or_404()
    data = request.get_json()

    if 'config' in data:
        widget.config = data['config']
    if 'layout' in data:
        widget.layout = data['layout'] # Make sure layout includes i,x,y,w,h

    db.session.commit()
    return jsonify({
        "id": widget.id,
        "type": widget.widget_type,
        "config": widget.config,
        "layout": widget.layout
    }), 200

@api_bp.route('/widgets/<string:widget_id>', methods=['DELETE'])
@jwt_required()
def delete_widget(widget_id):
    user_id = get_jwt_identity()
    widget = Widget.query.filter_by(id=widget_id, user_id=user_id).first_or_404()
    db.session.delete(widget)
    db.session.commit()
    return jsonify({"msg": "Widget deleted"}), 200


@api_bp.route('/weather', methods=['GET'])
@jwt_required() # Or remove if you want it to be a public proxy
def get_weather_data():
    city = request.args.get('city')
    if not city:
        return jsonify({"msg": "City parameter is required"}), 400
    if not OPENWEATHER_API_KEY:
        return jsonify({"msg": "Weather service not configured"}), 500

    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric' # or 'imperial'
    }
    try:
        response = requests.get(OPENWEATHER_API_URL, params=params)
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"msg": f"Error fetching weather data: {e}", "details": response.text if 'response' in locals() else "No response"}), 500