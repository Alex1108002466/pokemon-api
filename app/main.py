from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
app = FastAPI()
 
class PokemonInfo(BaseModel):
    name: str
    base_experience: int
    height: float
    type: list[str]
    weight: float

POKEMONS = {
    "pikachu": PokemonInfo(
        name = "pikachu",
        base_experience = 112,
        height = 0.4,
        type = ["electric"],
        weight = 6.0,
    ),
    "charizard": PokemonInfo(
        name = "charizard",
        base_experience = 267,
        height = 1.7,
        type = ["fire", "flying"],
        weight = 90.5,
    ),
    "mewtwo": PokemonInfo(
        name = "mewtwo",
        base_experience = 340,
        height = 2.0,
        type = ["psychic"],
        weight = 122.0,
    )
}
 
@app.get("/")
def root():
    return {"message": "Pokemon API работает!"}

@app.get("/pokemon")
def pokemons():
    return list(POKEMONS.keys())

@app.get("/pokemon/{name}", response_model = PokemonInfo)
def get_pokemon(name: str):
    pokemon = POKEMONS.get(name)
    if not pokemon:
        raise HTTPException(status_code = 404, detail = f"Покемон {name} не найден!")
    return pokemon