from dealer import Dealer
import sys, getopt
import copy

def choosePlayer(teamName):
   new_module = __import__(teamName) 
   return new_module.Player()


class PlayerInterface:
    def teamName(self) -> str:
        """队名"""
        pass

    def newGame(self, hand1, hand2, opponent):
        """
          hand1: 自己手里的牌，比如：['A', 'A', '2', '2']，字母大写
          hand2: 对方手里的牌
          opponent: 对手名称
        """
        pass

    def play(self, t):
        """
          t: 对手出的牌, []表示自己先手或者对方pass
          return: 自己出的牌，需要能压住t
        """
        pass

    def ack(self, t):
        """
          t: 裁判确认的有效出牌
        """
        pass

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ha:d:g:",["attacker=","defender=", "game="])
    except getopt.GetoptError:
        print('big2.py -a <attacker> -d <defender> -g <game>')
        sys.exit(2)
    Tom = Jack = game = None
    for opt, arg in opts:
        if opt == '-h':
            print('big2.py -a <attacker> -d <defender> -g <game>')
            sys.exit()
        elif opt in ("-a", "--attacker"):
            Tom = choosePlayer(arg)
        elif opt in ("-d", "--defender"):
            Jack = choosePlayer(arg)
        elif opt in ("-g", "--game"):
            game = int(arg)

    if not Tom or not Jack or not game:
        print('big2.py -a <attacker> -d <defender> -g <game>')
        sys.exit(3)

    Annie = Dealer("Version1")

    cards = Annie.deal(game)
    Tom.newGame(copy.copy(cards[0]), copy.copy(cards[1]), Jack.teamName())
    Jack.newGame(copy.copy(cards[1]), copy.copy(cards[0]), Tom.teamName())
    print("{:<80}".format(Tom.teamName()))
    print("{:<80}".format(str(cards[0])))
    print("{:>80}".format(Jack.teamName()))
    print("{:>80}".format(str(cards[1])))
    print("-"*80)

    #Tom.play(['A', 'J', '2', '3', '3', '5', '10'], [7, 7, 8], [8]))
    t, player, score = [], None, None
    while not score:
        # Tom 先手，然后轮流出牌
        player = Tom if not player or player is Jack else Jack 
        t = player.play(t)
        score, t = Annie.check(t)
        output = "{:<80}" if player is Tom else "{:>80}"
        print(output.format(str(t) if t else "pass"))
        player.ack(t) # player获知Annie的裁定
    else:
        print("{} is the winner! score={}".format(player.teamName(), score))

if __name__ == "__main__":
    main(sys.argv[1:])
