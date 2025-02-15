# Flux Dev Lora Runner

A little script to run the [Flux Dev Lora](https://replicate.com/lucataco/flux-dev-lora) model on Replicate.

## Usage

```python
uv run main.py "a photorealistic portrait of maxshapira as Superman, standing tall, wearing the classic Superman suit, with a determined expression, against a backdrop of a futuristic city." \
--model="xshapira/me-v1" \
--count=4
```

Additional arguments:

- **model:** The hugging face model to use (repo id)
- **count:** The number of photos to generate (1-4, defaults to 1)
