import copy
import os
from player import Player
import numpy as np
from operator import attrgetter


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # Select based on fitness
        # players.sort(key=lambda x: x.fitness, reverse=True)

        # Roulette Wheel
        # players = self.RouletteWheel(players, num_players)

        # SUS
        players = self.SUS(players, num_players)

        # Q-tournament
        # players = self.Qtournament(players, num_players, 3)

        # Save data to plot learning rates
        self.save_plot_data(players)

        return players[: num_players]

    def generate_new_population(self, num_players, prev_players=None):  # parent selection and child production
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """

        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            new_players = self.crossover(prev_players)
            for child in new_players:
                self.mutate(child)
            return new_players

    def crossover(self, prev_players):
        new_players = []
        for i in range(0, len(prev_players), 2):
            new_child1 = self.clone_player(prev_players[i])
            new_child2 = self.clone_player(prev_players[i + 1])

            if np.random.normal(0, 1) < 0.8:
                for j in range(len(new_child1.nn.w)):
                    shape = new_child1.nn.w[j].shape
                    new_child1.nn.w[j][:, :int(shape[1] / 2)] = prev_players[i+1].nn.w[j][:, :int(shape[1] / 2)]
                    new_child2.nn.w[j][:, :int(shape[1] / 2)] = prev_players[i].nn.w[j][:, :int(shape[1] / 2)]

                for k in range(len(new_child1.nn.b)):
                    shape = new_child1.nn.b[k].shape
                    new_child1.nn.b[k][:, :int(shape[1] / 2)] = prev_players[i + 1].nn.b[k][:, :int(shape[1] / 2)]
                    new_child2.nn.b[k][:, :int(shape[1] / 2)] = prev_players[i].nn.b[k][:, :int(shape[1] / 2)]

                new_players.append(new_child1)
                new_players.append(new_child2)
            else:
                new_players.append(prev_players[i])
                new_players.append(prev_players[i+1])

        return new_players

    def mutate(self, child):
        row = 0.75
        entry = 0.75

        for i in range(len(child.nn.w)):
            if np.random.normal(0, 1) >= row:
                for j in range(len(child.nn.w[i])):
                    if np.random.normal(0, 1) >= entry:
                        child.nn.w[i][j] += np.random.normal(0, 1)
        for i in range(len(child.nn.b)):
            if np.random.normal(0, 1) >= row:
                for j in range(len(child.nn.b[i])):
                    if np.random.normal(0, 1) >= entry:
                        child.nn.b[i][j] += np.random.normal(0, 1)

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player

    def RouletteWheel(self, players, num_player):
        next_generation = []
        probabilities = []
        sum_of_fitness = sum([player.fitness for player in players])
        for player in players:
            probabilities.append(player.fitness / sum_of_fitness)
        selected = np.random.choice(a=players, size=num_player, replace=True, p=probabilities)
        for player in selected:
            child = self.clone_player(player)
            next_generation.append(child)
        return next_generation

    def SUS(self, players, num_players):
        next_generation = []
        probabilities = []
        sum_of_fitness = sum([player.fitness for player in players])
        for player in players:
            probabilities.append(player.fitness/sum_of_fitness)
        for i in range(1, len(players)):
            probabilities[i] += probabilities[i - 1]

        start = np.random.uniform(0, 1 / num_players, 1)
        second_ruler = []
        steps = 1 / num_players
        for i in range(num_players):
            second_ruler.append(start + float(i * steps))

        for point in second_ruler:
            for i, prob in enumerate(probabilities):
                if i == 0:
                    if point < probabilities[i]:
                        next_generation.append(self.clone_player(players[i]))
                else:
                    if probabilities[i-1] < point <= probabilities[i]:
                        next_generation.append(self.clone_player(players[i]))

        return next_generation

    def Qtournament(self, players, num_players, q):
        new_generation = []
        for i in range(num_players):
            q_selected = np.random.choice(players, q)
            new_generation.append(max(q_selected, key=attrgetter('fitness')))

        return new_generation

    def save_plot_data(self, players):
        f = open("plot.txt", "a")
        for player in players:
            f.write(str(player.fitness) + " ")
        f.write("\n")
        f.close()

