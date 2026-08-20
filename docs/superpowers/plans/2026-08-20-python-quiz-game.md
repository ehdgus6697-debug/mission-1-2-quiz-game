# Python Quiz Game Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Python 기초 객관식 문제를 풀고 추가하며 최고 점수를 JSON 파일에 유지하는 콘솔 퀴즈 게임을 완성한다.

**Architecture:** `quiz_game.py`에 데이터 객체 `Quiz`와 프로그램 흐름을 담당하는 `QuizGame`을 둔다. 모든 영속 데이터는 주입 가능한 `state_path`를 통해 JSON으로 저장하고, 테스트는 임시 디렉터리를 사용해 실제 파일 동작과 콘솔 입력 흐름을 검증한다.

**Tech Stack:** Python 3.10+, 표준 라이브러리 `json`, `pathlib`, `unittest`, `tempfile`, `unittest.mock`

**Spec:** `docs/superpowers/specs/2026-08-20-python-quiz-game-design.md`

## Global Constraints

- Python 3.10 이상만 지원한다.
- 외부 라이브러리를 사용하지 않는다.
- 실행 코드는 `quiz_game.py`, 데이터는 프로젝트 루트의 UTF-8 `state.json`에 둔다.
- `Quiz`와 `QuizGame` 두 클래스를 정의하고 기능별 메서드를 분리한다.
- 보너스 기능은 구현하지 않는다.
- 실패하는 테스트를 확인한 뒤 최소 구현을 추가한다.

---

### Task 1: Quiz 데이터 객체

**Files:**
- Create: `.gitignore`
- Create: `tests/__init__.py`
- Create: `tests/test_quiz_game.py`
- Create: `quiz_game.py`

**Interfaces:**
- Produces: `Quiz(question: str, choices: list[str], answer: int)`, `Quiz.is_correct(choice: int) -> bool`, `Quiz.to_dict() -> dict`, `Quiz.from_dict(data: dict) -> Quiz`

- [ ] **Step 1: 프로젝트 기본 파일을 만들고 커밋**

`.gitignore`에는 `__pycache__/`, `*.pyc`, `.DS_Store`를 기록하고 빈 `tests/__init__.py`를 만든다.

Run: `git add .gitignore tests/__init__.py && git commit -m "Chore: Python 프로젝트 기본 파일 추가"`

- [ ] **Step 2: 실패하는 Quiz 테스트 작성**

```python
class QuizTests(unittest.TestCase):
    def test_answer_and_dictionary_round_trip(self):
        quiz = Quiz("list의 의미는?", ["숫자", "문자", "여러 값", "조건"], 3)
        self.assertTrue(quiz.is_correct(3))
        self.assertFalse(quiz.is_correct(1))
        self.assertEqual(Quiz.from_dict(quiz.to_dict()), quiz)

    def test_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2"], 1)
```

- [ ] **Step 3: RED 확인**

Run: `python3 -m unittest tests.test_quiz_game.QuizTests -v`
Expected: FAIL 또는 ERROR (`Quiz`를 가져올 수 없음)

- [ ] **Step 4: 최소 구현**

`Quiz`를 `@dataclass`로 만들고 `__post_init__`에서 빈 문제, 선택지 4개 여부, 빈 선택지, 1~4 정답을 검증한다. `to_dict`와 `from_dict`는 `question`, `choices`, `answer` 키를 일관되게 사용한다.

- [ ] **Step 5: GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.QuizTests -v`
Expected: 2 tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: Quiz 클래스와 정답 판정 구현"`

### Task 2: Python 기초 기본 퀴즈

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `create_default_quizzes() -> list[Quiz]`

- [ ] **Step 1: 실패하는 데이터 테스트 작성**

```python
def test_default_quizzes_have_required_shape(self):
    quizzes = create_default_quizzes()
    self.assertGreaterEqual(len(quizzes), 5)
    self.assertTrue(all(len(quiz.choices) == 4 for quiz in quizzes))
```

- [ ] **Step 2: RED 확인**

Run: `python3 -m unittest tests.test_quiz_game.DefaultQuizTests -v`
Expected: ERROR (`create_default_quizzes`를 가져올 수 없음)

- [ ] **Step 3: 최소 구현**

변수, 자료형, 조건문, 반복문, 함수에 관한 직접 작성 문제 5개를 `Quiz` 객체로 반환한다.

- [ ] **Step 4: GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.DefaultQuizTests -v`
Expected: 1 test OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Data: Python 기초 퀴즈 5개 추가"`

### Task 3: 상태 파일 저장과 복구

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `QuizGame(state_path: str | Path = "state.json")`, `QuizGame.save_state() -> bool`, `QuizGame.load_state() -> None`
- State: `quizzes`, `best_score`, `best_correct`, `best_total`

- [ ] **Step 1: 정상 저장·재로딩 실패 테스트 작성**

임시 경로로 게임을 생성하고 퀴즈 및 `80, 4, 5` 점수를 저장한 다음 새 객체가 같은 값을 읽는지 확인한다.

- [ ] **Step 2: RED 확인**

Run: `python3 -m unittest tests.test_quiz_game.PersistenceTests.test_save_and_reload -v`
Expected: ERROR (`QuizGame`을 가져올 수 없음)

- [ ] **Step 3: 정상 저장·불러오기 구현**

UTF-8과 `ensure_ascii=False`, `indent=2`로 최소 스키마를 저장한다. 파일이 없으면 기본 퀴즈를 설정하고 바로 저장한다.

- [ ] **Step 4: GREEN 확인과 첫 커밋**

Run: `python3 -m unittest tests.test_quiz_game.PersistenceTests.test_save_and_reload -v`
Expected: 1 test OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: JSON 상태 저장과 불러오기 구현"`

- [ ] **Step 5: 손상 파일 복구 실패 테스트 작성**

`{broken`을 파일에 쓴 뒤 `QuizGame`이 5개 기본 문제와 빈 점수를 갖고 유효한 JSON으로 파일을 복구하는지 확인한다.

- [ ] **Step 6: RED 확인, 복구 구현, GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.PersistenceTests.test_corrupt_file_recovers_defaults -v`
Expected before implementation: FAIL

`JSONDecodeError`, `OSError`, `KeyError`, `TypeError`, `ValueError`를 잡아 기본 상태로 복구한다. 읽기 오류는 메모리 복구 후 저장을 시도한다.

Run: `python3 -m unittest tests.test_quiz_game.PersistenceTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Fix: 손상된 상태 파일을 기본 데이터로 복구"`

### Task 4: 공통 숫자 입력과 메뉴

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `QuizGame.read_number(prompt: str, minimum: int, maximum: int) -> int`, `QuizGame.show_menu() -> None`

- [ ] **Step 1: 입력 재시도 실패 테스트 작성**

`input`을 `"", "abc", "9", " 2 "` 순서로 반환하게 하고 `read_number(..., 1, 5)`가 2를 반환하며 세 번의 오류 안내를 출력하는지 검사한다.

- [ ] **Step 2: RED 확인**

Run: `python3 -m unittest tests.test_quiz_game.InputTests -v`
Expected: ERROR (`read_number` 없음)

- [ ] **Step 3: 최소 구현과 메뉴 출력 구현**

공백 제거 후 빈 값, 변환 실패, 범위 오류를 각각 안내하고 반복한다. 메뉴에는 필수 기능 1~5만 출력한다.

- [ ] **Step 4: GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.InputTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 메뉴와 공통 숫자 입력 검증 구현"`

### Task 5: 퀴즈 풀기와 최고 점수

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `Quiz.display(index: int) -> None`, `QuizGame.update_best_score(correct: int, total: int) -> bool`, `QuizGame.play_quizzes() -> None`

- [ ] **Step 1: 브랜치 생성**

Run: `git checkout -b feature/play-quiz`
Expected: 새 브랜치로 이동

- [ ] **Step 2: 점수 정책 실패 테스트 작성**

최초 3/5가 60점으로 저장되고 4/5가 갱신되며 이후 4/5 동점과 2/5 하락은 기존 기록을 유지하는지 검사한다.

- [ ] **Step 3: RED 확인, 점수 구현, GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.ScoreTests -v`
Expected before implementation: ERROR (`update_best_score` 없음)

점수는 `round(correct / total * 100)`으로 계산하고 기존 점수보다 클 때만 저장한다.

Run: `python3 -m unittest tests.test_quiz_game.ScoreTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 최고 점수 계산과 갱신 구현"`

- [ ] **Step 4: 플레이 흐름 실패 테스트 작성**

두 문제와 입력 `1`, `2`를 사용해 정답/오답 메시지, 결과 `1/2`, 50점을 확인한다. 빈 목록에서는 안내 후 즉시 반환하는 테스트도 작성한다.

- [ ] **Step 5: RED 확인, 구현, GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.PlayTests -v`
Expected before implementation: FAIL

각 `Quiz.display` 뒤에 1~4 입력을 받고 결과를 누적한 후 점수와 새 기록 여부를 출력한다.

Run: `python3 -m unittest tests.test_quiz_game.PlayTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 퀴즈 출제와 결과 출력 구현"`

- [ ] **Step 6: main에 병합**

Run: `git checkout main && git merge --no-ff feature/play-quiz -m "Merge: 퀴즈 풀기 기능 통합"`
Expected: 병합 커밋 생성

### Task 6: 퀴즈 추가와 목록

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `QuizGame.read_non_empty(prompt: str) -> str`, `QuizGame.add_quiz() -> None`, `QuizGame.list_quizzes() -> None`

- [ ] **Step 1: 추가 흐름 실패 테스트 작성**

빈 문제 뒤 정상 문제, 선택지 4개, 정답 2를 입력해 퀴즈가 한 개 늘고 재로딩해도 유지되는지 확인한다.

- [ ] **Step 2: RED 확인, 구현, GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.AddQuizTests -v`
Expected before implementation: ERROR 또는 FAIL

`read_non_empty`로 빈 문자열을 재요청하고 추가 직후 `save_state`를 호출한다.

Run: `python3 -m unittest tests.test_quiz_game.AddQuizTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 사용자 퀴즈 추가와 즉시 저장 구현"`

- [ ] **Step 3: 목록 실패 테스트 작성, 구현, 검증 및 커밋**

문제가 있을 때 번호와 문제 텍스트를 출력하고 빈 목록에서는 안내하는 두 테스트를 작성한다.

Run before implementation: `python3 -m unittest tests.test_quiz_game.ListQuizTests -v`
Expected: FAIL

Run after implementation: `python3 -m unittest tests.test_quiz_game.ListQuizTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 저장된 퀴즈 목록 출력 구현"`

### Task 7: 점수 표시와 안전한 프로그램 실행

**Files:**
- Modify: `quiz_game.py`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Produces: `QuizGame.show_best_score() -> None`, `QuizGame.run() -> None`, `main() -> None`

- [ ] **Step 1: 점수 표시 테스트 작성, RED, 구현, GREEN 및 커밋**

기록이 없을 때 안내하고 `80, 4, 5`일 때 `80점`과 `5문제 중 4문제`를 출력하는지 검사한다.

Run: `python3 -m unittest tests.test_quiz_game.ShowScoreTests -v`
Expected before implementation: FAIL; after implementation: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 최고 점수 확인 기능 구현"`

- [ ] **Step 2: 메뉴 연결과 안전 종료 테스트 작성**

선택 5가 저장 후 종료되는지, `KeyboardInterrupt`와 `EOFError`도 안내·저장 후 반환하는지 mock으로 검사한다.

- [ ] **Step 3: RED 확인, 구현, GREEN 확인 및 커밋**

Run: `python3 -m unittest tests.test_quiz_game.RunTests -v`
Expected before implementation: FAIL

`run`에서 1~5를 각 메서드에 연결하고 입력 중단 예외를 바깥에서 잡아 `finally`에서 저장한다. `main`은 프로젝트 루트의 `state.json`으로 게임을 생성한다.

Run: `python3 -m unittest tests.test_quiz_game.RunTests -v`
Expected: all tests OK

Run: `git add quiz_game.py tests/test_quiz_game.py && git commit -m "Feat: 전체 메뉴 흐름과 안전 종료 연결"`

### Task 8: 데이터 파일, README, 최종 검증

**Files:**
- Create: `state.json`
- Create: `README.md`
- Modify: `tests/test_quiz_game.py`

**Interfaces:**
- Consumes: 완성된 `Quiz`, `QuizGame`, `main`

- [ ] **Step 1: 기본 state.json 생성과 검증**

Run: `python3 -c 'from pathlib import Path; from quiz_game import QuizGame; QuizGame(Path("state.json"))'`
Expected: UTF-8 JSON 파일과 기본 퀴즈 5개 생성

Run: `python3 -m json.tool state.json`
Expected: 유효한 JSON 출력

Run: `git add state.json && git commit -m "Data: 기본 상태 파일 추가"`

- [ ] **Step 2: README 작성과 커밋**

프로젝트 개요, Python 기초 주제 선정 이유, `python3 quiz_game.py` 실행 방법, 기능 목록, 파일 구조, `state.json` 경로·역할·스키마, 테스트 명령, Git 실습 설명을 작성한다.

Run: `git add README.md && git commit -m "Docs: 실행 방법과 데이터 구조 문서화"`

- [ ] **Step 3: 전체 자동 검증**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests OK

Run: `python3 -m py_compile quiz_game.py`
Expected: exit 0

Run: `git log --oneline --graph --all`
Expected: 의미 있는 커밋 10개 이상과 `feature/play-quiz` 병합 기록

- [ ] **Step 4: 콘솔 시나리오 검증과 증거 생성**

목록 → 퀴즈 풀기 → 점수 → 퀴즈 추가 → 종료 → 재시작 → 추가 퀴즈 유지 순서를 입력 파일로 실행하고 결과를 `docs/evidence/console-demo.txt`에 저장한다. 빈 입력, `abc`, 범위 밖 숫자도 별도 입력으로 검증한다.

Run: `git add docs/evidence && git commit -m "Test: 필수 기능 실행 증거 추가"`

- [ ] **Step 5: GitHub 게시와 clone/pull 실습**

사용자에게 저장소 공개 범위와 GitHub 계정을 확인한 후 `gh repo create`와 push를 수행한다. 별도 임시 디렉터리에 clone하고 README에 실습 문장을 추가해 commit·push한 뒤 원본에서 pull한다. 원격 쓰기 전에 사용자 승인을 받고, 결과 URL과 증거를 README 또는 `docs/evidence`에 정리한다.
