from contextlib import nullcontext
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required,current_user
from app.forms import CreateTransactionForm, CreateTadeForm
from app import db
from app.models import Pokemons,Profiles, Users, Transactions_a,Transactions_b, Decks, Trades

trading_bp = Blueprint('trading_bp',__name__,
    template_folder='templates',
    static_folder='static', 
    static_url_path='assets')


@trading_bp.route('/market', methods=['GET', 'POST'])
def market():
    if current_user.is_authenticated:
        transactions = Transactions_a.query.all()
        posts=[]
        for post in transactions:
            pokemon = Pokemons.query.filter_by(id=post.pokemons).first()
            posted_by = Users.query.join(Profiles, Users.id==Profiles.user_id).filter_by(id=post.profile).first()
            offer = Transactions_b.query.join(Trades, Transactions_b.id==Trades.transaction_b_id).join(Transactions_a, Trades.transaction_a_id==Transactions_a.id).filter_by(id=post.id).first()
            try:
                offer_pokemon = Pokemons.query.filter_by(id=offer.pokemons).first()
                offer_pokemon_name = offer_pokemon.name
                offer_currency = offer.currency
                offer_img = offer_pokemon.img
                offer_user = Users.query.join(Profiles, Users.id==Profiles.user_id).join(Transactions_b, Profiles.id==Transactions_b.profile).filter_by(id=offer.id).first()
                offer_user_name = offer_user.name
                offer_id = offer.id
                trade = Trades.query.join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=post.id).first()
                print(trade.approved)
                offer_approved =trade.approved
                
            except:
                offer_approved = None
                offer_pokemon_name = None
                offer_currency = None
                offer_img = None
                offer_user_name = None
                offer_id = None
                
            post_obj = {'id': post.id,'currency': post.currency,'pokemons': pokemon.name, 'profile': posted_by.name, 'img': pokemon.img, 'offer_pokemon': offer_pokemon_name, 'offer_currency': offer_currency, 'offer_img': offer_img, 'offer_user': offer_user_name, 'offer_id': offer_id, 'offer_approved': offer_approved} 
            posts.append(post_obj)
        create_transaction_formi = CreateTransactionForm()
        if create_transaction_formi.validate_on_submit():  
            transaction_a = Transactions_a()
            profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
            profile.transactions_a.append(transaction_a)
            pokemon_name = create_transaction_formi.pokemon.data
            pokemon = Pokemons.query.filter_by(name=pokemon_name[0]).first()
            pokemon.transactions_a.append(transaction_a)
            transaction_a.currency=create_transaction_formi.currency.data
            db.session.add(transaction_a)
            db.session.commit()
            return redirect(url_for('trading_bp.market'))
    else:
        return redirect(url_for('users_bp.login'))
    return render_template('market.html', form=create_transaction_formi, transactions=posts)

@trading_bp.route('/trade/<int:transaction_id>', methods=['GET', 'POST'])
def trade(transaction_id):
    transaction_a = Transactions_a.query.filter_by(id=transaction_id).first()
    pokemon_get = Pokemons.query.filter_by(id=transaction_a.pokemons).first()
    create_trade_formi = CreateTadeForm()
    if create_trade_formi.validate_on_submit():
        transaction_b = Transactions_b()
        profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
        profile.transactions_b.append(transaction_b)
        pokemon_name = create_trade_formi.pokemon.data
        pokemon = Pokemons.query.filter_by(name=pokemon_name[0]).first()
        pokemon.transactions_b.append(transaction_b)
        transaction_b.currency=create_trade_formi.currency.data
        trade = Trades()
        transaction_b.trades.append(trade)
        transaction_a.trades.append(trade)
        db.session.add(transaction_b)
        db.session.add(trade)
        db.session.commit()
        return redirect(url_for('trading_bp.market'))
    return render_template('trading.html', form=create_trade_formi, pokemon_get=pokemon_get)

@trading_bp.route('/buy/<transaction_id>', methods=['GET', 'POST'])
def buy(transaction_id):
    transaction_a = Transactions_a.query.filter_by(id=transaction_id).first()
    buyer_profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
    if buyer_profile.currency >= transaction_a.currency:
        pokemon_get = Pokemons.query.join(Transactions_a, Pokemons.id==Transactions_a.pokemons).filter_by(id=transaction_a.id).first()
        # seller
        seller_profile = Profiles.query.join(Transactions_a, Profiles.id==Transactions_a.profile).filter_by(id=transaction_a.id).first()
        seller_profile.currency += transaction_a.currency
        seller_deck = Decks.query.join(Profiles, Decks.profile_id==Profiles.id).filter_by(id=seller_profile.id).first()
        seller_deck.pokemons.remove(pokemon_get)
        # buyer
        buyer_profile.currency -= transaction_a.currency
        buyer_deck = Decks()
        buyer_deck.pokemons.append(pokemon_get)
        buyer_profile.decks.append(buyer_deck)
        db.session.query(Transactions_a).filter
        db.session.query(Transactions_a).filter_by(id=transaction_id).delete()
        db.session.add(buyer_deck)
        db.session.commit()
    else:
        return 'you dont have enough money'
    return redirect(url_for('trading_bp.market'))

@trading_bp.route('/cancel_offer/<transaction_id>', methods=['GET'])
def cancel_offer(transaction_id):
    transaction_a = Transactions_a.query.join(Trades, Transactions_a.id==Trades.transaction_a_id).join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    pokemon = Pokemons.query.join(Transactions_b, Pokemons.id==Transactions_b.pokemons).filter_by(id=transaction_id).first()
    # db.session.query(Trades).filter_by(transaction_b_id=transaction_id).delete()
    trade = Trades.query.join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    transaction_a.trades.remove(trade)
    # db.session.query(Transactions_b).filter_by(id=transaction_id).delete()
    db.session.commit()
    return redirect(url_for('trading_bp.market'))

@trading_bp.route('/accept_offer/<transaction_id>', methods=['GET'])
def accept_offer(transaction_id):
    transaction_b = Transactions_b.query.filter_by(id=transaction_id).first()
    transaction_a = Transactions_a.query.join(Trades, Transactions_a.id==Trades.transaction_a_id).join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    pokemon_b = Pokemons.query.join(Transactions_b, Pokemons.id==Transactions_b.pokemons).filter_by(id=transaction_id).first()
    pokemon_a = Pokemons.query.join(Transactions_a, Pokemons.id==Transactions_a.pokemons).filter_by(id=transaction_a.id).first()
    profile_b = Profiles.query.join(Transactions_b, Profiles.id==Transactions_b.profile).filter_by(id=transaction_id).first()
    profile_a = Profiles.query.join(Transactions_a, Profiles.id==Transactions_a.profile).filter_by(id=transaction_a.id).first()
    profile_b.currency -= transaction_b.currency
    profile_a.currency += transaction_b.currency
    deck_a_get = Decks()
    deck_b_get = Decks()
    deck_a_get.pokemons.append(pokemon_b)
    profile_a.decks.append(deck_a_get)
    db.session.add(deck_a_get)
    deck_b_get.pokemons.append(pokemon_a)
    profile_b.decks.append(deck_b_get)
    db.session.add(deck_b_get)
    deck_b_give = Decks.query.join(Profiles, Decks.profile_id==Profiles.id).filter_by(id=profile_b.id).first()
    deck_b_give.pokemons.remove(pokemon_b)
    deck_a_give = Decks.query.join(Profiles, Decks.profile_id==Profiles.id).filter_by(id=profile_a.id).first()
    deck_a_give.pokemons.remove(pokemon_a)
    # approve trade
    trade = Trades.query.join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    trade.approved=True    
    db.session.commit()
    return redirect(url_for('trading_bp.market'))

@trading_bp.route('/reject_offer/<transaction_id>', methods=['GET', 'POST'])
def reject_offer(transaction_id):
    transaction_a = Transactions_a.query.join(Trades, Transactions_a.id==Trades.transaction_a_id).join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    pokemon = Pokemons.query.join(Transactions_b, Pokemons.id==Transactions_b.pokemons).filter_by(id=transaction_id).first()
    # db.session.query(Trades).filter_by(transaction_b_id=transaction_id).delete()
    trade = Trades.query.join(Transactions_b, Trades.transaction_b_id==Transactions_b.id).filter_by(id=transaction_id).first()
    transaction_a.trades.remove(trade)
    # db.session.query(Transactions_b).filter_by(id=transaction_id).delete()
    db.session.commit()
    return redirect(url_for('trading_bp.market'))