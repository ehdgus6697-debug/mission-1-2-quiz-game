"""퀴즈 목록과 진행을 관리하는 QuizGame 클래스와 실행 진입점."""

import json
from pathlib import Path

from quiz import Quiz, create_default_quizzes, quiz_from_dict


class QuizGame:
    """퀴즈 목록, 점수, 메뉴와 저장 흐름을 관리한다."""

    def __init__(self, state_path="state.json"):
        self.state_path = Path(state_path)
        self.quizzes = []
        self.best_score = None
        self.best_correct = None
        self.best_total = None
        self.load_state()

    def _set_defaults(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    def save_state(self):
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

    def load_state(self):
        if not self.state_path.exists():
            self._set_defaults()
            self.save_state()
            return

        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data["quizzes"], list):
                raise ValueError("상태 데이터 형식이 올바르지 않습니다.")
            self.quizzes = [quiz_from_dict(item) for item in data["quizzes"]]
            self.best_score = data.get("best_score")
            self.best_correct = data.get("best_correct")
            self.best_total = data.get("best_total")
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("⚠️ 상태 파일을 읽을 수 없어 기본 데이터로 복구합니다.")
            self._set_defaults()
            self.save_state()

    def read_number(self, prompt, minimum, maximum):
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

    def read_non_empty(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 값은 입력할 수 없습니다.")

    def show_menu(self):
        print("\n" + "=" * 40)
        print("        🎯 Python 기초 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def update_best_score(self, correct, total):
        score = round(correct / total * 100)
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        self.save_state()
        return True

    def play_quizzes(self):
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

    def add_quiz(self):
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

    def list_quizzes(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self):
        if self.best_score is None:
            print("🏆 아직 퀴즈를 풀지 않았습니다.")
            return
        print(
            f"🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )

    def run(self):
        actions = {
            1: self.play_quizzes,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_best_score,
        }
        try:
            while True:
                self.show_menu()
                choice = self.read_number("선택: ", 1, 5)
                if choice == 5:
                    print("👋 현재 상태를 저장하고 안전하게 종료합니다.")
                    return
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되었습니다. 현재 상태를 저장하고 종료합니다.")
        finally:
            self.save_state()


def main():
    state_path = Path(__file__).with_name("state.json")
    QuizGame(state_path).run()


if __name__ == "__main__":
    main()
