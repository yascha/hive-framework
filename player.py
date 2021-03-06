import sys
from pieces import *

class Player:
  (WHITE, BLACK) = ('white', 'black')

  def __init__(self, color, bot, expansions):
    self.bot = bot
    self.color = color
    self.pieces = dict()
    self.setupStartingPieces(color[0], expansions)
    self.seenHiveStates = []
    self.timeUsed = 0


  def setupStartingPieces(self, color, expansions):
    self.pieces['Q'] = QueenBeePiece(color)
    self.pieces['S1'] = SpiderPiece(color, 1)
    self.pieces['S2'] = SpiderPiece(color, 2)
    self.pieces['B1'] = BeetlePiece(color, 1)
    self.pieces['B2'] = BeetlePiece(color, 2)
    self.pieces['A1'] = AntPiece(color, 1)
    self.pieces['A2'] = AntPiece(color, 2)
    self.pieces['A3'] = AntPiece(color, 3)
    self.pieces['G1'] = GrasshopperPiece(color, 1)
    self.pieces['G2'] = GrasshopperPiece(color, 2)
    self.pieces['G3'] = GrasshopperPiece(color, 3)
    if 'M' in expansions:
      self.pieces['M'] = MosquitoPiece(color)
    if 'L' in expansions:
      self.pieces['L'] = LadybugPiece(color)


  def getPiece(self, (color, kind, number)):
    key = kind + str(number)
    return self.pieces[key]


  def hasPlayed(self, kind, number = ''):
    key = kind + str(number)
    return self.pieces[key].isPlayed()


  def getNumberOfPiecesToPlay(self):
    count = 0
    for key, piece in self.pieces.iteritems():
      if not piece.isPlayed():
        count += 1
    return count


  def addHiveState(self, state):
    self.seenHiveStates.append(state)


  def removeHiveState(self):
    if len(self.seenHiveStates):
      self.seenHiveStates.pop()


  def hasSeenThreefoldRepetition(self):
    if len(self.seenHiveStates) < 5:
      return False

    length = len(self.seenHiveStates)
    return self.seenHiveStates[length - 5] == self.seenHiveStates[length - 3] == self.seenHiveStates[length - 1]

  def printPile(self):
    pile = []
    for key in sorted(self.pieces.keys()):
      piece = self.pieces[key]
      if not piece.isPlayed():
        pile.append(piece.getNotation())

    sys.stderr.write("%s's Pile: %s\n" % (self.color.capitalize(), ', '.join(pile)))

