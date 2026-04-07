import json

import requests
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage


load_dotenv()

MODEL = "gpt-4o-mini"
MOVIE_API_BASE_URL = "https://nomad-movies.nomadcoders.workers.dev"
EXIT_COMMANDS = {"q", "quit", "quit", "exit"}

client = OpenAI()
messages = [
    {
        "role": "system",
        "content": (
            "You are a movie recommendation assistant. "
            "Use the movie API tools when the user asks about popular movies, "
            "movie details, cast, or crew. Keep answers concise and useful."
        ),
    }
]


def fetch_json(path: str):
    response = requests.get(f"{MOVIE_API_BASE_URL}{path}", timeout=20)
    response.raise_for_status()
    return response.json()


def get_popular_movies():
    movies = fetch_json("/movies")
    return json.dumps(
        [
            {
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie.get("overview", ""),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
            }
            for movie in movies[:10]
        ],
        ensure_ascii=False,
    )


def get_movie_details(id):
    movie = fetch_json(f"/movies/{id}")
    return json.dumps(
        {
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie.get("overview", ""),
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "runtime": movie.get("runtime"),
            "release_date": movie.get("release_date"),
            "vote_average": movie.get("vote_average"),
        },
        ensure_ascii=False,
    )


def get_movie_credits(id):
    credits = fetch_json(f"/movies/{id}/credits")
    cast = [
        {
            "name": person["name"],
            "character": person.get("character"),
        }
        for person in credits
        if person.get("known_for_department") == "Acting"
    ][:10]
    crew = [
        {
            "name": person["name"],
            "job": person.get("known_for_department"),
        }
        for person in credits
        if person.get("known_for_department") != "Acting"
    ][:10]

    return json.dumps(
        {
            "cast": cast,
            "crew": crew,
        },
        ensure_ascii=False,
    )


FUNCTION_MAP = {
    "get_popular_movies": get_popular_movies,
    "get_movie_details": get_movie_details,
    "get_movie_credits": get_movie_credits,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_popular_movies",
            "description": "Get current popular movies.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_movie_details",
            "description": "Get detailed information for a movie by id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "The movie id.",
                    }
                },
                "required": ["id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_movie_credits",
            "description": "Get cast and crew information for a movie by id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "The movie id.",
                    }
                },
                "required": ["id"],
            },
        },
    },
]


def process_ai_response(message: ChatCompletionMessage):
    if message.tool_calls:
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ],
            }
        )

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"Calling function: {function_name} with {arguments}")

            try:
                parsed_arguments = json.loads(arguments)
            except json.JSONDecodeError:
                parsed_arguments = {}

            function_to_run = FUNCTION_MAP.get(function_name)

            try:
                result = function_to_run(**parsed_arguments)
            except requests.RequestException as exc:
                result = json.dumps(
                    {"error": f"Movie API request failed: {exc}"},
                    ensure_ascii=False,
                )
            except Exception as exc:
                result = json.dumps({"error": str(exc)}, ensure_ascii=False)

            print(
                f"Ran {function_name} with args {parsed_arguments} for a result of {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": result,
                }
            )

        call_ai()
    else:
        messages.append({"role": "assistant", "content": message.content or ""})
        print(f"AI: {message.content}")


def call_ai():
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    )
    process_ai_response(response.choices[0].message)


def main():
    print("Movie Agent를 시작합니다. 종료하려면 q, quit, ㅕquit, exit 를 입력하세요.")

    while True:
        message = input("대화를 입력하세요: ").strip()

        if message.lower() in EXIT_COMMANDS:
            print("대화를 종료합니다.")
            break

        if not message:
            continue

        messages.append({"role": "user", "content": message})
        print(f"User: {message}")
        call_ai()


if __name__ == "__main__":
    main()
