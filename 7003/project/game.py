import math
import random
import copy
import json
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Game:
    def __init__(self):
        self.tanks = ['LA', 'LB', 'LC', 'RA', 'RB', 'RC']
        self.players = ['U', 'D']
        self.row_id = {'U': {'LA': 3, 'LB': 4, 'LC': 5, 'RA': 2, 'RB': 1, 'RC': 0},
                       'D': {'LA': 2, 'LB': 1, 'LC': 0, 'RA': 3, 'RB': 4, 'RC': 5}}
        self.half_length = 3
        self.length = 6
        self.max_moves = self.half_length * 2 - 1
        self.player_tanks = None
        self.boxes = None
        self.rounds = None
        self.print = False

    def init(self):
        self.player_tanks = {}
        for player in self.players:
            self.player_tanks[player] = {}
            for tank in self.tanks:
                self.player_tanks[player][tank] = 0
                self.player_tanks[player][tank] = 0
        self.boxes = [[player for _ in self.tanks] for player in self.players for _ in range(self.half_length)]
        self.rounds = 0
        # print("Game Start:")

    def round(self, choices=None):
        if not choices:
            choices = self.move_policy()
        if '' in choices.values():
            return False
        self.rounds += 1
        if self.print:
            print("Round", self.rounds, ":")
        self.move(choices)
        self.fire()
        return True

    def next(self, choices):
        self.older_player_tanks = copy.deepcopy(self.player_tanks)
        self.older_boxes = copy.deepcopy(self.boxes)
        self.move(choices)
        self.fire()

    def roll_back(self):
        self.player_tanks = self.older_player_tanks
        self.boxes = self.older_boxes
    def move_policy(self):
        choices = {}
        for player in self.players:
            move_tanks = []
            for tank in self.tanks:
                if self.can_move(player, tank):
                    move_tanks.append(tank)
            if not move_tanks:
                choices[player] = ''
            else:
                choices[player] = random.choice(move_tanks)
        return choices

    def move(self, choices):
        text = []
        for player in self.players:
            self.player_tanks[player][choices[player]] += 1
            text.append(player + "：" + choices[player])
        if self.print:
            print("  " + "; ".join(text))
        for player in self.players:
            if self.player_tanks[player][choices[player]] == self.max_moves - self.opponent(player, choices[player]):
                if player != self.box_belong(player, choices[player], self.player_tanks[player][choices[player]]):
                    self.player_tanks[player][choices[player]] -= 1
            self.box_occupy(player, choices[player], self.player_tanks[player][choices[player]])

    def fire(self):
        fire_list = {}
        fire_flag = False
        for player in self.players:
            fire_list[self.opponent(player)] = []
            for tank in self.tanks:
                if self.player_tanks[player][tank] >= 0:
                    for key, value in self.fire_obj(tank, self.player_tanks[player][tank]).items():
                        if self.opponent(player, key, False) in value:
                            fire_list[self.opponent(player)].append(key)
                            if self.print:
                                print("  " + player + "'s " + tank + " destroys " + self.opponent(player) + "'s " + key)
                            fire_flag = True
        for player in self.players:
            for tank in fire_list[player]:
                self.player_tanks[player][tank] = -self.half_length
        if not fire_flag:
            pass
            if self.print:
                print("  No Fire")

    def can_move(self, player, tank):
        return 0 <= self.player_tanks[player][tank] < self.max_moves

    def box_occupy(self, player, tank, moves):
        self.boxes[moves if player == self.players[0] else self.max_moves - moves][self.row_id[player][tank]] = player

    def box_belong(self, player, tank, moves):
        return self.boxes[self.row_id[player][tank]][moves if player == self.players[0] else self.max_moves - moves]

    def opponent(self, player, tank=None, reverse=True):
        op = self.players[0] if player == self.players[1] else self.players[1]
        if tank:
            if reverse:
                ot = 'R' + tank[1] if tank[0] == 'L' else 'L' + tank[1]
            else:
                ot = tank
            return self.player_tanks[op][ot]
        else:
            return op

    def fire_obj(self, tank, moves):
        if tank == 'LA':
            return {'LA': [self.max_moves - moves - 1, self.max_moves - moves + 1],
                    'RB': [self.max_moves - moves - 1, self.max_moves - moves + 1]}
        elif tank == 'RA':
            return {'RA': [self.max_moves - moves - 1, self.max_moves - moves + 1],
                    'LB': [self.max_moves - moves - 1, self.max_moves - moves + 1]}
        elif tank == 'LB':
            return {'RA': [self.max_moves - moves],
                    'RB': [self.max_moves - moves - 1],
                    'RC': [self.max_moves - moves]}
        elif tank == 'RB':
            return {'LA': [self.max_moves - moves],
                    'LB': [self.max_moves - moves - 1],
                    'LC': [self.max_moves - moves]}
        elif tank == 'LC':
            return {'RA': [self.max_moves - moves],
                    'RC': [self.max_moves - moves - 2, self.max_moves - moves + 2]}
        elif tank == 'RC':
            return {'LA': [self.max_moves - moves],
                    'LC': [self.max_moves - moves - 2, self.max_moves - moves + 2]}

    def get_current_state(self):
        tanks = "".join([str(value) for player in self.players for value in self.player_tanks[player].values()])
        columns = [0] * 6
        for i, column in enumerate(self.boxes):
            for j, box in enumerate(column):
                columns[i] |= (box == 'D') << j
        state = tanks + "".join([str(value) for value in columns])
        return state

    def display(self):
        size = 7
        boxes = []
        for c in self.boxes:
            column = []
            for r in c:
                if r == self.players[0]:
                    column.append((255, 255, 255))
                else:
                    column.append((127, 127, 127))
            boxes.append(column)
        boxes = np.array(boxes)

        # Reshape things into a 9x9 grid.

        row_labels = [str(i) for i in range(size)]
        col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        for i in range(size):
            plt.hlines(i-0.5, -0.5, size - 0.5, color="black")
            plt.vlines(i-0.5, -0.5, size - 0.5, color="black")

        for item in self.player_tanks[self.players[0]].items():
            if item[1] >= 0:
                self.paint_node(self.row_id[self.players[0]][item[0]], item[1], item[0], 'orange')
        for item in self.player_tanks[self.players[1]].items():
            if item[1] >= 0:
                self.paint_node(self.row_id[self.players[1]][item[0]], self.max_moves - item[1], item[0], 'blue')
        plt.xticks(range(size), col_labels)
        plt.yticks(range(size), row_labels)
        plt.imshow(boxes)
        plt.show()

    def paint_node(self, a, b, text, color):
        r = 0.3
        theta = np.arange(0, 2 * np.pi, 0.01)
        x = a + r * np.cos(theta) * 1.5
        y = b + r * np.sin(theta) * 1.5
        plt.plot(x, y, c=color)
        plt.text(a - r * 1.2, b - r * 0.8 + 0.4, text, fontdict={'family': 'Times New Roman', 'size': 24, 'color': color})
    def end(self):
        cnt = {}
        for player in self.players:
            cnt[player] = 0
            for tank in self.tanks:
                if self.player_tanks[player][tank] >= 0:
                    cnt[player] += 1

        if cnt[self.players[0]] > cnt[self.players[1]]:
            # return self.players[0]
            return 1
        elif cnt[self.players[0]] < cnt[self.players[1]]:
            # return self.players[1]
            return -1
        else:
            for columns in self.boxes:
                for player in columns:
                    cnt[player] += 1
            if cnt[self.players[0]] > cnt[self.players[1]]:
                # return self.players[0]
                return 1
            elif cnt[self.players[0]] < cnt[self.players[1]]:
                # return self.players[1]
                return -1
            else:
                return 0


def simulate(values):
    game = Game()
    game.init()
    states = []
    choices = []
    while True:
        state = game.get_current_state()
        choice = policy(values, game)
        if not game.round(choice):
            break
        states.append(state)
        choices.append(choice)
    winner = game.end()
    # if winner == 0:
    #     print("Draw")
    # else:
    #     print("Winner is " + winner)
    for i in range(len(states)):
        update_values(states[-i], choices[-i][game.players[0]], winner, values)



def learning(cnt):
    values = {}
    for i in range(cnt):
        simulate(values)
        state = ('000000000000000636363')
        if i % 10000 == 0:
            print(i, values[state])
    return values

def gaming(values):
    game = Game()
    game.init()
    game.print = True
    print("Game Start")
    print("Your Role is Down")
    # while True:
    #     action = input("  Please input your action: ")
    #     state = game.get_current_state()
    #     break
    while True:
        game.display()
        choices = policy(values, game)
        action = input("Please input your action: ").strip().upper()
        choices[game.players[1]] = action
        if not game.round(choices):
            break
    winner = game.end()
    if winner == 1:
        print("Winner is Up")
    elif winner == -1:
        print("Winner is Down")
    else:
        print("Draw")

def update_values(state, action, reward, values):
    if state in values:
        values[state][action][1] += 1
        values[state][action][0] += (reward - values[state][action][0]) / values[state][action][1]
        values[state][""][0] = -1.0
        values[state][""][1] += 1
        for a in ['LA', 'LB', 'LC', 'RA', 'RB', 'RC']:
            if values[state][""][0] < values[state][a][0]:
                values[state][""][0] = values[state][a][0]
    else:
        values[state] = {"": [reward, 1], 'LA': [-3, 0], 'LB': [-2, 0], 'LC': [-1, 0], 'RA': [-3, 0], 'RB': [-2, 0],
                         'RC': [-1, 0]}
        values[state][action] = [reward, 1]


def policy(values, game:Game):
    # 超参数，alpha控制UCB增长率，epsilon控制soft-greedy阈值，建议alpha<=1
    alpha = 0.95
    epsilon = 0.05

    print_flag = game.print
    game.print = False
    choices = {}
    state = game.get_current_state()

    move_tanks = []
    for tank in game.tanks:
        if game.can_move(game.players[0], tank):
            move_tanks.append(tank)
    if not move_tanks:
        choices[game.players[0]] = ''
    elif state in values:
        # epsilon = 0.05
        # if random.random() < epsilon:
        #     choices[game.players[0]] = random.choice(move_tanks)
        # else:
        #     max_value = -1
        #     for tank in move_tanks:
        #         if values[state][tank][0] > max_value:
        #             max_value = values[state][tank][0]
        #
        #     select_tanks = []
        #     for tank in move_tanks:
        #         if values[state][tank][0] == max_value:
        #             select_tanks.append(tank)
        #     choices[game.players[0]] = random.choice(select_tanks)
        bounds = {}
        for tank in move_tanks:
            if values[state][tank][1] == 0:
                bounds[tank] = 50
            else:
                bounds[tank] = round(values[state][tank][0] + alpha * math.sqrt(math.log(values[state][""][1]) / values[state][tank][1]))
        max_value = max(bounds.values())
        select_tanks = []
        for tank in move_tanks:
            if bounds[tank] == max_value:
                select_tanks.append(tank)
        choices[game.players[0]] = random.choice(select_tanks)
    else:
        choices[game.players[0]] = random.choice(move_tanks)

    move_tanks = []
    for tank in game.tanks:
        if game.can_move(game.players[1], tank):
            move_tanks.append(tank)
    if not move_tanks or choices[game.players[0]] == '':
        choices[game.players[1]] = ""
    else:
        if random.random() >= epsilon:
            action_values = {}
            for tank in move_tanks:
                choices[game.players[1]] = tank
                game.next(choices)
                next_state = game.get_current_state()
                if next_state in values:
                    action_values[tank] = values[next_state][""][0]
                else:
                    action_values[tank] = 0
                game.roll_back()
            min_value = 1
            for tank in move_tanks:
                if action_values[tank] < min_value:
                    min_value = action_values[tank]
            select_tanks = []
            for tank in move_tanks:
                if action_values[tank] == min_value:
                    select_tanks.append(tank)
            choices[game.players[1]] = random.choice(select_tanks)
        else:
            choices[game.players[1]] = random.choice(move_tanks)

    game.print = print_flag
    return choices


def load_values():
    values = {}
    with open('values.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
        for item in items:
            values[item['state']] = item['value']
    return values


if __name__ == "__main__":
    # game_cnt = 10000000
    # values = learning(game_cnt)
    # values_list = [{'state': item[0], 'value': item[1]} for item in values.items()]
    # values_json = json.dumps(values_list, sort_keys=False, indent=4, separators=(',', ': '))
    # with open('values.json', 'w') as file:
    #     file.write(values_json)
    values = load_values()
    gaming(values)
    # if winner == 0:
    #     print("Draw")
    # else:
    #     print("Winner is " + winner)