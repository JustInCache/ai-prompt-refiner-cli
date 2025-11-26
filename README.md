# AI Prompt Refiner CLI

Turn scrappy ideas into production-ready prompts without ever leaving the terminal.

## Why it exists

Prompting is still a superpower, but crafting great prompts takes time. **AI Prompt Refiner CLI** transforms a single rough idea into five ready-to-use variants in seconds:

- Polished improved prompt
- Power prompt with deep structure
- Short <20 word prompt
- Long narrative-style prompt
- Creative twist prompt

All powered by an abstract provider system (defaults to OpenAI GPT-4o mini), wrapped in a fast, colorful CLI.

## Install

```bash
pip install promptrefiner
```

Or work locally:

```bash
git clone https://github.com/oss/prompt-refiner-cli.git
cd prompt-refiner-cli
pip install -e .
```

## Usage

Basic command:

```bash
promptref refine "Help me explain quantum computing to kids"
```

Flagged variants:

```bash
promptref refine "Plan a Mars mission" --short --creative
```

Pipe from any tool:

```bash
cat idea.txt | promptref refine
```

Interactive mode (no args, no stdin):

```bash
promptref refine
```

### ASCII Screenshot

```
+-----------------------------------------------------------+
| promptref refine "Design a community art festival"        |
+-----------------------------------------------------------+
| ORIGINAL: Design a community art festival                 |
|                                                           |
| Variant        | Prompt                                   |
| -------------- | ---------------------------------------- |
| Improved       | Curate a vibrant neighborhood art...     |
| Power          | You are an event architect...            |
| Short          | Design an immersive community art fest   |
| Long           | Imagine a summer weekend...              |
| Creative Twist | Surprise residents with...               |
+-----------------------------------------------------------+
```

## Example Output

See `example_output.md` for a full run with every variant rendered.

## Environment & Providers

1. Set your OpenAI key:
   ```bash
   export OPENAI_API_KEY="sk-live..."
   ```
2. Run the CLI. Missing keys produce a helpful error.

### Custom Providers

Providers live in `promptrefiner/providers/`.

```python
from promptrefiner.providers.base import BaseProvider

class MyProvider(BaseProvider):
    name = "my-provider"

    def generate(self, prompt: str) -> dict[str, str]:
        # Hit your favorite API
        return {
            "improved": "...",
            "power": "...",
            "short": "...",
            "long": "...",
            "creative": "...",
        }
```

Then register it in `promptrefiner.cli.get_provider`.

## Logging & Debug

Use `--debug` to see API payloads and internal state transitions:

```bash
promptref refine "Frame a VC pitch" --debug
```

## Development

```bash
git clone https://github.com/oss/prompt-refiner-cli.git
cd prompt-refiner-cli
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Contributing

1. Fork the repo
2. Create a feature branch
3. Add/adjust tests
4. Submit a PR with context and screenshots

We love docs and creative prompt presets—send them!

## Support the Project

If this repo saved you time or sparked an idea, consider buying me a coffee to keep the prompts flowing. ❤️ 

[https://buymeacoffee.com/connectankush](https://buymeacoffee.com/connectankush)

Your support and feedback are valuable in maintaining and improving the extension.

![Buy Me a Coffee](img/bmc.png)
![Buy Me a Coffee QR](img/bmc-qr-code.png)



## License

MIT © Prompt Refiner contributors
