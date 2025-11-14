import verifiers as vf
from datasets import load_dataset
from verifiers.parsers.parser import Parser
from verifiers.types import Messages
import re
from typing import Optional


class TemporalBenchParser(Parser):
    def parse(self, text: str) -> Optional[str]:
        return self.parse_answer(text)

    def parse_answer(self, completion: Messages) -> Optional[str]:
        if isinstance(completion, list):
            assistant_msgs = [msg for msg in completion if msg.get("role") == "assistant"]
            if assistant_msgs:
                text = assistant_msgs[-1].get("content", "")
            else:
                return None
        else:
            text = str(completion)

        match = re.search(r'\(([A-Z])\)', text)
        if match:
            return match.group(1).upper()

        match = re.search(r"(?:answer is|is:|is|:)\s*([A-Z])", text, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        match = re.search(r"\\boxed\{([A-Z])\}", text)
        if match:
            return match.group(1).upper()

        match = re.search(r'\b([A-Z])[\.\)\],]', text)
        if match:
            return match.group(1).upper()

        matches = re.findall(r'\b([A-Z])\b', text)
        if matches:
            possible_answers = [m for m in matches if m in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
            if possible_answers:
                return possible_answers[-1]

        match = re.search(r"\b([A-Z])\.", text)
        if match:
            return match.group(1).upper()

        return text.strip().upper()


def load_environment(
    dataset_split: str = "test",
    task_type: str = None,
    system_prompt: str = "Evaluate the sequence, duration, or timing of events in the given context. For multiple choice questions, respond with only the letter of the correct answer choice (such as 'A', 'B', 'C', etc.) with no additional text.",
    **kwargs
) -> vf.Environment:
    dataset = load_dataset("Warrieryes/TRAM-Temporal", split=dataset_split)
    
    # Filter by task type if specified
    if task_type is not None:
        dataset = dataset.filter(lambda example: example["task"] == task_type)
    
    def process_input(example):
        input_text = example["input"]
        
        if "### Instruction:" in input_text and "### Response:" in input_text:
            response_parts = input_text.split("### Response:")
            
            last_instruction_part = response_parts[-2] if len(response_parts) > 1 else response_parts[0]
            
            if "### Instruction:" in last_instruction_part:
                actual_question = last_instruction_part.split("### Instruction:")[-1].strip()
                input_text = actual_question
            else:
                input_text = last_instruction_part.strip()
        
        return {
            "prompt": [{"role": "user", "content": input_text}],
            "answer": example["answer"],
            "task": example["task"],
        }
    
    dataset = dataset.map(process_input).select_columns(["prompt", "answer", "task"])
    
    parser = TemporalBenchParser()
    
    def exact_match_reward(parser: Parser, completion: Messages, answer: str, **kwargs) -> float:
        response = parser.parse_answer(completion)
        return 1.0 if response and response == answer else 0.0

    rubric = vf.Rubric(funcs=[exact_match_reward], parser=parser)

    return vf.SingleTurnEnv(
        dataset=dataset,
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric,
        **kwargs
    )