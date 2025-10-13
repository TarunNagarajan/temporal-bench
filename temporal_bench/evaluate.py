import argparse
import os
import json
from Typing import Any, Dict, List

def load_dataset(path: str, num_examples: int, seed: int) -> List[Dict[str, Any]] :
    """
    - specify path of 'temporal_bench_mcq.csv' and 'temporal_bench_saq.csv'
    - parse CSVs into a list of question objects
    - random sampling of 'num_examples' examples from the list (seed for reproducbility) 
    """
    print(f"Dataset Load: '{path}'...")
    dummy_dataset = [
            {"id": i, "type": "mcq", "question": f"This is question {i}."}
            for i in range(num_examples)
    ]

    return dummy_dataset

def evaluate_model(
        model_name: str,
        dataset: List[Dict[str, Any]],
        use_llm_judge: bool,
        judge_model: str,
        use_counterfactuals: bool
        ) -> Dict[str, Any]:
    """
    runs the temporal reasoning evaluation
    """
    
    results = {
        "reward": 0.0,
        "accuracy": 0.0,
        "criteria_results": [],
        "coherence_score": 0.0,
        "config": {
            "model_name": model_name,
            "num_examples": len(dataset)
            "use_llm_judge": use_llm_judge,
            "judge_model": judge_model,
            "use_counterfactuals": use_counterfactuals,
            },
        }

    return results



