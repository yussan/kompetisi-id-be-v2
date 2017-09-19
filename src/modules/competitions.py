from flask import Blueprint, redirect, request , jsonify

bp = Blueprint('competitions', __name__)

@bp.route('/competitions')
def competition_list():
    "list competition"
    return jsonify({'data':{}})