from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required,current_user
from app.forms import CreatePost
from app import db
from app.models import Pokemons,Profiles, Users, Posts

forum_bp = Blueprint('forum_bp',__name__,
    template_folder='templates',
    static_folder='static', 
    static_url_path='assets')

@forum_bp.route('/posts', methods=['GET', 'POST'])
# @login_required
def posts():
    if current_user.is_authenticated:
        posts = Posts.query.all()
        posts_array = []
        for post in posts:
            post_title = post.title
            post_body = post.body
            try:
                author = db.session.query(Users).join(Profiles, Users.id == Profiles.user_id).join(Posts, Profiles.id==Posts.profile_id).filter_by(id=post.id).first()
                main_pokemon = Pokemons.query.join(Profiles, Pokemons.id==Profiles.pokemon_id).join(Users, Profiles.user_id==Users.id).filter_by(id=author.id).first()
                post_object = {'title': post_title, 'body': post_body, 'user': author.name ,'main_pokemon_img': main_pokemon.img}
                posts_array.append(post_object)
            except:
                print('no forum posts yet')
        create_post_formi = CreatePost()
        if create_post_formi.validate_on_submit():  
            title = create_post_formi.title.data
            body = create_post_formi.body.data  
            post = Posts(title,body)    
            profile = Profiles.query.join(Users, Profiles.user_id==Users.id).filter_by(name=current_user.name).first()
            profile.posts.append(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('forum_bp.posts'))
    else:
        return redirect(url_for('users_bp.login'))
    return render_template('posts.html', form=create_post_formi, posts=posts_array)