# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "replicate",
#     "tqdm",
# ]
# ///
import argparse
import pathlib
import re
import uuid
from collections.abc import Iterator
from typing import Any, TypedDict

from replicate.client import Client
from tqdm import tqdm

from config import config
from logger import setup_logger

log = setup_logger(__name__)

DEFAULT_MODEL = "xshapira/me-v1"
DEFAULT_COUNT = 1
REPLICATE_API_TOKEN = config["replicate_api_token"]


class ModelDict(TypedDict):
    prompt: str
    hf_lora: str
    num_outputs: int


def get_input(
    prompt: str, model: str = DEFAULT_MODEL, count: int = DEFAULT_COUNT
) -> ModelDict:
    return {
        "prompt": prompt,
        "hf_lora": model,
        "num_outputs": count,
    }


def generate_images(prompt: str, model: str, count: int) -> Any:  # pyright: ignore [reportExplicitAny, reportAny]
    """Generates images using the specified model and prompt."""
    input_data = get_input(prompt, model, count)
    replicate = Client(api_token=REPLICATE_API_TOKEN)
    with tqdm(
        total=count, desc="Generating images", unit="image", colour="#4ABDA6"
    ) as pbar:
        for image in replicate.run(  # pyright: ignore [reportAny]
            "lucataco/flux-dev-lora:091495765fa5ef2725a175a57b276ec30dc9d39c22d30410f2ede68a3eab66b3",
            input=input_data,
        ):
            yield image
            pbar.update(1)


def save_images(images: Iterator[Any], prompt: str, output_dir: str = "output") -> None:  # pyright: ignore [reportExplicitAny]
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    prompt_slug = "-".join(prompt.split(" ")[-3:])
    prompt_slug = re.sub(r"[^a-zA-Z0-9\-]", "", prompt_slug).lower()

    for item in images:  # pyright: ignore [reportAny]
        file_id = uuid.uuid4().hex[:5]
        file_path = output_path / f"{prompt_slug}-{file_id}.webp"
        with open(file_path, "wb") as file:
            image_data = item.read()
            file.write(image_data)  # pyright: ignore [reportAny, reportUnusedCallResult]
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
