from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from .forms import PokemonForm, SignUpForm, LogInForm
import requests as r
from .models import User
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def index():
    return render_template('index.html')


def get_pokemon(poke_name):
        poke_name = poke_name.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
        response = r.get(url)
        if response.ok:
            data = response.json()
            # pokemon name
            # base stat for hp
            # base stat for defense
            # base stat for attack
            # front_shiny (URL to the image) or any other image you like more
            # At Least One Ability
            return {
                 'name': data['name'],
                 'base hp stat': data['stats'][0]['base_stat'],
                 'base defense': data['stats'][2]['base_stat'],
                 'base attack': data['stats'][1]['base_stat'],
                 'image': data['sprites']['front_shiny'],
                 'ability': data['abilities'][0]['ability']['name']
            }


@app.route("/pokemoninfo", methods=["GET", "POST"], endpoint='pokemoninfo')
def get_poke_info():
    form = PokemonForm()
    poke_dict = {}

    if request.method == 'POST':
        if form.validate():
            poke_name = form.poke_name.data
            poke_dict = get_pokemon(poke_name)

    return render_template('pokeinfo.html', form=form, pokemon_info=poke_dict)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        print("POST REQUEST MADE")
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data 
            password = form.password.data

            # check if email already exists
            user_exists = User.query.filter_by(email=email).first()

            if user_exists:
                flash("A user with this email already exists. Please use a different email.")
                return redirect(url_for('signup'))
            
            # if email is clear
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully!')
            return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            # check if user exists
            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                # session['user_id'] = user.id
                login_user(user)
                flash("LOGIN SUCCESSFUL")
                return redirect(url_for('index'))
            else:
                flash("INVALID EMAIL OR PASSWORD. TRY AGAIN")
    
    return render_template('login.html', form=form)