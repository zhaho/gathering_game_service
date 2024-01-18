from lookup import price_lookup
game = "Las Navas de Tolosa, 1212"
print("Price Lookup Game: "+game)
print("Price Lookup: "+str(price_lookup.game_title(game)))


def test_price_lookup_game_title():
        assert type(price_lookup.game_title(game)) == int
