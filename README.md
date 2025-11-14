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
The TRAM dataset contains 38 different types of temporal reasoning tasks. You can filter by task type:

| Task Type | Description | Count (Train) | Count (Test) |
|-----------|-------------|---------------|--------------|
| ambiguity_resolution_interpretation | Resolving ambiguous temporal expressions through interpretation | 290 | (Test count varies) |
| ambiguity_resolution_shift_calendar | Resolving temporal ambiguities with calendar shifts | 195 | (Test count varies) |
| ambiguity_resolution_shift_lt | Resolving long-term temporal ambiguities | 495 | (Test count varies) |
| ambiguity_resolution_shift_mt | Resolving medium-term temporal ambiguities | 1,249 | (Test count varies) |
| ambiguity_resolution_shift_st | Resolving short-term temporal ambiguities | 895 | (Test count varies) |
| arithmetic_application | Applying arithmetic to temporal problems | 1,937 | (Test count varies) |
| arithmetic_date_computation | Computing dates using arithmetic | 5,895 | (Test count varies) |
| arithmetic_hour_adjustment(12h) | 12-hour format hour adjustments | 1,395 | (Test count varies) |
| arithmetic_hour_adjustment (24h) | 24-hour format hour adjustments | 1,395 | (Test count varies) |
| arithmetic_month_shift | Shifting months using arithmetic | 35 | (Test count varies) |
| arithmetic_time_computation | Computing time using arithmetic | 875 | (Test count varies) |
| arithmetic_time_zone_conversion | Converting between time zones | 395 | (Test count varies) |
| arithmetic_week_identification | Identifying weeks using arithmetic | 1,392 | (Test count varies) |
| arithmetic_year_shift | Shifting years using arithmetic | 1,365 | (Test count varies) |
| causality_cause | Identifying temporal causes | 195 | (Test count varies) |
| causality_effect | Identifying temporal effects | 195 | (Test count varies) |
| duration_analogy_inference | Duration inference using analogies | 695 | (Test count varies) |
| duration_commonsense | Commonsense reasoning about durations | 210 | (Test count varies) |
| duration_computation | Computing durations using arithmetic | 1,395 | (Test count varies) |
| duration_direct_comparison | Direct comparisons of durations | 1,895 | (Test count varies) |
| duration_facts | Factual knowledge about durations | 30 | (Test count varies) |
| duration_multi-step_comparison | Multi-step duration comparisons | 1,395 | (Test count varies) |
| duration_reading_comprehension | Reading comprehension with duration focus | 877 | (Test count varies) |
| frequency_application | Applying frequency concepts to temporal problems | 1,895 | (Test count varies) |
| frequency_commonsense | Commonsense reasoning about frequencies | 190 | (Test count varies) |
| frequency_comparison | Comparing frequencies | 695 | (Test count varies) |
| frequency_computation | Computing frequencies | 1,095 | (Test count varies) |
| frequency_facts | Factual knowledge about frequencies | 43 | (Test count varies) |
| frequency_reading_comprehension | Reading comprehension with frequency focus | 110 | (Test count varies) |
| nli | Natural Language Inference with temporal aspects | 5,000 | (Test count varies) |
| ordering_commonsense | Commonsense reasoning about temporal order | 2,357 | (Test count varies) |
| ordering_facts | Factual knowledge about temporal order | 5,000 | (Test count varies) |
| relation | Reasoning about temporal relations | 5,000 | (Test count varies) |
| storytelling | Temporal aspects in storytelling | 5,000 | (Test count varies) |
| typical_time_comparsion | Comparing typical time durations | 496 | (Test count varies) |
| typical_time_commonsense | Commonsense about typical time durations | 113 | (Test count varies) |
| typical_time_facts | Factual knowledge about typical time durations | 3,002 | (Test count varies) |
| typical_time_reading_comprehension | Reading comprehension with typical time focus | 5,000 | (Test count varies) |

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
| `task_type` | str | `None` | Filter to specific task type (e.g., 'ambiguity_resolution_interpretation', 'arithmetic_date_computation', 'ordering_commonsense', etc.). If None, uses all task types. |
| `system_prompt` | str | `"Evaluate the sequence, duration, or timing of events in the given context. For multiple choice questions, respond with only the letter of the correct answer choice (such as 'A', 'B', 'C', etc.) with no additional text."` | System prompt to guide model behavior |

### Using the Environment for Evaluation
To use this environment in your evaluations:
1. Install the environment with: `prime env install runes/temporal-bench`
2. Run evaluations with: `uv run vf-eval temporal-bench -m [your-model] -n [number-of-examples]`
3. For specific task types: `uv run vf-eval temporal-bench -m [your-model] -n [number] -a '{"task_type":"arithmetic_date_computation"}'`
4. For more details about the environment, visit: [https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench](https://app.primeintellect.ai/dashboard/environments/runes/temporal-bench)

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` | Main scalar reward, 1.0 if the chosen answer is correct, else 0.0 |