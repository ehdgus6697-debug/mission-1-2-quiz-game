# Clone / Pull 실습 기록

이 문서는 `mission-1-2-quiz-game`(작업 저장소)과 별도 디렉터리 `mission-1-2-quiz-game-clone`(복제 저장소)을 이용해 `git clone`과 `git pull` 실습을 실제로 수행한 기록이다.

## 1. Clone

작업 저장소가 아닌 별도 디렉터리에서 원격 저장소를 복제했다.

```bash
cd ~/Desktop/codyssey
git clone https://github.com/ehdgus6697-debug/mission-1-2-quiz-game.git mission-1-2-quiz-game-clone
```

clone 실행 사실은 `mission-1-2-quiz-game-clone`의 `git reflog`로도 확인할 수 있다.

```text
5507874 HEAD@{2}: clone: from https://github.com/ehdgus6697-debug/mission-1-2-quiz-game.git
```

복제 직후 `mission-1-2-quiz-game-clone`의 `git log --oneline -1` 결과가 원본 저장소의 최신 커밋과 같음을 확인했다.

## 2. Pull

복제 저장소(`mission-1-2-quiz-game-clone`)에서 README에 변경을 만들어 commit → push하고, 작업 저장소(`mission-1-2-quiz-game`)에서 pull로 반영했다.

```bash
# mission-1-2-quiz-game-clone 에서
echo "clone/pull 실습 확인용 기록: 2026-08-20 18:31" >> README.md
git add -A
git commit -m "Docs: clone/pull 실습 기록 추가"
git push origin main
```

```text
To https://github.com/ehdgus6697-debug/mission-1-2-quiz-game.git
   a9ec762..a8287a9  main -> main
```

```bash
# mission-1-2-quiz-game 에서
git pull origin main
```

```text
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 363 bytes | 181.00 KiB/s, done.
From https://github.com/ehdgus6697-debug/mission-1-2-quiz-game
 * branch            main       -> FETCH_HEAD
   a9ec762..a8287a9  main       -> origin/main
Updating a9ec762..a8287a9
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

실행 결과 캡처:

<img width="1384" height="994" alt="image" src="https://github.com/user-attachments/assets/44d62091-e354-472f-9c8f-30a6a9a730cf" />

pull 이후 `mission-1-2-quiz-game`의 `git log --oneline -1`이 복제 저장소에서 push한 커밋(`a8287a9`)과 같아진 것으로 반영을 확인했다. (실습용으로 추가했던 기록 줄은 이후 README 정리 커밋에서 제거했다.)

## 3. 확인 명령

```bash
git log --oneline -1
git remote -v
git status
```
