class playerClass:
    def __init__(self):
        self.score = 0

class boardClass:
    def __init__(self, beadsPerPit=4):
        self.player1 = playerClass()
        self.player2 = playerClass()
        self.pits = [
            beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit, # Top pits 0-5
            beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit, beadsPerPit  # Bottom pits 6-11
        ]
        self.turn = 0
        self.winner = None

    def addScore(self, beadCount):
        if self.turn == 0:
            self.player1.score += beadCount
        else:
            self.player2.score += beadCount

    def move(self, pit):
        pit += self.turn * 6
        beads = self.pits[pit]
        self.pits[pit] = 0
        stoppedInPit = False

        if pit == 5 and self.turn == 0 and beads > 0:
            self.player1.score += 1
            beads -= 1
            stoppedInPit = True
        elif pit == 11 and self.turn == 1 and beads > 0:
            self.player2.score += 1
            beads -= 1
            stoppedInPit = True

        while beads > 0:
            pit = (pit+1) % len(self.pits)
            stoppedInPit = False

            self.pits[pit] += 1
            beads -= 1

            if sum(self.pits[0:5]) == 0 or sum(self.pits[6:11]) == 0:
                self.player1.score += sum(self.pits[0:5])
                self.player2.score += sum(self.pits[6:11])
                if self.player1.score > self.player2.score:   self.winner = 0
                elif self.player2.score > self.player1.score: self.winner = 1
                else:                                         self.winner = -1

            if pit == 5 and self.turn == 0 and beads > 0:
                self.player1.score += 1
                beads -= 1
                stoppedInPit = True
                continue
            elif pit == 11 and self.turn == 1 and beads > 0:
                self.player2.score += 1
                beads -= 1
                stoppedInPit = True
                continue
            elif beads == 0 and self.pits[pit] == 1 and pit in range(6*self.turn, 6*self.turn+6):
                otherPit = 5 - ((pit+6) % len(self.pits))
                self.addScore(self.pits[otherPit] + 1)
                self.pits[pit] = 0
                self.pits[otherPit] = 0

        if not stoppedInPit:
            self.turn = (self.turn + 1) % 2


board = boardClass()

while board.winner is None:
    print(f"Player {board.turn+1}'s turn ({'top' if board.turn == 0 else 'bottom'})")
    print(f"""
    |{board.player1.score}|{board.pits[0:6][::-1]}| |
    | |{board.pits[6:12]}|{board.player2.score}|
    """.strip("\n"))
    pit = int(input("Select pit (0-5):"))%6
    if board.turn == 0: pit = 5-pit
    board.move(pit)

print("Final score:")
print("Player 1:", board.player1.score)
print("Player 2:", board.player2.score)

if board.winner == 0:   print("Player 1 wins!")
elif board.winner == 1: print("Player 2 wins!")
else:                   print("Tie!")
