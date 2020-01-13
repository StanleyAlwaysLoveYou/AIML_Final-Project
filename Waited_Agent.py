import numpy as np
from ple import PLE

from ple.games.waterworld import WaterWorld
import time
import os


class WaitedAgent():
    """
        always eat red creep, when eat negative creep, wait for a while then continue
    """
    
    def __init__(self,actions):
        self.action = actions
        self.wait_step = 0

    def nearIndex(self, gamestate):
        index = gamestate['creep_dist']['R'].index(min(gamestate['creep_dist']['R']))
        # print index
        return index

    def pickAction(self, reward, obs, gamestate):
        # if reward !=0:
        #     print "eat creepy:", reward
        if reward<0:
            # print "wait"
            self.wait_step = 100
        # print reward
        if self.wait_step>0:
            self.wait_step = self.wait_step-1
            return None
        
        state = gamestate['creep_pos']['R'][self.nearIndex(gamestate)]
        if abs(gamestate["player_x"]-state[0]) > abs(gamestate["player_y"]-state[1]):
            if gamestate["player_x"] <= state[0] :
                # print "right"
                return 100
            elif gamestate["player_x"] > state[0]:
                # print "left"
                return 97
        else:
            if gamestate["player_y"] <= state[1]:
                # print "down"
                return 115
            elif gamestate["player_y"] > state[1]:
                # print "up"
                return 119


# Don't display window.
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"

# create our game
force_fps = True  # slower speed
display_screen = False 
reward = 0.0
game = WaterWorld()

# make a PLE instance.
p = PLE(game,force_fps=force_fps)

# our Naive agent!
agent = WaitedAgent(p.getActionSet())

# init agent and game.
p.init()
p.display_screen = True


# start our loop
score = 0.0
for i in range(10):
    # if the game is over
    if p.game_over():
        p.reset_game()
    while p.game_over() == False:
        obs = p.getScreenRGB()
        gamestate = p.getGameState()
        action = agent.pickAction(reward, obs, gamestate)
        reward = p.act(action) # reward after an action
    score = game.getScore()
    print "Trial no.{:02d} : score {:0.3f}".format(i,score)

# Screen Shot
#     p.saveScreen("screen_capture.png")
