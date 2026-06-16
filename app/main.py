from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, Field, create_engine, select


class PokemonBase(SQLModel):
    name: str = Field(index=True)
    base_experience: int
    height: float
    type: str
    weight: float

class Pokemon(PokemonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class PokemonPublic(PokemonBase):
    id: int

class PokemonCreate(PokemonBase):
    pass

class PokemonUpdate(SQLModel):
    name: str | None = None
    base_experience: int | None = None
    height: float | None = None
    type: str | None = None
    weight: float | None = None

sqlite_url = f"sqlite:///pokemon.db"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

def seed_pokemons():
    """
    Заполняет БД покемонами, если таблица пустая
    """
    with Session(engine) as session:
        existing = session.exec(select(Pokemon)).first()
        if existing:
            return  # данные уже есть, не дублируем
 
        pokemons = [
            Pokemon(name="pikachu", base_experience=112, height=0.4, type="electric", weight=6.0),
            Pokemon(name="charizard", base_experience=267, height=1.7, type="fire,flying", weight=90.5),
            Pokemon(name="mewtwo", base_experience=340, height=2.0, type="psychic", weight=122.0),
        ]
        session.add_all(pokemons)
        session.commit()

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_pokemons()


@app.get("/", summary="Проверка работы сервера")
def root():
    """
    Возвращает приветственное сообщение, чтобы убедиться что API запущен
    """
    return {"message": "Pokemon API работает!"}

# LIST
@app.get("/pokemon", response_model=list[PokemonPublic], summary="Список всех покемонов")
def get_pokemons(session: Session = Depends(get_session)):
    """
    Возвращает список названий всех покемонов
    """
    pokemons = session.exec(select(Pokemon)).all()
    return pokemons

# INFO
@app.get("/pokemon/{pokemon_id}", response_model = PokemonPublic, summary="Информация о покемоне")
def get_pokemon(pokemon_id: int, session: Session = Depends(get_session)):
    """
    Возвращает характеристики покемона по его id
    """
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code = 404, detail="Покемон не найден!")
    return pokemon

# CREATE
@app.post("/pokemon/", response_model=PokemonPublic, summary="Создать покемона")
def create_pokemon(pokemon: PokemonCreate, session: Session = Depends(get_session)):
    """
    Добавляет нового покемона в бд
    """
    db_pokemon = Pokemon.model_validate(pokemon)
    session.add(db_pokemon)
    session.commit()
    session.refresh(db_pokemon)
    return db_pokemon

# UPDATE
@app.patch("/pokemon/{pokemon_id}", response_model=PokemonPublic, summary="Обновить покемона")
def update_pokemon(pokemon_id: int, pokemon: PokemonUpdate, session: Session = Depends(get_session)):
    """
    Обновляет поля покемона
    """
    pokemon_db = session.get(Pokemon, pokemon_id)
    if not pokemon_db:
        raise HTTPException(status_code=404, detail="Покемон не найден")
    pokemon_data = pokemon.model_dump(exclude_unset=True)
    pokemon_db.sqlmodel_update(pokemon_data)
    session.add(pokemon_db)
    session.commit()
    session.refresh(pokemon_db)
    return pokemon_db

# DELETE
@app.delete("/pokemon/{pokemon_id}", summary="Удалить покемона")
def delete_pokemon(pokemon_id: int, session: Session = Depends(get_session)):
    """
    Удаляет покемона из бд по id
    """
    pokemon = session.get(Pokemon, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Покемон не найден")
    session.delete(pokemon)
    session.commit()
    return {"ok": True}
