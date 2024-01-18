from main import game_info

#game = game_info("288841")
game = game_info("116954")
#game = game_info("313476")

print("Validating game: ",game.title())
print("Categories: ",game.category())
print("Mechanics: ",game.mechanic())
print("Expansion: ",game.expansion())
print("Year Published: ",game.year_published())
print("Min Players: ",game.minplayers())
print("Max Players: ",game.maxplayers())
print("Playtime: ",game.playtime())
print("Age: ",game.age())


def test_valid():
    assert game.is_valid() == True
        
def test_titles():
    assert len(game.title()) > 0
    assert type(game.title()) == str

def test_categories():
    assert len(game.category()) > 0
    assert type(game.category()) == str

def test_mechanics():
    assert len(game.mechanic()) > 0
    assert type(game.mechanic()) == str

def test_bgg_rating():
    assert len(str(game.bgg_rating())) > 0
    assert type(game.bgg_rating()) == int

def test_expansion():
    assert type(game.expansion()) == int
