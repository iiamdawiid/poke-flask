from app import app
from flask import render_template, request
from .forms import PokemonForm
import requests as r


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


@app.route("/pokemoninfo", methods=["GET", "POST"])
def get_poke_info():
    form = PokemonForm()
    poke_dict = {}

    if request.method == 'POST':
        if form.validate():
            poke_name = form.poke_name.data
            poke_dict = get_pokemon(poke_name)

    return render_template('pokeinfo.html', form=form, pokemon_info=poke_dict)