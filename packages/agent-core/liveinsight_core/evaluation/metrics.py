def recall_at_k(relevant_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    top_k = set(retrieved_ids[:k])
    return len(relevant_ids.intersection(top_k)) / len(relevant_ids)


def precision_at_k(relevant_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    return len([item for item in top_k if item in relevant_ids]) / k


def tool_success_rate(results: list[bool]) -> float:
    if not results:
        return 0.0
    return sum(1 for item in results if item) / len(results)
