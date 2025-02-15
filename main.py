import argparse
import pathlib
import re
import uuid
from collections.abc import Iterator
from typing import Any, TypedDict

import replicate

from logger import setup_logger

log = setup_logger(__name__)

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
            log.info(f"Saved photo {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="prompt for the photo")
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help="Model to use (default: %(default)s)"
    )
    parser.add_argument(
        "--count",
        default=DEFAULT_COUNT,
        help="Number of photos to generate (default: %(default)s)",
        type=int,
    )
    args = parser.parse_args()

    generated_images = generate_images(args.prompt, args.model, args.count)
    save_images(generated_images, args.prompt)


if __name__ == "__main__":
    main()
