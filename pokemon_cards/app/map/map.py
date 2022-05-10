from flask import Blueprint, render_template, redirect, url_for
import random
from app import db
from app.models import Pokemons,Profiles, Users, Decks
from flask_login import login_required,current_user

map_bp = Blueprint('map_bp',__name__,
    template_folder='templates',
    static_folder='static', 
    static_url_path='assets')

@login_required
@map_bp.route('/get_random', methods=['GET'])
def get_random():
    if current_user.is_authenticated:
        profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
        deck = Decks()
        num = random.randint(1,151)
        pokemon = Pokemons.query.filter_by(id=num).first()
        deck.pokemons.append(pokemon)
        profile.decks.append(deck)
        db.session.commit()
        return redirect(url_for('profiles_bp.display'))
    else:
        return redirect(url_for('users_bp.login'))