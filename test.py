from awesome import Player

p = Player()
# p.newGame(['A', 'A', 'K', '9', '9', '8', '8', '4', '4', '4', '3', '3'], ['Q', 'Q', 'Q', 'J', '10', '9', '7', '7', '5', '5', '3', '3'], 'OP')
p.newGame(['A', '9'], ['10', '8', '8', '6'], 'op')
print(p.play([]))
