class Throw:

    def __init__(self, game_result, game):
        self.game = game
        self.game_result = game_result


class Throw1(Throw):

    def count_points(self):
        current_throw = self.game_result.pop(0)

        if current_throw == 'X':
            self.game.score += 20

        elif current_throw == '/':
            raise NameError(f'Проверьте значение броска "{current_throw}"')

        else:
            if current_throw != '-':
                self.game.prev_throw = int(current_throw)
                self.game.score += int(current_throw)
            self.game.state = Throw2(self.game_result, self.game)


class Throw2(Throw):

    def count_points(self):
        current_throw = self.game_result.pop(0)

        if current_throw == 'X':
            raise NameError(f'Проверьте значение броска "{current_throw}"')

        elif current_throw == '/':
            self.game.score += 15
            self.game.score -= self.game.prev_throw
            self.game.state = Throw1(self.game_result, self.game)

        else:
            if current_throw != '-':
                self.game.score += int(current_throw)
            self.game.state = Throw1(self.game_result, self.game)


class NewThrow1(Throw):

    def count_points(self):
        current_throw = self.game_result.pop(0)
        current_frame = self.game.frames.pop(0)
        self.game.current_frame = current_frame

        if current_throw == 'X':
            self.game.score += 10
            if 'X' in current_frame:
                print(f'отлично, в текущем фрейме {current_frame} страйк, '
                      f'поэтому пробуем подсчитать очки в двух следующих бросках ')
                try:
                    extra_frame_1 = self.game.frames[0]
                    print(f'Пробуем взять следующий фрейм {extra_frame_1}')
                    if 'X' in extra_frame_1:
                        print(f'отлично, в следующем фрейме {extra_frame_1} страйк, '
                              f'поэтому прибавляем 10 очков ')
                        self.game.score += 10
                        try:
                            extra_frame_2 = self.game.frames[1]
                            print(f'Пробуем взять второй следующий фрейм {extra_frame_2}')
                            if 'X' in extra_frame_2:
                                print(f'отлично, во втором следующем фрейме {extra_frame_2} страйк, '
                                      f'поэтому прибавляем 10 очков ')
                                self.game.score += 10
                            else:
                                print(f'отлично, во втором следующем фрейме {extra_frame_2} нет страйка, '
                                      f'поэтому прибавляем количество сбитых кеглей {extra_frame_2[0]} ')
                                self.game.score += int(extra_frame_2[0])

                        except Exception as exc_2:
                            print('второго следующего броска нет, но у нас страйк, поэтому +10 очков')
                    elif '/' in extra_frame_1:
                        print(f'отлично, в следующем фрейме {extra_frame_1} spare, '
                              f'поэтому прибавляем 10 очков ')
                        self.game.score += 10
                    else:
                        print(f' в следующем фрейме {extra_frame_1} нет ни страйка, ни spare, '
                              f'поэтому прибавляем {extra_frame_1[0]} + {extra_frame_1[1]} очков ')
                        self.game.score += int(extra_frame_1[0]) + int(extra_frame_1[1])
                except Exception as exc_1:
                    print(f'следующих бросков нет, +10 очков')

        elif current_throw == '/':
            raise NameError(f'Проверьте значение броска "{current_throw} фрейма {current_frame}"')

        else:
            if current_throw != '-':
                self.game.prev_throw = int(current_throw)
                self.game.score += int(current_throw)
            self.game.state = NewThrow2(self.game_result, self.game)

        print(f'Очков после 1 броска - {self.game.score}')


class NewThrow2(Throw):

    def count_points(self):
        current_throw = self.game_result.pop(0)
        current_frame = self.game.current_frame

        if current_throw == 'X':
            raise NameError(f'Проверьте значение броска "{current_throw}" во фрейме {current_frame} ')

        elif current_throw == '/':
            print('Ура! У нас spare, +10 очков')
            self.game.score += 10
            self.game.score -= self.game.prev_throw
            try:
                extra_frame = self.game.frames[0]
                print(f'Пробуем взять очки из следущего фрейма {extra_frame}')
                if 'X' in extra_frame:
                    print(f'Ура, во врейме {extra_frame} страйк, +10 очков')
                    self.game.score += 10
                else:
                    print(f'во фрейме {extra_frame} нет страйка, поэтому + {extra_frame[0]} очков')
                    self.game.score += int(extra_frame[0])
            except Exception as exc:
                print(f'У нас spare, но следующих бросков нет, поэтому +10 очков')

            self.game.state = NewThrow1(self.game_result, self.game)

        else:
            if current_throw != '-':
                self.game.score += int(current_throw)
            self.game.state = NewThrow1(self.game_result, self.game)

        print(f'Очков после 2 броска - {self.game.score}')


class Game:

    def __init__(self, game_result):
        self.game_result = list(game_result)
        self.score, self.prev_throw = 0, None
        self.state = Throw1(self.game_result, game=self)

    def count_points(self):
        while self.game_result:
            self.state.count_points()


class NewGame:

    def __init__(self, game_result):
        self.game_result = list(game_result)
        self.frames = Check(self.game_result).check_frames()
        self.score, self.prev_throw, self.current_frame = 0, None, 0
        self.state = NewThrow1(self.game_result, game=self)

    def count_points(self):
        while self.game_result:
            self.state.count_points()


class Check:

    def __init__(self, game_result):
        self.game_result = game_result
        self.symbols = ['X', '/', '-', ]

    def check_game_result(self):

        if not isinstance(self.game_result, str):
            raise TypeError('Неверный формат. Результат должен быть строкой')

        spare_count, strikes, check_spare = 0, 0, 0
        game_result = list(self.game_result)

        for frame in game_result:
            if frame in self.symbols:
                strikes += frame == 'X'
                check_spare += frame == '/'
            elif frame == '0':
                raise NameError('Введены неверные символы, возможно Вы хотели написать "-" вместо "0"')
            else:
                try:
                    int(frame)
                except NameError as exc:
                    f'Введены неверные символы, {exc}'

        if check_spare > 10:
            raise NameError('Слишком много spare')

        check = len(game_result) + strikes

        if check < 20:
            raise NameError('введено недостаточное количество символов')
        elif check > 20:
            raise NameError('введено слишком много символов')

    def check_frames(self):
        game_result = list(self.game_result)
        frames, frame = [], []

        for symbol in game_result:
            if symbol == 'X':
                frames.append([symbol])
            else:
                if symbol == '-':
                    frame.append(0)
                else:
                    frame.append(symbol)
            if len(frame) == 2:
                frames.append(frame)
                frame = []

        for frame in frames:
            if 'X' not in frame and '/' not in frame:
                if int(frame[0]) + int(frame[1]) == 10:
                    raise NameError(f'Недопустимая комбинация фрейма "{frame[0]}{frame[1]}" ')

        return frames


def play(game_result, rules):
    check = Check(game_result)
    check.check_game_result()
    check.check_frames()

    if rules == 'old':
        game = Game(game_result)
    else:
        game = NewGame(game_result)

    game.count_points()
    return game.score
