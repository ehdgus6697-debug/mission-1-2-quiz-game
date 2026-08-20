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

    def display(self, index: int) -> None:
        print("\n" + "-" * 40)
        print(f"[문제 {index}] {self.question}")
        for choice_number, choice in enumerate(self.choices, start=1):
            print(f"{choice_number}. {choice}")

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

    def read_non_empty(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 값은 입력할 수 없습니다.")

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

    def update_best_score(self, correct: int, total: int) -> bool:
        score = round(correct / total * 100)
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        self.save_state()
        return True

    def play_quizzes(self) -> None:
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0
        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            choice = self.read_number("정답 입력: ", 1, 4)
            if quiz.is_correct(choice):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        total = len(self.quizzes)
        score = round(correct_count / total * 100)
        is_new_best = self.update_best_score(correct_count, total)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self) -> None:
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_non_empty("문제를 입력하세요: ")
        choices = [
            self.read_non_empty(f"선택지 {number}: ")
            for number in range(1, 5)
        ]
        answer = self.read_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)
