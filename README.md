# VAD-Bench

A controlled benchmark for evaluating task success and least-privilege authorization in GUI agents, with an implementation of **Mutual Authorization Verification (MAV)**.

The benchmark includes **7 scenarios**, **11 GUI conditions**, and **10 layouts**. Scenarios cover Photo, File, Editor, Location, Checkout, Drive, and Mail; Drive and Mail require joint decisions across two permission groups.

## Methods

| Method | Entry point |
| --- | --- |
| Vanilla | `vanilla.py` |
| Least-Privilege Prompt (LP) | `least_prompt.py` |
| Self-Check (SC) | `advanced_baselines_runner.py` |
| Fixed-Policy Verifier (FPV) | `policy_only_runner.py` |
| Mutual Authorization Verification (MAV) | `mutual_verifier.py` |

MAV compares a visual agent's proposal with a text-only verifier's choice, performs mutual reconsideration on disagreement, and uses a verifier-guided final agent choice if disagreement persists.

## Setup

Use Python 3.10+ and install the runtime dependencies:

```bash
pip install fastapi uvicorn pydantic playwright pillow
playwright install chromium
```

For local Qwen inference, also install CUDA-compatible PyTorch, `transformers`, and `accelerate`. The Transformers version must support your Qwen2.5-VL or Qwen3.5 checkpoint. Optional 4-bit loading requires `bitsandbytes`.

Keep `suite_app.py`, `vad_core.py`, and the seven scenario `*_app.py` files at the repository root. Place the method entry points and their shared modules (`policy_only.py`, `structured_protocol.py`, and `outcome_metrics.py`) together in `baselines/`.

## Quick Start

Start the benchmark server from the repository root:

```bash
python -m uvicorn suite_app:app --host 127.0.0.1 --port 8004
```

In another terminal, run MAV:

```bash
python -m baselines.mutual_verifier --model-path /path/to/model --results-root results/mav
```

Select another method using its entry point from the table. Use `--scenarios photo`, `--variants control`, or `--layouts 11` for a smaller run; add `--resume` to resume a run with identical configuration. MAV supports `--max-rechecks 1`, `2`, or `3` (default: `1`).

If all Python files are kept in one directory, use `python mutual_verifier.py ...` instead.

## Evaluation

Defaults: seed **42**, temperature **0**, **1,024** output tokens per call, **3** repeats, and **12** executed GUI actions per episode (**14** under Friction). Blocked proposals do not consume the GUI action budget.

- **TSR:** task success rate.
- **LPR:** rate of minimum-permission correctness across all required permission groups.
- **LPTSR:** rate of simultaneous task success and minimum-permission correctness.

Results include per-episode action/model-call logs, `episodes.csv`, and `summary.json`. Infrastructure failures are reported separately as incomplete episodes. Use a fresh results directory when changing the model, code, or experiment configuration.
