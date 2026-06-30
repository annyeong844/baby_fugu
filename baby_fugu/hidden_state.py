from __future__ import annotations

from typing import Iterable


def extract_last_token_hidden_states(
    texts: Iterable[str],
    *,
    model_id: str = "Qwen/Qwen3-0.6B",
    device: str = "cpu",
    layer_index: int = -2,
) -> list[list[float]]:
    """Extract local hidden states.

    This function is intentionally optional. Importing this module does not import
    torch or transformers, so CI can run without downloading models.
    """

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        output_hidden_states=True,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    ).to(device)
    model.eval()

    vectors: list[list[float]] = []
    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(text, return_tensors="pt").to(device)
            outputs = model(**inputs, output_hidden_states=True)
            hidden = outputs.hidden_states[layer_index][0, -1, :].detach().cpu().float()
            vectors.append([float(value) for value in hidden.tolist()])
    return vectors
