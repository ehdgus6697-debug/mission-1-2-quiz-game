import unittest

from quiz_game import Quiz


class QuizTests(unittest.TestCase):
    def test_answer_and_dictionary_round_trip(self):
        quiz = Quiz("list의 의미는?", ["숫자", "문자", "여러 값", "조건"], 3)

        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()), quiz)

    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2"], 1)


if __name__ == "__main__":
    unittest.main()
