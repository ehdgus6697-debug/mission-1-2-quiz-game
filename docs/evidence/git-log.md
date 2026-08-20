# 커밋 수 및 병합 기록

검증일: 2026-08-20

## 커밋 수

```bash
$ git rev-list --count main
31
```

## 병합 기록 포함 전체 로그

```bash
$ git log --oneline --graph --all
* 2e93155 Refactor: Quiz와 QuizGame 클래스를 quiz.py, quiz_game.py 두 파일로 분리
* 4f49b6e Style: classmethod와 던더 메서드를 일반 함수로 단순화
* da5284a Docs: 평가 피드백 반영 (커밋/병합 증거, JSON 선정 이유, 확장성·백업 전략 보완)
* c6c78e7 Style: 타입 힌트 제거, 순수 Python 기초 문법으로 정리
* 7951195 Refactor: Quiz 클래스를 dataclass 없이 __init__으로 재작성
* b5d6cd5 Docs: 프로젝트 개요, 실행 화면 스크린샷, clone/pull 증거 정리
* c4d39cd Update clone-pull.md with pull confirmation
* a8287a9 Docs: clone/pull 실습 기록 추가
* a9ec762 Docs: README 정리 및 clone/pull 증거 정리
*   756ac77 Merge: 퀴즈 추가 입력 검증 테스트 통합
|\
| * ba5799d Test: 퀴즈 추가 입력 예외 검증 보강
|/
*   5507874 Merge: Python 퀴즈 게임 구현 통합
|\
| * a286257 Test: 필수 기능 실행 증거 추가
| * e0ea247 Docs: 실행 방법과 데이터 구조 문서화
| * 7fe3c98 Data: 기본 상태 파일 추가
| * 256bce5 Feat: 전체 메뉴 흐름과 안전 종료 연결
| * 70fdcd5 Feat: 최고 점수 확인 기능 구현
| * 5f9c3f2 Feat: 저장된 퀴즈 목록 출력 구현
| * 84814e8 Feat: 사용자 퀴즈 추가와 즉시 저장 구현
| *   816ae1a Merge: 퀴즈 풀기 기능 통합
| |\
| | * aaf66e1 Feat: 퀴즈 출제와 결과 출력 구현
| | * a89c4e8 Feat: 최고 점수 계산과 갱신 구현
| |/
| * 550e161 Feat: 메뉴와 공통 숫자 입력 검증 구현
| * 65461eb Fix: 손상된 상태 파일을 기본 데이터로 복구
| * e66655b Feat: JSON 상태 저장과 불러오기 구현
| * a594723 Data: Python 기초 퀴즈 5개 추가
| * c700844 Feat: Quiz 클래스와 정답 판정 구현
| * b796cd2 Chore: 테스트 패키지 기본 구조 추가
|/
* 3bbe4ab Chore: Python 및 worktree 제외 설정
* e5c0707 Docs: Python 퀴즈 게임 구현 계획 작성
* 61bbe53 Docs: Python 퀴즈 게임 설계 작성
```

병합 커밋은 `756ac77`, `5507874`, `816ae1a` 세 곳에서 확인할 수 있으며, 각각 별도 브랜치(`docs/peer-review-alignment`, `implement/quiz-game`, `feature/play-quiz` 계열)에서 작업한 내용을 `main`에 합친 기록이다.
