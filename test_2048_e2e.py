import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import sys
import os

class Test2048Game(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game_process = subprocess.Popen([sys.executable, 'pytk2048.py'])
        time.sleep(2)

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000")

    def test_game_initialization(self):
        board = self.get_board_state()
        non_empty_cells = sum(1 for row in board for cell in row if cell != 0)
        self.assertEqual(non_empty_cells, 2, "В начале игры должно быть ровно 2 плитки")

    def test_basic_moves_and_merge(self):
        self.send_move(Keys.RIGHT)
        self.send_move(Keys.LEFT)
        board = self.get_board_state()
        self.assertNotEqual(board, [[0]*4 for _ in range(4)], 
                          "После ходов поле должно измениться")

    def test_score_increase_after_merge(self):
        initial_score = self.get_score()
        self.set_board_state([[2, 2, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        
        self.send_move(Keys.RIGHT)
        new_score = self.get_score()
        self.assertGreater(new_score, initial_score, 
                          "Счет должен увеличиться после слияния плиток")

    def test_game_over_detection(self):
        self.set_board_state([[2, 4, 2, 4],
                            [4, 2, 4, 2],
                            [2, 4, 2, 4],
                            [4, 2, 4, 2]])
        
        self.assertTrue(self.is_game_over(), 
                       "Игра должна закончиться, когда нет возможных ходов")

    def test_move_to_edge(self):
        self.set_board_state([[0, 0, 0, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        
        self.send_move(Keys.LEFT)
        board = self.get_board_state()
        self.assertEqual(board[0][0], 2, 
                        "Плитка должна переместиться к левому краю")

    def test_multiple_merges_in_one_move(self):
        self.set_board_state([[2, 2, 2, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        
        self.send_move(Keys.RIGHT)
        board = self.get_board_state()
        self.assertEqual(board[0][2:], [4, 4], 
                        "Должно произойти два слияния за один ход")

    def test_no_merge_different_values(self):
        self.set_board_state([[2, 4, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        
        self.send_move(Keys.RIGHT)
        board = self.get_board_state()
        self.assertEqual(board[0][2:], [2, 4], 
                        "Плитки с разными значениями не должны сливаться")

    def test_ui_elements_present(self):
        """Проверка наличия всех элементов интерфейса"""
        score_label = self.driver.find_element(By.ID, "score-label")
        self.assertTrue(score_label.is_displayed(), "Счет должен быть виден")
        
        game_grid = self.driver.find_element(By.ID, "game-grid")
        self.assertTrue(game_grid.is_displayed(), "Игровое поле должно быть видно")
        
        cells = game_grid.find_elements(By.CLASS_NAME, "grid-cell")
        self.assertEqual(len(cells), 16, "Должно быть 16 клеток")

    def test_invalid_moves(self):
        """Проверка некорректных действий пользователя"""
        # Проверка нажатия неправильных клавиш
        self.driver.find_element(By.TAG_NAME, "body").send_keys('q')
        board_before = self.get_board_state()
        time.sleep(0.1)
        board_after = self.get_board_state()
        self.assertEqual(board_before, board_after, 
                        "Неправильные клавиши не должны влиять на игру")
        
        # Проверка быстрых последовательных нажатий
        self.send_move(Keys.RIGHT)
        time.sleep(0.01)  # Слишком быстрое нажатие
        self.send_move(Keys.LEFT)
        self.assertTrue(self.is_move_animation_complete(), 
                       "Анимация должна завершиться перед следующим ходом")

    def test_error_handling(self):
        """Проверка обработки ошибок"""
        # Проверка восстановления после сбоя
        self.simulate_crash()
        self.assertTrue(self.is_game_recovered(), 
                       "Игра должна восстановиться после сбоя")
        
        # Проверка сохранения состояния при ошибке
        score_before = self.get_score()
        self.simulate_error()
        score_after = self.get_score()
        self.assertEqual(score_before, score_after, 
                        "Счет не должен меняться при ошибке")

    def get_board_state(self):
        """Получение текущего состояния игрового поля"""
        pass

    def set_board_state(self, board):
        """Установка состояния игрового поля"""
        pass

    def get_score(self):
        """Получение текущего счета"""
        pass

    def is_game_over(self):
        """Проверка окончания игры"""
        pass

    def send_move(self, key):
        """Отправка хода"""
        pass

    def find_element(self, by, value):
        """Поиск элемента на странице"""
        pass

    def send_key(self, key):
        """Отправка нажатия клавиши"""
        pass

    def is_move_animation_complete(self):
        """Проверка завершения анимации"""
        pass

    def simulate_crash(self):
        """Симуляция сбоя приложения"""
        pass

    def simulate_error(self):
        """Симуляция ошибки"""
        pass

    def is_game_recovered(self):
        """Проверка восстановления игры"""
        pass

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        cls.game_process.terminate()

if __name__ == '__main__':
    unittest.main()
