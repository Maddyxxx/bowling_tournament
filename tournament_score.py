from collections import defaultdict
from operator import itemgetter

from prettytable import PrettyTable

import bowling


class GetScoreFromTournament:

    def __init__(self, input_file, output_file, rules):
        self.input_data = []
        self.input_file = input_file
        self.output_file = output_file
        self.rating_players = {}
        self.rules = rules

    def get_data(self):
        work_list = []
        with open(self.input_file, 'r', encoding='utf8') as file:
            for line in file:
                if '###' in line:
                    if work_list:
                        self.input_data.append(work_list)
                    work_list = [line]
                else:
                    work_list.append(line)
            self.input_data.append(work_list)
        return self.input_data

    def get_tours(self):
        all_tours = []
        for tour in self.get_data():
            tour_data = []
            tour_number = 0
            for line in tour:
                if '###' in line:
                    tour_number = line.split(' ')[2][:-1]
                else:
                    if len(line.split('\t')) == 2:
                        tour_data.append(line.split('\t'))
            all_tours.append((tour_number, tour_data))
        return all_tours

    def tour_data_score(self):
        tours_data = []
        for tour in self.get_tours():
            data_tour = []
            for name, result in tour[1]:
                try:
                    score = bowling.play(result[:-1], self.rules)
                except Exception as exc:
                    score = str(exc)
                data_tour.append((score, name, result[:-1]))
            try_find_winner = [i for i in data_tour if isinstance(i[0], int)]
            if try_find_winner:
                winner = max(try_find_winner)[1]
            else:
                winner = 'Нет победителя'
            tours_data.append((tour[0], data_tour, winner))
        return tours_data

    def write_result(self):
        with open(self.output_file, 'w', encoding='utf8') as file:
            for tour in self.tour_data_score():
                tour_number, data_tour, winner = tour[0], tour[1], tour[2]
                file.write(f'### Tour {tour_number}\n')
                for score, name, result in tour[1]:
                    file.write("{0:<10}{1:<25}{2:<4}\n".format(name, result, score))
                file.write(f'winner is {winner}\n')
                file.write(f'\n')

    def get_player_rating(self):
        for tour in self.tour_data_score():
            tour_number, data_tour, winner = tour[0], tour[1], tour[2]
            for score, name, result in data_tour:
                if name in self.rating_players:
                    self.rating_players[name]['games'] += 1
                else:
                    self.rating_players[name] = defaultdict(int)
            if winner in self.rating_players:
                self.rating_players[winner]['wins'] += 1

        return self.rating_players

    def show_player_rating(self):
        list_for_sort = []
        for name in self.rating_players:
            data = {'name': name, 'games': self.rating_players[name]['games'],
                    'wins': self.rating_players[name]['wins']}
            list_for_sort.append(data)

        sorted_data = sorted(list_for_sort, key=itemgetter('wins'), reverse=True)

        columns = ['Игрок', 'Сыграно матчей', 'Всего побед']
        table = PrettyTable(columns)

        for data in sorted_data:
            table.add_row([data['name'], data['games'], data['wins']])

        return table


def get_score(input_file, output_file, rules):
    gsft = GetScoreFromTournament(input_file, output_file, rules)
    gsft.write_result()
    gsft.get_player_rating()
    rating = gsft.show_player_rating()
    return rating




