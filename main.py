import pathlib
import re
import uuid
from collections.abc import Iterator
from typing import Any, TypedDict

import replicate

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


def generate_images(prompt: str, model: str, count: int) -> Any:  # pyright: ignore [reportExplicitAny, reportAny]
    """Generates images using the specified model and prompt."""
    input_data = get_input(prompt, model, count)
    return replicate.run(  # pyright: ignore [reportAny]
        "lucataco/flux-dev-lora:091495765fa5ef2725a175a57b276ec30dc9d39c22d30410f2ede68a3eab66b3",
        input=input_data,
    )


def save_images(images: Iterator[Any], prompt: str, output_dir: str = "output") -> None:  # pyright: ignore [reportExplicitAny]
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    prompt_slug = "-".join(prompt.split(" ")[-3:])
    prompt_slug = re.sub(r"[^a-zA-Z0-9\-]", "", prompt_slug).lower()

    for item in images:  # pyright: ignore [reportAny]
        file_id = uuid.uuid4().hex[:5]
        file_path = output_path / f"{prompt_slug}-{file_id}.webp"
        with open(file_path, "wb") as file:
            file.write(item)  # pyright: ignore [reportAny, reportUnusedCallResult]
            print(f"Saved photo {file_path}")


def main() -> None:
    pass


if __name__ == "__main__":
    main()
