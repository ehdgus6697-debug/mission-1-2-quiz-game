"""Python 기초 퀴즈 게임."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Quiz:
    """선택지가 네 개인 객관식 퀴즈 한 문제."""

    question: str
    choices: list[str]
    answer: int

    def __post_init__(self) -> None:
        self.question = self.question.strip()
        self.choices = [str(choice).strip() for choice in self.choices]
        if not self.question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(self.choices) != 4 or any(not choice for choice in self.choices):
            raise ValueError("선택지는 비어 있지 않은 4개여야 합니다.")
        if not isinstance(self.answer, int) or not 1 <= self.answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 정수여야 합니다.")

    def is_correct(self, choice: int) -> bool:
        return choice == self.answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 객체여야 합니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except (KeyError, TypeError) as error:
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.") from error


def create_default_quizzes() -> list[Quiz]:
    """처음 실행할 때 사용할 Python 기초 퀴즈를 반환한다."""
    return [
        Quiz(
            "Python에서 값을 저장할 때 사용하는 이름은 무엇인가요?",
            ["변수", "반복문", "조건문", "주석"],
            1,
        ),
        Quiz(
            "여러 값을 순서대로 저장하는 자료형은 무엇인가요?",
            ["bool", "int", "list", "str"],
            3,
        ),
        Quiz(
            "조건에 따라 다른 코드를 실행할 때 사용하는 문법은 무엇인가요?",
            ["import", "if", "def", "class"],
            2,
        ),
        Quiz(
            "정해진 횟수만큼 반복할 때 주로 사용하는 문법은 무엇인가요?",
            ["try", "return", "for", "with"],
            3,
        ),
        Quiz(
            "함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            ["def", "while", "elif", "print"],
            1,
        ),
    ]


class QuizGame:
    """퀴즈 목록, 점수, 메뉴와 저장 흐름을 관리한다."""

    def __init__(self, state_path: str | Path = "state.json") -> None:
        self.state_path = Path(state_path)
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.best_correct: int | None = None
        self.best_total: int | None = None
        self.load_state()

    def _set_defaults(self) -> None:
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    def save_state(self) -> bool:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            self.state_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError:
            print("⚠️ 상태 파일을 저장하지 못했습니다.")
            return False
        return True

    def load_state(self) -> None:
        if not self.state_path.exists():
            self._set_defaults()
            self.save_state()
            return

        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data["quizzes"], list):
                raise ValueError("상태 데이터 형식이 올바르지 않습니다.")
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = data.get("best_score")
            self.best_correct = data.get("best_correct")
            self.best_total = data.get("best_total")
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("⚠️ 상태 파일을 읽을 수 없어 기본 데이터로 복구합니다.")
            self._set_defaults()
            self.save_state()

    def read_number(self, prompt: str, minimum: int, maximum: int) -> int:
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("⚠️ 값을 입력해 주세요.")
                continue
            try:
                value = int(raw_value)
            except ValueError:
                print("⚠️ 숫자를 입력해 주세요.")
                continue
            if not minimum <= value <= maximum:
                print(f"⚠️ {minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")
                continue
            return value

    def show_menu(self) -> None:
        print("\n" + "=" * 40)
        print("        🎯 Python 기초 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)
