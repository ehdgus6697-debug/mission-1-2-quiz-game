# Python 기초 퀴즈 게임

터미널에서 실행하는 객관식 퀴즈 게임입니다. 퀴즈를 풀고, 새로운 문제를 추가하고, 목록과 최고 점수를 확인할 수 있습니다. 프로그램을 종료해도 `state.json`에 퀴즈와 최고 점수가 남습니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초**입니다. 이 프로젝트에서 사용하는 변수, 자료형, 조건문, 반복문, 함수를 문제로 다시 확인할 수 있고, 입문자가 코드와 퀴즈 내용을 함께 설명하기 쉬워 이 주제를 선택했습니다.

## 실행 환경

- Python 3.10 이상
- 외부 라이브러리 없음

Python 버전을 확인하고 프로그램을 실행합니다.

```bash
python3 --version
python3 quiz_game.py
```

## 기능 목록

1. 저장된 모든 퀴즈 풀기
2. 문제, 선택지 4개, 정답 번호를 입력해 퀴즈 추가
3. 등록된 퀴즈 목록 확인
4. 최고 점수와 당시 정답 수 확인
5. 현재 데이터를 저장하고 종료

빈 입력, 숫자가 아닌 입력, 범위 밖 숫자는 안내 후 다시 입력받습니다. `Ctrl+C` 또는 입력 스트림 종료가 발생해도 가능한 데이터를 저장하고 종료합니다. `state.json`이 없으면 기본 퀴즈를 만들고, 파일이 손상되면 기본 데이터로 복구합니다.

## 파일 구조

```text
mission-1-2-quiz-game/
├── quiz_game.py          # Quiz, QuizGame 클래스와 실행 진입점
├── state.json            # 퀴즈 목록과 최고 점수
├── tests/
│   └── test_quiz_game.py # 표준 라이브러리 unittest 테스트
├── docs/
│   ├── evidence/         # 실행 및 Git 검증 기록
│   └── superpowers/      # 설계와 구현 계획
├── .gitignore
└── README.md
```

## 데이터 파일

`state.json`은 프로젝트 루트에 있으며 UTF-8 JSON 형식을 사용합니다.

```json
{
  "quizzes": [
    {
      "question": "문제 내용",
      "choices": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"],
      "answer": 1
    }
  ],
  "best_score": 80,
  "best_correct": 4,
  "best_total": 5
}
```

- `quizzes`: 퀴즈 객체 목록
- `best_score`: 100점 기준 최고 점수
- `best_correct`: 최고 점수를 기록했을 때 맞힌 문제 수
- `best_total`: 최고 점수를 기록했을 때 전체 문제 수

아직 퀴즈를 풀지 않은 경우 점수 관련 값은 `null`입니다.

## 테스트

외부 도구 없이 전체 테스트를 실행할 수 있습니다.

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile quiz_game.py
python3 -m json.tool state.json
```

## 클래스 설명

- `Quiz`: 문제, 선택지, 정답을 보관하고 문제 출력과 정답 판정을 담당합니다.
- `QuizGame`: 메뉴, 입력 검증, 게임 진행, 퀴즈 추가·목록, 점수, JSON 저장·불러오기를 관리합니다.

`__init__`은 객체가 만들어질 때 필요한 속성을 준비합니다. `self`는 지금 사용 중인 객체 자신을 가리킵니다. 기능을 메서드로 나누었기 때문에 각 부분을 따로 읽고 테스트할 수 있습니다.

## Git 확인

커밋과 브랜치 병합 기록은 다음 명령으로 확인합니다.

```bash
git log --oneline --graph --all
```

원격 저장소 복제와 pull 실습은 GitHub 저장소를 만든 뒤 별도 디렉터리에서 진행합니다.
