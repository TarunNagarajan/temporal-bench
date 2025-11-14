# temporal-bench

### Overview
- **Environment ID**: `temporal-bench`
- **Short description**: A temporal reasoning evaluation environment for LLMs, evaluating models on their ability to reason about time sequences, durations, and temporal relationships.
- **Tags**: eval, reasoning, single-turn, temporal, temporal-bench

### Citation
If you use this environment, please cite:
- TRAM Dataset: [TRAM: Temporal Reasoning About Events](https://arxiv.org/abs/2310.00835) by Yuqing Wang, Yun Zhao.
- Hugging Face dataset: Warrieryes/TRAM-Temporal

### Datasets
- **Primary dataset(s)**: TRAM (Temporal Reasoning About Events) dataset loaded via the Hugging Face datasets library
- **Source links**: [TRAM-Temporal dataset on Hugging Face](https://huggingface.co/datasets/Warrieryes/TRAM-Temporal)
- **Split sizes**: Uses test split with 3,800 examples and train split with 59,691 examples

### Task Types
The TRAM dataset contains various temporal reasoning tasks. You can filter by task type:

| Task Type | Description | Count |
|-----------|-------------|-------|
| ambiguity_resolution_interpretation | Resolving ambiguous temporal expressions | ~3,800 (test) / ~59,691 (train) |

To select specific task types, use environment arguments as described below.

### Task
- **Type**: single-turn
- **Parser**: Custom `TemporalBenchParser` that extracts the final lettered answer (e.g., 'B') or formatted answer from the model's output using regex.
- **Rubric overview**: The reward is calculated by an exact match reward function, which returns 1.0 for correct answers and 0.0 for incorrect ones.

### Quickstart
Run an evaluation with default settings:

```bash
uv run vf-eval temporal-bench
```

Configure model and sampling:

```bash
uv run vf-eval temporal-bench -m gpt-4.1-mini -n 20 -r 3 -t 8192 -T 0.7 -a '{"dataset_split":"test"}'
```

Notes:
- Use `-a` / `--env-args` to pass environment-specific configuration as a JSON object.

### Environment Arguments
Document any supported environment arguments and their meaning. Example:

| Arg | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `dataset_split` | str | `"test"` | Dataset split to use (train/test) |
| `system_prompt` | str | `"Evaluate the sequence, duration, or timing of events in the given context. For multiple choice questions, respond with only the letter of the correct answer choice (such as 'A', 'B', 'C', etc.) with no additional text."` | System prompt to guide model behavior |

### Using the Environment for Evaluation
To use this environment in your evaluations:
1. Install the environment with: `prime env install runes/temporal-bench`
2. Run evaluations with: `uv run vf-eval temporal-bench -m [your-model] -n [number-of-examples]`
3. For more details about the environment, visit: [https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench](https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench)

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` | Main scalar reward, 1.0 if the chosen answer is correct, else 0.0 |