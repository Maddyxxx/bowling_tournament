# -*- coding: utf-8 -*-
import unittest

from bowling import Game, NewGame, Throw1, Throw2, NewThrow1, NewThrow2, play


class Throw1Test(unittest.TestCase):

    def setUp(self):
        self.game_result = list('3532X332/3/62--62X')
        self.frames = [['3', '5'], ['3', '2']]
        self.game = Game
        self.throw = Throw1

    def test_count_points(self):
        self.game.score = 0
        self.game.frames = [['3', '5'], ['3', '2']]
        self.throw.count_points(self)
        self.assertEqual(self.game.score, 3)


class Throw2Test(unittest.TestCase):

    def setUp(self):
        self.game = Game
        self.n = 10
        self.throw = Throw2
        self.game_result = list('3532X332/3/62--62X')

    def test_count_points(self):
        self.game.score = 0
        self.game.frames = [['4', '5'], ['3', '2']]
        self.throw.count_points(self)
        self.assertEqual(self.game.score, 10)


class NewThrow1Test(unittest.TestCase):

    def setUp(self):
        self.game_result = list('3532X332/3/62--62X')
        self.game = NewGame
        self.throw = NewThrow1

    def test_count_points(self):
        self.game.score = 0
        self.game.current_frame = ['X']
        self.game.frames = [['3', '/'], ['X']]
        self.throw.count_points(self)
        self.assertEqual(self.game.score, 3)


class NewThrow2Test(unittest.TestCase):

    def setUp(self):
        self.game = NewGame
        self.throw = NewThrow2
        self.game_result = list('3532X332/3/62--62X')

    def test_count_points(self):
        self.game.score = 0
        self.game.frames = [['3', '/'], ['X']]
        self.game.current_frame = ['3', '/']
        self.throw.count_points(self)
        self.assertEqual(self.game.score, 10)


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = Game
        self.game.score = None
        self.rules = 'old'

    def test_play(self):
        self.game = Game
        self.game.score = play('3-6/5/9/5---1/--5-52', self.rules)
        self.assertEqual(self.game.score, 80)

    def test_errors(self):
        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--327-18812382', self.rules)

        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--327-18812380', self.rules)

        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--///327-18812382', self.rules)

        with self.assertRaises(TypeError):
            self.game.score = play(123, self.rules)


class NewGameTest(unittest.TestCase):

    def setUp(self):
        self.game = NewGame
        self.game.score = None
        self.game.frames = None

    def test_play(self):
        rules = 'new'
        self.game = NewGame
        self.game.score = play('3-6/5/9/5---1/--5-52', rules)  # 3+0 + 10+5 + 10+9 + 10+5 + 5 + 0 + 10+0 + 0 + 5 + 5+2
        self.assertEqual(self.game.score, 79)

        self.game.score = play('XXXXXXXXXX', rules)
        self.assertEqual(self.game.score, 240 + 20 + 10)  # 8 страйков подряд по 30 очков, + 2 последних по 20 и 10,
        # тк следующих бросков нет

    def test_errors(self):
        rules = 'new'

        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--327-18812382', rules)

        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--327-18812380', rules)

        with self.assertRaises(NameError):
            self.game.score = play('1/6/1/--///327-18812382', rules)

        with self.assertRaises(TypeError):
            self.game.score = play(123, rules)


if __name__ == '__main__':
    unittest.main()
