# Clone / Pull 실습 기록

이 문서는 `mission-1-2-quiz-game`(작업 저장소)과 별도 디렉터리 `mission-1-2-quiz-game-clone`(복제 저장소)을 이용해 `git clone`과 `git pull` 실습을 실제로 수행한 기록이다.

## 1. Clone

작업 저장소가 아닌 별도 디렉터리에서 원격 저장소를 복제했다.

```bash
cd ~/Desktop/codyssey
git clone https://github.com/ehdgus6697-debug/mission-1-2-quiz-game.git mission-1-2-quiz-game-clone
```

<!-- TODO: 실제 실행한 터미널 출력(Cloning into ... 로 시작하는 로그)을 여기에 붙여넣거나 스크린샷을 docs/evidence/ 아래에 추가하고 경로를 링크한다. -->

복제 직후 `mission-1-2-quiz-game-clone`의 `git log --oneline -1` 결과가 원본 저장소의 최신 커밋과 같음을 확인했다.

## 2. Pull

작업 저장소(`mission-1-2-quiz-game`)에서 새 커밋을 만들어 push한 뒤, 복제 저장소(`mission-1-2-quiz-game-clone`)에서 pull로 반영했다.

```bash
# mission-1-2-quiz-game 에서
git push origin main

# mission-1-2-quiz-game-clone 에서
git pull origin main
```

<img width="1384" height="994" alt="image" src="https://github.com/user-attachments/assets/44d62091-e354-472f-9c8f-30a6a9a730cf" />


pull 이후 `mission-1-2-quiz-game-clone`의 `git log --oneline -1`이 작업 저장소의 최신 커밋과 같아진 것으로 반영을 확인했다.

## 3. 확인 명령

```bash
git log --oneline -1
git remote -v
git status
```
