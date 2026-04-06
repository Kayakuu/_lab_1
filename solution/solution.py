"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable, Tuple, Dict
import openai

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

# Rerouting to Gemini API for free tier usage
OPENAI_MODEL = "gemini-1.5-pro"
OPENAI_MINI_MODEL = "gemini-1.5-flash"

def get_client():
    return openai.OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> Tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    start_time = time.time()
    client = get_client()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    
    latency = max(time.time() - start_time, 0.001)
    return response.choices[0].message.content or "", latency

# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> Tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> Dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)
    
    # Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    words = len(gpt4o_response.split())
    cost_estimate = (words / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": cost_estimate,
    }

# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    history = []
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                break
        except (EOFError, KeyboardInterrupt):
            break
            
        history.append({"role": "user", "content": user_input})
        history = history[-6:] # Keep last 3 turns
        
        print("Assistant: ", end="", flush=True)
        client = get_client()
        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL,
            messages=history,
            stream=True
        )
        
        reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            reply += delta
            
        history.append({"role": "assistant", "content": reply})
        history = history[-6:]

# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    last_ex = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_ex = e
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))
    if last_ex:
        raise last_ex

# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for p in prompts:
        res = compare_models(p)
        res["prompt"] = p
        results.append(res)
    return results

# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    header = f"{'Prompt':<25} | {'GPT-4o':<15} | {'Mini':<15} | {'Lat 4o':<8} | {'Lat Mini':<8}"
    separator = "-" * len(header)
    lines = [header, separator]
    
    for r in results:
        p = (r['prompt'][:22] + '...') if len(r['prompt']) > 25 else r['prompt']
        g = (r['gpt4o_response'][:12] + '...') if len(r['gpt4o_response']) > 15 else r['gpt4o_response']
        m = (r['mini_response'][:12] + '...') if len(r['mini_response']) > 15 else r['mini_response']
        l4 = f"{r['gpt4o_latency']:.2f}s"
        lm = f"{r['mini_latency']:.2f}s"
        lines.append(f"{p:<25} | {g:<15} | {m:<15} | {l4:<8} | {lm:<8}")
        
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
