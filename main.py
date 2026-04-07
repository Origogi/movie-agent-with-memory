from __future__ import annotations

import os

from openai import OpenAI
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4o-mini",
        input="안녕 내이름은 link 야",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
