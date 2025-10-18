import argparse
import json
import random
from typing import Any, Dict, List

import verifiers as vf
from verifiers.models import OpenAI
from datasets import load_dataset

import re

def extract_answer(completion: str) -> str:
    completion = completion.strip()
    
    match = re.search(r"\\boxed{([A-Z])}", completion, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    match = re.search(r"(?:answer is|is:|is|:)\\s*([A-Z])", completion, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    matches = re.findall(r"\\b([A-Z])\\b", completion)
    if matches:
        return matches[-1]

    if len(completion) == 2 and completion.endswith('.'):
        return completion[0].upper()

    return completion.upper()

def mcq_reward(parser: vf.Parser, completion: str, answer: str, **kwargs) -> float:
    response = parser.parse_answer(completion)
    return 1.0 if response.lower() == answer.lower() else 0.0

def create_dispatch_reward_function(judge_model_name: str):

    def dispatch_reward_function(parser: vf.Parser, completion: str, answer: str, **kwargs) -> float:
        question_type = kwargs.get('row', {}).get('type')

        if question_type == 'mcq':
            return mcq_reward(parser, completion, answer, **kwargs)
        
        elif question_type == 'saq':
            try:
                judge_llm = OpenAI(model=judge_model_name)
                question = kwargs.get('row', {}).get('question', '')
                submitted_answer = parser.parse_answer(completion)

                prompt = f'''Your task is to assess a submitted answer for a question, based on a provided reference answer.

[Question]
{question}

[Reference Answer]
{answer}

[Submitted Answer]
{submitted_answer}

Evaluate if the "Submitted Answer" is a correct and reasonable answer to the "Question", when compared to the "Reference Answer". The submitted answer does not need to be a perfect match, but it must be factually correct and not contradict the reference answer.

Respond with a single floating-point number from 0.0 to 1.0, where 1.0 represents a perfect match or a fully correct answer, and 0.0 represents a completely incorrect answer. Do not provide any other text or explanation.'''
                
                raw_score = judge_llm.generate(prompt)
                score = float(raw_score.strip())
                return max(0.0, min(1.0, score))
            except Exception as e:
                print(f"LLM Judge failed: {e}")
                return 0.0
        else:
            return 0.0

    return dispatch_reward_function

def load_environment(
    categories: List[str],
    num_examples: int,
    judge_model: str,
    seed: int = 42,
) -> vf.SingleTurnEnv:
    
    all_questions = []
    for category in categories:
        try:
            dataset = load_dataset("tram", name=category, split="validation")
            question_type = 'saq' if 'saq' in category else 'mcq'
            dataset = dataset.add_column("type", [question_type] * len(dataset))
            all_questions.extend(list(dataset))
        except Exception as e:
            print(f"Warning: Could not load category '{category}'. Error: {e}")

    if not all_questions:
        raise ValueError("No questions were loaded. Please check category names.")

    random.seed(seed)
    if len(all_questions) > num_examples:
        dataset = random.sample(all_questions, num_examples)
    else:
        dataset = all_questions

    parser = vf.Parser(extract_fn=extract_answer)
    
    dispatch_function = create_dispatch_reward_function(judge_model)
    rubric = vf.Rubric(parser=parser, funcs=[dispatch_function])
    
    system_prompt = (
        "Please answer the following question. For multiple-choice questions, "
        "provide only the letter of the correct option (e.g., 'A', 'B', 'C')."
    )

    env = vf.SingleTurnEnv(
        dataset=dataset,
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric,
        input_formatter=lambda x: x["question"],
        answer_formatter=lambda x: x["answer_key"] if "answer_key" in x else x["answer"],
    )
    return env

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--categories", nargs='+', default=["ordering"])
    parser.add_argument("-n", "--num_examples", type=int, default=2)
    parser.add_argument("--model", type=str, default="gpt-4.1-mini")
    parser.add_argument("--judge_model", type=str, default="gpt-4.1-mini")
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    env = load_environment(
        categories=args.categories,
        num_examples=args.num_examples,
        judge_model=args.judge_model,
        seed=args.seed,
    )

    print(f"\n--- Initializing Model and Evaluator ---")
    try:
        model = OpenAI(model=args.model)
        print(f"Using model: {model.model}")
    except Exception as e:
        print(f"Error initializing model. Have you set your API key environment variable (e.g., OPENAI_API_KEY)? Error: {e}")
        return

    evaluator = vf.Evaluator()
    print(f"Starting evaluation on {len(env.dataset)} examples...")
    results = evaluator.evaluate(env=env, model=model)

    print("\n--- Evaluation Complete ---")
    print(json.dumps(results.to_dict(), indent=4))


if __name__ == "__main__":
    main()