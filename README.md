# temporal-bench (Technical Details)

## Environment Functionality

- **Task Type:** Single-turn reasoning evaluation.
- **Model receives a temporal reasoning prompt and must:**
  1. Identify relationships between events.
  2. Maintain or update a consistent timeline when given new facts.
  3. (Optionally) Handle a counterfactual variant of the same prompt.

### Evaluation Flow
| Step | Component | Description |
| :--- | :--- | :--- |
| 1 | Prompt Loader | Loads question (MCQ or SAQ) from subset. |
| 2 | Model Response | LLM produces an answer (A/B/C/D or free text). |
| 3 | Judge Selection | Chooses between programmatic judge or LLM judge. |
| 4 | Scoring | Judge compares answer to gold or rubric, assigns weighted score. |
| 5 | Reward Computation | Weighted sum of correctness, temporal coherence, and counterfactual consistency. |

## Judging System

**1. Programmatic Judge (default)**
- **Used for:** MCQ questions.
- **Scoring:** Binary or fractional accuracy.
- **Advantage:** Deterministic, zero-cost.

**2. LLM Judge (optional)**
- **Used for:** SAQ or counterfactual updates.
- **Model:** Configurable (e.g., `gpt-4.1-mini`, `gemini-1.5-flash`, or local API).
- **Scoring rubric:**
  - `temporal_order_correct` (0–1)
  - `explanation_consistent` (0–1)
  - `counterfactual_update_valid` (0–1)
- **Reward:** Weighted mean (0–1).

## Metrics

| Metric | Description |
| :--- | :--- | :--- |
| `reward` | Overall weighted score across criteria. |
| `accuracy` | Fraction of correct answers (for MCQs). |
| `criteria_results` | Per-example boolean vector of evaluation dimensions. |
| `coherence_score` | (Optional) Evaluates internal consistency across multi-part prompts. |

## Configuration Arguments

| Arg | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `dataset_path` | `str` | Local TRAM subset path | Path to the curated subset CSVs |
| `judge_model` | `str` | `"gpt-4.1-mini"` | Model used as LLM judge |
| `use_llm_judge` | `bool` | `False` | Whether to use LLM judge instead of programmatic one |
| `num_examples` | `int` | `32` | Number of examples to sample |
| `use_counterfactuals` | `bool` | `True` | Whether to include counterfactual follow-up questions |
| `seed` | `int` | `42` | For reproducibility |

## Example Usage

```bash
# Run evaluation on 10 examples using default settings
uv run vf-eval temporal-bench -m "gpt-4.1-mini" -n 10 -r 5

# Use custom judge and enable counterfactual reasoning
uv run vf-eval temporal-bench -m "gemini-1.5-flash" --use_llm_judge --use_counterfactuals
```

## Scoring Rubric Example (LLM Judge)

| Criterion | Weight | Description |
| :--- | :--- | :--- |
| `temporal_order_correct` | 0.5 | Correctness of event sequence understanding |
| `duration_reasoning_correct` | 0.2 | Proper inference of time durations |
| `counterfactual_consistency` | 0.2 | Coherence after hypothetical change |
| `explanation_quality` | 0.1 | Clarity and internal reasoning validity |

## Environment Convention (Prime Intellect)

Following the Prime Intellect Environment Hub conventions:

- **Environment name:** `temporal-bench`
- **Each environment must include:**
  - Metadata YAML (`environment.yaml`)
  - Dataset manifest (`dataset_manifest.json`)
  - Evaluator script (`evaluate.py`)
  - Readme (overview, task, config, rubric)
- **Evaluation metrics must be standardized to:**
  - `reward`
  - `criteria_results`
- **Judge API config:** optional, auto-reads from `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.