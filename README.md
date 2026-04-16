# model_grabber

Small `uv`-based CLI for downloading Hugging Face models into `/data/seth/models`.

## Install

```bash
uv sync
```

## Usage

Download the preset models:

```bash
uv run model-grabber kimi-k2.5 glm-5.1
```

Download a specific Hugging Face repo directly:

```bash
uv run model-grabber Qwen/Qwen3-8B
```

Download to a different directory:

```bash
uv run model-grabber kimi-k2.5 --root /data/seth/other_models
```

Download only selected files:

```bash
uv run model-grabber kimi-k2.5 \
  --allow-pattern "*.json" \
  --allow-pattern "*.safetensors"
```

Ignore selected files:

```bash
uv run model-grabber glm-5.1 \
  --ignore-pattern "*.pt" \
  --ignore-pattern "*.bin"
```

Use a Hugging Face token explicitly:

```bash
uv run model-grabber kimi-k2.5 --token hf_xxx
```

## Notes

Preset names currently supported:

* `kimi-k2.5` -> `moonshotai/Kimi-K2.5`
* `glm-5.1` -> `zai-org/GLM-5.1`
