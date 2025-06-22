# backend/utils/cost_utils.py
import tiktoken

TOKEN_PRICES = {
    "gpt-4-turbo": 0.01 / 1000,
    "gpt-3.5-turbo": 0.0015 / 1000
}

def count_tokens_and_cost(messages, model="gpt-4-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    total_tokens = sum(len(encoding.encode(m["content"])) for m in messages)
    cost = round(total_tokens * TOKEN_PRICES.get(model, 0), 6)
    return {"total_tokens": total_tokens, "estimated_cost_usd": cost}
