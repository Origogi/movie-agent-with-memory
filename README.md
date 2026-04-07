# Movie Agent

간단한 영화 추천 에이전트입니다.

## Run

```bash
uv run python main.py
```

## APIs

- OpenAI API: 에이전트 응답 생성
- Movie API: https://nomad-movies.nomadcoders.workers.dev

확인된 영화 API 엔드포인트:

- `/movies`
- `/movies/:id`
- `/movies/:id/credits`
- `/movies/:id/videos`
- `/movies/:id/providers`
- `/movies/:id/similar`
