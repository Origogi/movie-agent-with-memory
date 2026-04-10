# Movie Agent

간단한 영화 추천 에이전트입니다. `openai-agents` SDK를 사용하며, 대화 기록을 SQLite에 저장하여 세션을 유지합니다.

## 실행 방법

이 프로젝트는 주피터 노트북(`main.ipynb`)에서 실행하는 것을 권장합니다.

1.  의존성 설치 (`uv` 사용 시):
    ```bash
    uv sync
    ```
2.  `.env` 파일에 `OPENAI_API_KEY` 설정
3.  `main.ipynb` 파일을 열고 셀을 순서대로 실행합니다.

## 기능

- **세션 유지**: `SQLiteSession`을 사용하여 대화 기록을 `chat_history.db`에 저장하고, 에이전트 재시작 시에도 이전 대화 내용을 기억합니다.
- **영화 정보 조회**: 현재 인기 영화, 상세 정보, 출연진 정보를 API를 통해 조회하여 추천합니다.

## APIs

- OpenAI API: 에이전트 응답 생성 (`openai-agents` SDK 사용)
- Movie API: [Nomad Movies API](https://nomad-movies.nomadcoders.workers.dev)

확인된 영화 API 엔드포인트:
- `/movies` (인기 영화 목록)
- `/movies/:id` (영화 상세 정보)
- `/movies/:id/credits` (출연진 및 제작진)
