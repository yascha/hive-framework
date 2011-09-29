import argparse
import logging
import os
import shlex
import subprocess
import sys
from time import time
from cmd2 import Cmd
from errors import *
from game import *

#logging.basicConfig(level=logging.DEBUG)

class Framework():
  def __init__(self, args):
    self.args = self._parseArgs(args)

  def _parseArgs(self, args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--white')
    parser.add_argument('--black')
    parser.add_argument('--times', default='30000,0,0')
    parser.add_argument('--moves', default='')
    args = parser.parse_args(args.split())
    args = vars(args)
    logging.debug('Framework._parseArgs: args = ' + str(args))
    return args

  def run(self):
    self.args['white'] = self.readBot('white', self.args['white'])
    self.args['black'] = self.readBot('black', self.args['black'])
    self.game = Game(self.args['white'], self.args['black'], self.args['times'], self.args['moves'])

    while not self.game.isGameOver():
      moveString = self.readMove()
      if moveString == 'quit' or moveString == 'exit':
        break
      try:
        sys.stdout.write(self.game.currentPlayer.color.capitalize() + ' plays ' + moveString + '\n')
        self.game.playMove(moveString)
      except InputError as e:
        sys.stderr.write(e.value + '\n')
        if self.game.currentPlayer.bot: break;
      except MoveError as e:
        sys.stderr.write(e.value + '\n')
        if self.game.currentPlayer.bot: break;
      else:
        self.game.printBoard()


  def readBot(self, color, bot=''):
    while True:
      if not bot:
        bot = raw_input(color.capitalize() + " player bot (blank for human): ")
      else:
        sys.stdout.write(color.capitalize() + " player bot (blank for human): " + bot + "\n")

      if bot == '':
        return None
      elif os.path.exists(bot):
        return bot
      else:
        sys.stdout.write("Couldn't locate the bot. Try again.\n")
        bot = None
    return None


  def readMove(self): 
    moveString = 'error'
    if self.game.currentPlayer.bot:
      try:
        bot = self.game.currentPlayer.bot
        if bot.endswith('.py'):
          bot = 'python ' + bot

        commandLine = bot + ' --times="' + self.game.getTimeControlsCsv() + '" --moves="' + self.game.getMoveListCsv() + '"'
        logging.debug('Framework.readMove: commandLine = ' + commandLine)
        args = shlex.split(commandLine)
        startTime = time()
        botProcess = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=None)
        moveString, errorOutput = botProcess.communicate()
        sys.stderr.write(errorOutput)
        logging.debug('Framework.readMove: moveString = ' + moveString)
        endTime = time()
        totalTime = round((endTime - startTime) * 100)
        self.game.currentPlayer.timeUsed += totalTime
        logging.debug('Framework.readMove: bottime = ' + str(totalTime))
      except OSError as details:
        logging.debug('Framework.readMove: OSError = ' + str(details))
        raise InputError(self.game.currentPlayer.bot + ' process failed to execute')
    else:
      moveString = raw_input(self.game.currentPlayer.color.capitalize() + "'s turn: ")

    return moveString



class HiveCmd(Cmd):
  """ Hive Bot Framework """
  prompt = 'hive> '
  intro = 'Hive Bot Framework\n------------------'

  def do_game(self, args = ''):
    Framework(args).run()


if __name__ == "__main__": 
  HiveCmd().cmdloop() 

