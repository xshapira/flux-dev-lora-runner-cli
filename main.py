from typing import TypedDict

DEFAULT_MODEL = "xshapira/me-v1"
DEFAULT_COUNT = 1


class ModelDict(TypedDict):
    prompt: str
    hr_lora: str
    num_outputs: int


def get_input(
    prompt: str, model: str = DEFAULT_MODEL, count: int = DEFAULT_COUNT
) -> ModelDict:
    return {
        "prompt": prompt,
        "hr_lora": model,
        "num_outputs": count,
    }


def main() -> None:
    pass


if __name__ == "__main__":
    main()
