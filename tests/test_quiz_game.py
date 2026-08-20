import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from quiz_game import Quiz, QuizGame, create_default_quizzes


class QuizTests(unittest.TestCase):
    def test_answer_and_dictionary_round_trip(self):
        quiz = Quiz("list의 의미는?", ["숫자", "문자", "여러 값", "조건"], 3)

        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()), quiz)

    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2"], 1)


class DefaultQuizTests(unittest.TestCase):
    def test_default_quizzes_have_required_shape(self):
        quizzes = create_default_quizzes()

        self.assertGreaterEqual(len(quizzes), 5)
        self.assertTrue(all(len(quiz.choices) == 4 for quiz in quizzes))
        self.assertTrue(all(1 <= quiz.answer <= 4 for quiz in quizzes))


class PersistenceTests(unittest.TestCase):
    def test_save_and_reload(self):
        with TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            game = QuizGame(state_path)
            game.best_score = 80
            game.best_correct = 4
            game.best_total = 5

            self.assertTrue(game.save_state())
            loaded = QuizGame(state_path)

            self.assertEqual(len(loaded.quizzes), 5)
            self.assertEqual(loaded.best_score, 80)
            self.assertEqual(loaded.best_correct, 4)
            self.assertEqual(loaded.best_total, 5)

    def test_corrupt_file_recovers_defaults(self):
        with TemporaryDirectory() as directory:
            state_path = Path(directory) / "state.json"
            state_path.write_text("{broken", encoding="utf-8")

            game = QuizGame(state_path)

            self.assertEqual(len(game.quizzes), 5)
            self.assertIsNone(game.best_score)
            reloaded = QuizGame(state_path)
            self.assertEqual(len(reloaded.quizzes), 5)


class InputTests(unittest.TestCase):
    def test_read_number_retries_invalid_values(self):
        with TemporaryDirectory() as directory:
            game = QuizGame(Path(directory) / "state.json")
            output = StringIO()
            with patch("builtins.input", side_effect=["", "abc", "9", " 2 "]):
                with redirect_stdout(output):
                    result = game.read_number("선택: ", 1, 5)

            self.assertEqual(result, 2)
            self.assertEqual(output.getvalue().count("⚠️"), 3)

    def test_show_menu_contains_only_required_choices(self):
        with TemporaryDirectory() as directory:
            game = QuizGame(Path(directory) / "state.json")
            output = StringIO()
            with redirect_stdout(output):
                game.show_menu()

            text = output.getvalue()
            self.assertIn("1. 퀴즈 풀기", text)
            self.assertIn("5. 종료", text)
            self.assertNotIn("힌트", text)


if __name__ == "__main__":
    unittest.main()
