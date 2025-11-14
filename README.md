# temporal-bench: Evaluating Temporal Reasoning in Language Models

<div align="center">
  <img src="https://github.com/user-attachments/assets/40c36e38-c5bd-4c5a-9cb3-f7b902cd155d#gh-light-mode-only" alt="Prime Intellect" width="312">
  <img src="https://github.com/user-attachments/assets/6414bc9b-126b-41ca-9307-9e982430cde8#gh-dark-mode-only"  alt="Prime Intellect" width="312">
</div>

### Overview
- **Environment ID**: `temporal-bench`
- **Short description**: A temporal reasoning evaluation environment for LLMs, evaluating models on their ability to reason about time sequences, durations, and temporal relationships.
- **Tags**: eval, reasoning, single-turn, temporal, temporal-bench

### Find this environment on Prime Intellect
This environment is available on the [Prime Intellect Environment's Repository](https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench). Prime Intellect is building a community platform for crowdsourcing open environments, so anyone can contribute to open-source AGI research and evaluation.

### Citation
If you use this environment, please cite:
- TRAM Dataset: [TRAM: Temporal Reasoning About Events](https://arxiv.org/abs/2310.00835) by Yuqing Wang, Yun Zhao.
- Hugging Face dataset: Warrieryes/TRAM-Temporal

### Datasets
- **Primary dataset(s)**: TRAM (Temporal Reasoning About Events) dataset loaded via the Hugging Face datasets library
- **Source links**: [TRAM-Temporal dataset on Hugging Face](https://huggingface.co/datasets/Warrieryes/TRAM-Temporal)
- **Split sizes**: Uses test split with 3,800 examples and train split with 59,691 examples

### Task Types
The TRAM dataset contains 38 different types of temporal reasoning tasks, organized into thematic categories. You can filter by specific task type or by category:

#### Category-Based Filtering
You can filter by broader categories such as:
- `ambiguity_resolution_*` (e.g., `ambiguity_resolution_interpretation`, `ambiguity_resolution_shift_*`)
- `arithmetic_*` (e.g., `arithmetic_date_computation`, `arithmetic_time_computation`, `arithmetic_hour_adjustment*`)
- `causality_*` (e.g., `causality_cause`, `causality_effect`)
- `duration_*` (e.g., `duration_commonsense`, `duration_computation`, `duration_direct_comparison`)
- `frequency_*` (e.g., `frequency_commonsense`, `frequency_computation`, `frequency_comparison`)
- `typical_time_*` (e.g., `typical_time_commonsense`, `typical_time_facts`, `typical_time_computation`)

#### Individual Task Types

| Task Type | Description | Count (Train) |
|-----------|-------------|---------------|
| ambiguity_resolution_interpretation | Resolving ambiguous temporal expressions through interpretation | 290 |
| ambiguity_resolution_shift_calendar | Resolving temporal ambiguities with calendar shifts | 195 |
| ambiguity_resolution_shift_lt | Resolving long-term temporal ambiguities | 495 |
| ambiguity_resolution_shift_mt | Resolving medium-term temporal ambiguities | 1,249 |
| ambiguity_resolution_shift_st | Resolving short-term temporal ambiguities | 895 |
| arithmetic_application | Applying arithmetic to temporal problems | 1,937 |
| arithmetic_date_computation | Computing dates using arithmetic | 5,895 |
| arithmetic_hour_adjustment(12h) | 12-hour format hour adjustments | 1,395 |
| arithmetic_hour_adjustment (24h) | 24-hour format hour adjustments | 1,395 |
| arithmetic_month_shift | Shifting months using arithmetic | 35 |
| arithmetic_time_computation | Computing time using arithmetic | 875 |
| arithmetic_time_zone_conversion | Converting between time zones | 395 |
| arithmetic_week_identification | Identifying weeks using arithmetic | 1,392 |
| arithmetic_year_shift | Shifting years using arithmetic | 1,365 |
| causality_cause | Identifying temporal causes | 195 |
| causality_effect | Identifying temporal effects | 195 |
| duration_analogy_inference | Duration inference using analogies | 695 |
| duration_commonsense | Commonsense reasoning about durations | 210 |
| duration_computation | Computing durations using arithmetic | 1,395 |
| duration_direct_comparison | Direct comparisons of durations | 1,895 |
| duration_facts | Factual knowledge about durations | 30 |
| duration_multi-step_comparison | Multi-step duration comparisons | 1,395 |
| duration_reading_comprehension | Reading comprehension with duration focus | 877 |
| frequency_application | Applying frequency concepts to temporal problems | 1,895 |
| frequency_commonsense | Commonsense reasoning about frequencies | 190 |
| frequency_comparison | Comparing frequencies | 695 |
| frequency_computation | Computing frequencies | 1,095 |
| frequency_facts | Factual knowledge about frequencies | 43 |
| frequency_reading_comprehension | Reading comprehension with frequency focus | 110 |
| nli | Natural Language Inference with temporal aspects | 5,000 |
| ordering_commonsense | Commonsense reasoning about temporal order | 2,357 |
| ordering_facts | Factual knowledge about temporal order | 5,000 |
| relation | Reasoning about temporal relations | 5,000 |
| storytelling | Temporal aspects in storytelling | 5,000 |
| typical_time_comparsion | Comparing typical time durations | 496 |
| typical_time_commonsense | Commonsense about typical time durations | 113 |
| typical_time_facts | Factual knowledge about typical time durations | 3,002 |
| typical_time_reading_comprehension | Reading comprehension with typical time focus | 5,000 |

**Note:** The test split contains 3,800 examples distributed across these task types.

To select specific task types, use the `task_type` environment argument as described below.

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
| `task_type` | str | `None` | Filter to specific task type (e.g., 'ambiguity_resolution_interpretation', 'arithmetic_date_computation', 'ordering_commonsense', etc.) or category (e.g., 'causality_*', 'arithmetic_*', 'ambiguity_resolution_*', etc.). Use '*' suffix to filter by category prefix. If None, uses all task types. |
| `system_prompt` | str | `"Evaluate the sequence, duration, or timing of events in the given context. For multiple choice questions, respond with only the letter of the correct answer choice (such as 'A', 'B', 'C', etc.) with no additional text."` | System prompt to guide model behavior |

### Using the Environment for Evaluation
To use this environment in your evaluations:
1. Install the environment with: `prime env install runes/temporal-bench`
2. Run evaluations with: `uv run vf-eval temporal-bench -m [your-model] -n [number-of-examples]`
3. For specific task types: `uv run vf-eval temporal-bench -m [your-model] -n [number] -a '{"task_type":"arithmetic_date_computation"}'`
4. For categories: `uv run vf-eval temporal-bench -m [your-model] -n [number] -a '{"task_type":"causality_*"}'` (uses all causality task types)
5. For more details about the environment, visit: [https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench](https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench)

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` | Main scalar reward, 1.0 if the chosen answer is correct, else 0.0 |