import numpy as np
from ple import PLE

from ple.games.waterworld import WaterWorld
import time
import os

class NaiveAgent():
    """
            This is our naive agent. It picks actions at random!
    """

    def __init__(self, actions):
        self.actions = actions

    def pickAction(self, reward, obs):
        return self.actions[np.random.randint(len(self.actions))]

class RedAgent():
    """
        always eat red creep
    """
    
    def __init__(self,actions):
        self.action = actions

    def nearIndex(self, gamestate):
        index = gamestate['creep_dist']['R'].index(min(gamestate['creep_dist']['R']))
        # print index
        return index

    def pickAction(self, reward, obs, gamestate):
        # print reward
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

class GreedyAgent():
    """
        when eat the negative creep, change color
    """

    def __init__(self,actions):
        self.action = actions
        self.colors = ['R','G','Y']
        self.color = 'R'

    def nearIndex(self, gamestate):
        index = gamestate['creep_dist'][self.color].index(min(gamestate['creep_dist'][self.color]))
        # print index
        return index

    def pickAction(self, reward, obs, gamestate):
        # print reward
        # print self.color
        # if reward != 0:
            # print "eat creepy:", reward
        if reward<0:
            self.colors.remove(self.color)
            self.color = self.colors[np.random.randint(len(self.colors))]
            self.colors = ['R','G','Y']
            # print "change color to", self.color
        state = gamestate['creep_pos'][self.color][self.nearIndex(gamestate)]
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


# preprocessor example
# def nv_state_preprocessor(state):

#     colors = ['G','R','Y']
#     val = state.values()
#     x_pos = state['player_x']/256.0
#     y_pos = state['player_y']/256.0
#     x_vel = state['player_velocity_x']/64.0
#     y_vel = state['player_velocity_y']/64.0
#     tmp = state['creep_pos']
#     all_pos = np.array([])
#     for color in colors:
#         for position in tmp[color]:
#             k = np.array(position)/256.0
#             all_pos = np.append(all_pos,k)
#     all_dist = np.array([])
#     tmp = state['creep_dist']

#     for color in colors:
#         k = np.array(tmp[color])/362.1
#         all_dist = np.append(all_dist,k)

#     all_state = np.append([x_pos,y_pos,x_vel,y_vel],all_pos)

#     return all_state.flatten()


###################################


# Don't display window.
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# create our game
force_fps = True  # slower speed
display_screen = False 
reward = 0.0
game = WaterWorld()

# make a PLE instance.
p = PLE(game,force_fps=force_fps)

# our Naive agent!
agent = GreedyAgent(p.getActionSet())
print "action set: ", p.getActionSet()

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
