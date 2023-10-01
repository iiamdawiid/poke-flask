from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from .forms import PokemonForm, SignUpForm, LogInForm, EditProfileForm, CatchPokemonForm
import requests as r
from .models import User, CatchPokemon
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def index():
    return render_template('index.html')

# for /pokemoninfo
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
@login_required
def get_poke_info():
    form = PokemonForm()
    poke_dict = {}

    if request.method == 'POST':
        if form.validate():
            poke_name = form.poke_name.data
            poke_dict = get_pokemon(poke_name)

            if not poke_dict:
                flash('Pokemon not found. Please try again.', 'danger')
                return redirect(url_for('pokemoninfo'))
        else:
            flash('INVALID FORM', 'danger')
            return redirect(url_for('pokemoninfo'))

    return render_template('pokeinfo.html', form=form, pokemon_info=poke_dict)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        print("POST REQUEST MADE")
        if form.validate():
            first_name = form.first_name.data.title()
            last_name = form.last_name.data.title()
            email = form.email.data 
            password = form.password.data

            # check if email already exists
            user_exists = User.query.filter_by(email=email).first()

            if user_exists:
                print("USER EXISTS")
                flash("A user with this email already exists. Please use a different email.", 'danger')
                return redirect(url_for('signup'))
            
            else:
                new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()

                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
        
        else:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))
    
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
                flash("Login Successful", 'success')
                return redirect(url_for('index'))
            
            else:
                flash('Invalid email or password. Please try again.', 'danger')
                return redirect(url_for('login'))

        else:
            flash('Invalid Form. Please try again.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route("/editprofile", methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if request.method == 'POST':
        if 'delete_account' in request.form:
            deleted_user = User.query.get(current_user.id)
            CatchPokemon.query.filter_by(user_id=current_user.id).delete()
            db.session.delete(deleted_user)
            db.session.commit()

            logout_user()
            flash('Account successfully deleted.', 'danger')
            return redirect(url_for('login'))

        elif form.validate():
            new_email = form.email.data
            new_password = form.password.data
           
            if new_email:
                user_exists = User.query.filter_by(email=new_email).first()
                if new_email != current_user.email and not user_exists:
                    current_user.email = new_email
                    flash(f'Success! Email changed to: {new_email}', 'success')
                elif form.email.data != form.confirm_email.data:
                    flash("Email's do not match. Please try again.", 'danger')
                else:
                    flash('Please choose a new email.', 'danger')

            if new_password:
                if form.password.data != form.confirm_password.data:
                    flash("Password's do not match. Please try again.", 'danger')
                
                elif new_password != current_user.password:
                    current_user.password = new_password
                    flash('Success! New password created.', 'success')
                else:
                    flash('Please choose a different password.', 'danger')

            db.session.commit()
            return redirect(url_for('editprofile'))

        else:
            flash("Password's or Email's do not match. Please try again", 'danger')
            return redirect(url_for('editprofile'))
 
    return render_template('editprofile.html', form=form)

# for /catchpokemons       
def get_random_pokemon():
        import random
        random_pokemon = random.randint(1, 1292)
        url = f"https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
        response = r.get(url)
        if response.ok:
            data = response.json()
            poke_url = data['results'][random_pokemon]['url']
            print(poke_url)
            info_url = poke_url
            new_response = r.get(info_url)
            if new_response.ok:
                rand_poke_info = new_response.json()
    
                return {
                    'name': data['results'][random_pokemon]['name'],
                    'base hp stat': rand_poke_info['stats'][0]['base_stat'],
                    'base defense': rand_poke_info['stats'][2]['base_stat'],
                    'base attack': rand_poke_info['stats'][1]['base_stat'],
                    'image': rand_poke_info['sprites']['front_shiny'],
                    'ability': rand_poke_info['abilities'][0]['ability']['name']
                }
            
# for /catchpokemons          
def determine_if_caught():
    import random
    # determine whether or not the pokemon was caught
    determiner = random.randint(1,2)
    return determiner

@app.route('/catchpokemons', methods=['GET', 'POST'])
@login_required
def catch_pokemons():
    form = CatchPokemonForm()
    rand_pokemon_dict = {}
    user_id = current_user.id
    pokemon_name = session.get('pokemon_name')

    num_pokemon_caught = CatchPokemon.query.filter_by(user_id=user_id).count()

    if num_pokemon_caught >= 10:
        flash('You can not catch more than 10 Pokemon!', 'warning')
        return redirect(url_for('pokemoninfo'))

    if request.method == 'POST':
        if 'find_pokemon' in request.form:
            rand_pokemon_dict = get_random_pokemon()
            pokemon_name = rand_pokemon_dict.get('name')
            session['pokemon_name'] = pokemon_name

        elif 'catch_pokemon' in request.form:
            if not pokemon_name:
                flash('You need to find a pokemon first!', 'danger')
                return redirect(url_for('catch_pokemons'))
            
            caught_or_not = determine_if_caught()

            if caught_or_not == 1:
                # pokemon is caught
                already_caught = CatchPokemon.query.filter_by(user_id=user_id, pokemon_name=pokemon_name).first()

                if already_caught:
                    flash('You already have this pokemon.', 'danger')
                    return redirect(url_for('catchpokemons'))
                
                else:
                    new_pokemon = CatchPokemon(pokemon_name=pokemon_name, user_id=user_id)
                    db.session.add(new_pokemon)
                    db.session.commit()
                    flash(f'You caught {pokemon_name.title()}!', 'success')
                    session.pop('pokemon_name', None)
                return redirect('catchpokemons')

            else:
                flash(f'Dang! {pokemon_name.title()} escaped!', 'danger')
                session.pop('pokemon_name', None)
                return redirect(url_for('catch_pokemons'))

    return render_template('catchpokemons.html', form=form, rand_pokemon_info=rand_pokemon_dict)