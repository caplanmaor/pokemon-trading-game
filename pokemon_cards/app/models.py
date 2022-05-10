from app import db
from app import login_manager
import flask_login
import json
from requests import Session

class Users(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    user_profile = db.relationship("Profiles", backref=db.backref("user_profile", uselist=False))

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

class Pokemons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img = db.Column(db.String(256))
    in_deck = db.Column(db.Integer, db.ForeignKey('decks.id'))
    pokemon_profile = db.relationship("Profiles", backref=db.backref("profile_pokemons", uselist=False))
    transactions_a = db.relationship("Transactions_a", backref='pokemon_transactions_a', lazy='dynamic')
    transactions_b = db.relationship("Transactions_b", backref='pokemon_transactions_b', lazy='dynamic')

    def __init__(self,name,img):
        self.name = name
        self.img = img

    def populate_db():
        try:
            session = Session()
            url='https://pokeapi.co/api/v2/pokemon?limit=151'
            response = session.get(url)
            data = json.loads(response.text)
            pokemons = data['results']
            # check if pokemon already exists
            for pokemon in pokemons:
                temp_pokemon = Pokemons.query.filter_by(name=pokemon['name']).first()
                if not temp_pokemon:
                    name = pokemon['name']
                    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
                    response = session.get(url)
                    data = json.loads(response.text)
                    img = data['sprites']['other']['official-artwork']['front_default']
                    pokemon_i = Pokemons(name,img)
                    db.session.add(pokemon_i)
            db.session.commit()  
        except:
            print("could not populate")   

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Integer)
    posts = db.relationship('Posts', backref='profile_posts', lazy='dynamic')
    transactions_a = db.relationship('Transactions_a', backref='profile_transactions_a', lazy='dynamic')
    transactions_b = db.relationship('Transactions_b', backref='profile_transactions_b', lazy='dynamic')
    decks = db.relationship('Decks', backref='profile_decks', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemons.id'))

    def __init__(self,currency,posts = tuple(),transactions_a = tuple(),transactions_b = tuple(),decks = tuple()):
        self.currency = currency
        self.posts = posts
        self.transactions_a = transactions_a
        self.transactions_b = transactions_b
        self.decks = decks


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(64))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __init__(self,title,body):
        self.title = title
        self.body = body

class Decks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemons = db.relationship('Pokemons', backref='deck_pokemons', lazy='dynamic')
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __init__(self,pokemons = tuple()):
        self.pokemons = pokemons

            
class Transactions_a(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    pokemons = db.Column(db.Integer, db.ForeignKey('pokemons.id'))
    currency = db.Column(db.Integer, default=0)
    trades = db.relationship('Trades', backref='trades_transactions_a', lazy='dynamic')

class Transactions_b(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    pokemons = db.Column(db.Integer, db.ForeignKey('pokemons.id'))
    currency = db.Column(db.Integer, default=0)
    trades = db.relationship('Trades', backref='trades_transactions_b', lazy='dynamic')

class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_a_id = db.Column(db.Integer, db.ForeignKey('transactions_a.id'))
    transaction_b_id = db.Column(db.Integer, db.ForeignKey('transactions_b.id'))
    approved = db.Column(db.Boolean, unique=False, default=False)