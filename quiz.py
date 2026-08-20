"""퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """선택지가 네 개인 객관식 퀴즈 한 문제."""

    def __init__(self, question, choices, answer):
        question = question.strip()
        choices = [str(choice).strip() for choice in choices]
        if not question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(choices) != 4 or any(not choice for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 4개여야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices
        self.answer = answer

    def is_correct(self, choice):
        return choice == self.answer

    def display(self, index):
        print("\n" + "-" * 40)
        print(f"[문제 {index}] {self.question}")
        for choice_number, choice in enumerate(self.choices, start=1):
            print(f"{choice_number}. {choice}")

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


def quiz_from_dict(data):
    """딕셔너리(state.json에서 읽은 데이터)를 Quiz 객체로 만든다."""
    if not isinstance(data, dict):
        raise ValueError("퀴즈 데이터는 객체여야 합니다.")
    try:
        return Quiz(data["question"], data["choices"], data["answer"])
    except (KeyError, TypeError) as error:
        raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.") from error


def create_default_quizzes():
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
