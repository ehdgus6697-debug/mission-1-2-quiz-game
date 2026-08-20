"""Python 기초 퀴즈 게임."""

from dataclasses import dataclass


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
