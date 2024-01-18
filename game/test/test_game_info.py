from main import game_info

#game = game_info("288841")
game = game_info("116954")
#game = game_info("313476")

print("\nValidating game: ",game.title())
print("\nCategories: ",game.category())
print("\nMechanics: ",game.mechanic())
print("\nExpansion: ",game.expansion())
print("\nYear Published: ",game.year_published())
print("\nMin Players: ",game.minplayers())
print("\nMax Players: ",game.maxplayers())
print("\nPlaytime: ",game.playtime())
print("\nAge: ",game.age())


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
