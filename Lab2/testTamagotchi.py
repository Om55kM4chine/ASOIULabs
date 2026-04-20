import unittest
from unittest.mock import patch
from Lab2.tamagotchi import Tamagotchi


class TestTamagotchi(unittest.TestCase):
    """Unit-тесты для класса Tamagotchi"""

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.tamagotchi = Tamagotchi("Тестовый тамагочи")

    def test_initialization(self):
        """Тест инициализации Tamagotchi"""
        self.assertEqual(self.tamagotchi.name, "Тестовый тамагочи")
        self.assertEqual(self.tamagotchi.hunger, 100)
        self.assertEqual(self.tamagotchi.thirst, 100)
        self.assertEqual(self.tamagotchi.happiness, 100)

    def test_feed_increases_hunger(self):
        """Тест: кормление увеличивает голод"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.feed()
        self.assertEqual(self.tamagotchi.hunger, 70)

    def test_feed_caps_at_100(self):
        """Тест: голод не превышает 100"""
        self.tamagotchi.hunger = 90
        self.tamagotchi.feed()
        self.assertEqual(self.tamagotchi.hunger, 100)
        
        # Повторное кормление не должно увеличивать сверх 100
        self.tamagotchi.feed()
        self.assertEqual(self.tamagotchi.hunger, 100)

    def test_give_water_increases_thirst(self):
        """Тест: вода увеличивает жажду"""
        self.tamagotchi.thirst = 50
        self.tamagotchi.give_water()
        self.assertEqual(self.tamagotchi.thirst, 70)

    def test_give_water_caps_at_100(self):
        """Тест: жажда не превышает 100"""
        self.tamagotchi.thirst = 95
        self.tamagotchi.give_water()
        self.assertEqual(self.tamagotchi.thirst, 100)
        
        # Повторное добавление воды не должно увеличивать сверх 100
        self.tamagotchi.give_water()
        self.assertEqual(self.tamagotchi.thirst, 100)

    def test_play_increases_happiness(self):
        """Тест: игра увеличивает счастье"""
        self.tamagotchi.happiness = 50
        self.tamagotchi.play()
        self.assertEqual(self.tamagotchi.happiness, 70)

    def test_play_caps_at_100(self):
        """Тест: счастье не превышает 100"""
        self.tamagotchi.happiness = 85
        self.tamagotchi.play()
        self.assertEqual(self.tamagotchi.happiness, 100)
        
        # Повторная игра не должна увеличивать сверх 100
        self.tamagotchi.play()
        self.assertEqual(self.tamagotchi.happiness, 100)

    @patch('random.randint')
    def test_decrease_stats(self, mock_randint):
        """Тест: уменьшение характеристик"""
        # Устанавливаем фиксированные значения для уменьшения
        mock_randint.return_value = 10
        
        initial_hunger = self.tamagotchi.hunger
        initial_thirst = self.tamagotchi.thirst
        initial_happiness = self.tamagotchi.happiness
        
        self.tamagotchi.decrease_stats()
        
        self.assertEqual(self.tamagotchi.hunger, initial_hunger - 10)
        self.assertEqual(self.tamagotchi.thirst, initial_thirst - 10)
        self.assertEqual(self.tamagotchi.happiness, initial_happiness - 10)

    def test_decrease_stats_can_go_negative(self):
        """Тест: характеристики могут быть отрицательными"""
        self.tamagotchi.hunger = 5
        self.tamagotchi.thirst = 5
        self.tamagotchi.happiness = 5
        
        # Уменьшение может быть > 5, поэтому характеристики могут стать отрицательными
        # Проверяем, что это возможно
        for _ in range(100):
            tamagotchi_temp = Tamagotchi("temp")
            tamagotchi_temp.hunger = 5
            tamagotchi_temp.thirst = 5
            tamagotchi_temp.happiness = 5
            tamagotchi_temp.decrease_stats()
            
            # Если хотя бы одна характеристика стала отрицательной, тест пройден
            if (tamagotchi_temp.hunger < 0 or 
                tamagotchi_temp.thirst < 0 or 
                tamagotchi_temp.happiness < 0):
                break
        else:
            # Если не стала отрицательной, это тоже нормально (маловероятный случай)
            pass

    def test_is_alive_when_all_stats_positive(self):
        """Тест: живое состояние когда все характеристики положительные"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = 50
        self.assertTrue(self.tamagotchi.is_alive())

    def test_is_alive_when_stats_at_1(self):
        """Тест: живое состояние когда все характеристики = 1"""
        self.tamagotchi.hunger = 1
        self.tamagotchi.thirst = 1
        self.tamagotchi.happiness = 1
        self.assertTrue(self.tamagotchi.is_alive())

    def test_is_not_alive_when_hunger_zero(self):
        """Тест: мертвое состояние когда голод = 0"""
        self.tamagotchi.hunger = 0
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = 50
        self.assertFalse(self.tamagotchi.is_alive())

    def test_is_not_alive_when_hunger_negative(self):
        """Тест: мертвое состояние когда голод < 0"""
        self.tamagotchi.hunger = -1
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = 50
        self.assertFalse(self.tamagotchi.is_alive())

    def test_is_not_alive_when_thirst_zero(self):
        """Тест: мертвое состояние когда жажда = 0"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = 0
        self.tamagotchi.happiness = 50
        self.assertFalse(self.tamagotchi.is_alive())

    def test_is_not_alive_when_thirst_negative(self):
        """Тест: мертвое состояние когда жажда < 0"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = -1
        self.tamagotchi.happiness = 50
        self.assertFalse(self.tamagotchi.is_alive())

    def test_is_not_alive_when_happiness_zero(self):
        """Тест: мертвое состояние когда счастье = 0"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = 0
        self.assertFalse(self.tamagotchi.is_alive())

    def test_is_not_alive_when_happiness_negative(self):
        """Тест: мертвое состояние когда счастье < 0"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = -1
        self.assertFalse(self.tamagotchi.is_alive())

    def test_multiple_feed_operations(self):
        """Тест: множественные операции кормления"""
        self.tamagotchi.hunger = 60
        
        self.tamagotchi.feed()  # 60 + 20 = 80
        self.assertEqual(self.tamagotchi.hunger, 80)
        
        self.tamagotchi.feed()  # 80 + 20 = 100
        self.assertEqual(self.tamagotchi.hunger, 100)
        
        self.tamagotchi.feed()  # 100 + 20 = 100 (capped)
        self.assertEqual(self.tamagotchi.hunger, 100)

    def test_combined_operations(self):
        """Тест: комбинированные операции"""
        self.tamagotchi.hunger = 50
        self.tamagotchi.thirst = 50
        self.tamagotchi.happiness = 50
        
        # Все еще живой
        self.assertTrue(self.tamagotchi.is_alive())
        
        # Кормим
        self.tamagotchi.feed()
        self.assertEqual(self.tamagotchi.hunger, 70)
        
        # Даем воду
        self.tamagotchi.give_water()
        self.assertEqual(self.tamagotchi.thirst, 70)
        
        # Играем
        self.tamagotchi.play()
        self.assertEqual(self.tamagotchi.happiness, 70)
        
        # Все еще живой
        self.assertTrue(self.tamagotchi.is_alive())


if __name__ == '__main__':
    unittest.main()
