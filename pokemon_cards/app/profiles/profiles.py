from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required,current_user
import random
from app.forms import CreateProfileForm
from app import db
from app.models import Pokemons,Profiles, Users, Decks

profiles_bp = Blueprint('profiles_bp',__name__,
    template_folder='templates',
    static_folder='static', 
    static_url_path='assets')

@profiles_bp.route('/create', methods=['GET', 'POST'])
def create():
    if current_user.is_authenticated:
        create_profile_formi = CreateProfileForm()
        if create_profile_formi.validate_on_submit():  
            pokemon_name = create_profile_formi.pokemon.data  
            profile = Profiles(currency=5)
            try:
                user = Users.query.filter_by(name=current_user.name).first()
            except:
                return redirect(url_for('users_bp.login'))
            user.user_profile.append(profile)
            pokemon = Pokemons.query.filter_by(name=pokemon_name[0]).first()
            pokemon.pokemon_profile.append(profile)
            deck = Decks()
            # adding 3 random pokemons to the deck
            for i in range(3):
                print(profile)
                num = random.randint(1,151)
                pokemon = Pokemons.query.filter_by(id=num).first()
                deck.pokemons.append(pokemon)
            profile.decks.append(deck)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('profiles_bp.display'))
        return render_template('create.html', form=create_profile_formi)
    return redirect(url_for('users_bp.login'))


@profiles_bp.route('/display', methods=['GET', 'POST'])
def display():
    try:
        profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
        currency = profile.currency
        pokemon = db.session.query(Pokemons).join(Profiles, Pokemons.id == Profiles.pokemon_id).join(Users, Profiles.user_id == Users.id).filter_by(name=current_user.name).first()
        cards = db.session.query(Pokemons).join(Decks, Pokemons.in_deck == Decks.id).join(Profiles, Decks.profile_id == Profiles.id).join(Users, Profiles.user_id == Users.id).filter_by(name=current_user.name).all()
        return render_template('display.html', main_pokemon=pokemon, cards=cards, currency=currency)
    except:
        return redirect(url_for('profiles_bp.create')) 