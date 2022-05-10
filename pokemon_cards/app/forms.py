from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectMultipleField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput
from app.models import Pokemons,Decks,Profiles,Users
from app import db
from flask_login import login_required,current_user


class SignUpForm(FlaskForm):
    username = TextAreaField('User Name',
                                validators=[InputRequired(),
                                            Length(max=200)])
    email = TextAreaField('Email',
                                validators=[InputRequired(),
                                            Length(max=200)])
    password1 = TextAreaField('Password', widget=PasswordInput(hide_value=False),
                                validators=[InputRequired(),
                                            Length(max=200)])
    password2 = TextAreaField('Password Again', widget=PasswordInput(hide_value=False),
                                validators=[InputRequired(),
                                            Length(max=200)])
    

class LogInForm(FlaskForm):
    username = TextAreaField('User Name',
                                validators=[InputRequired(),
                                            Length(max=200)])
    password = TextAreaField('Password', widget=PasswordInput(hide_value=False),
                                validators=[InputRequired(),
                                            Length(max=200)])

class CreateProfileForm(FlaskForm):
    pokemon = SelectMultipleField('pokemon', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        pokemons = Pokemons.query.all()
        names = []
        for pokemon in pokemons:
            names.append(pokemon.name)
        self.pokemon.choices = names
    
class CreatePost(FlaskForm):
    title = TextAreaField('Post Title',
                                validators=[InputRequired(),
                                            Length(max=200)])
    body = TextAreaField('Post Body', 
                                validators=[InputRequired(),
                                            Length(max=2000)])

class CreateTransactionForm(FlaskForm):
    pokemon = SelectMultipleField('pokemon', validators=[InputRequired()])
    currency = TextAreaField('Currency',
                                validators=[Length(max=200)])
    def __init__(self, *args, **kwargs):
        super(CreateTransactionForm, self).__init__(*args, **kwargs)
        try:
            pokemons = db.session.query(Pokemons).join(Decks, Pokemons.in_deck==Decks.id).join(Profiles, Decks.profile_id==Profiles.id).join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).all()
            names = []
            for pokemon in pokemons:
                names.append(pokemon.name)
            self.pokemon.choices = names
        except:
            print('log in first')

class CreateTadeForm(FlaskForm):
    pokemon = SelectMultipleField('pokemon', validators=[InputRequired()])
    currency = TextAreaField('Currency',
                                validators=[Length(max=200)])
    def __init__(self, *args, **kwargs):
        super(CreateTadeForm, self).__init__(*args, **kwargs)
        try:
            pokemons = db.session.query(Pokemons).join(Decks, Pokemons.in_deck==Decks.id).join(Profiles, Decks.profile_id==Profiles.id).join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).all()
            names = []
            for pokemon in pokemons:
                names.append(pokemon.name)
            self.pokemon.choices = names
        except:
            print('log in first')