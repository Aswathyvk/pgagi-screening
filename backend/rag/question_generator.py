import random

QUESTION_TEMPLATES = {
    "beginner": [
        "Can you explain what {topic} means and why it's important in {role} work?",
        "Describe a basic use case where you would apply {topic}.",
        "What is the difference between {topic} and a related concept you've worked with?",
        "How would you explain {topic} to someone new to the field?",
    ],
    "intermediate": [
        "Walk me through how you would implement {topic} in a real project.",
        "What are the trade-offs of using {topic} compared to alternative approaches?",
        "Based on the context below, how would you apply {topic} to solve a practical problem?\n\nContext: {context}",
        "How does {topic} fit into a larger {role} system architecture?",
    ],
    "advanced": [
        "Given the following context, critically evaluate when {topic} would NOT be the right choice:\n\nContext: {context}",
        "How would you optimize {topic} for performance and scalability in production?",
        "Design a system that uses {topic} to solve a complex {role} problem. Walk through your reasoning.",
        "What are common pitfalls when implementing {topic}, and how would you avoid them based on this context?\n\nContext: {context}",
    ],
}

TOPIC_KEYWORDS = {
    "ai_ml": ["machine learning models", "neural networks", "supervised learning", "model evaluation", "feature engineering", "overfitting", "gradient descent", "embeddings"],
    "backend": ["API design", "database optimization", "authentication", "caching strategies", "microservices", "concurrency", "error handling", "system scalability"],
    "data_science": ["data preprocessing", "statistical analysis", "data visualization", "model selection", "feature engineering", "exploratory data analysis", "data pipelines"],
    "fullstack": ["state management", "API integration", "component architecture", "responsive design", "authentication flow", "performance optimization"],
}

DIFFICULTY_ORDER = ["beginner", "intermediate", "advanced"]

def generate_question(skills: list, role: str, context_chunks: list, prior_qa: list = []) -> dict:
    topics = TOPIC_KEYWORDS.get(role, TOPIC_KEYWORDS["ai_ml"])

    if skills:
        skill_topics = [s for s in skills if len(s) > 2]
        topics = skill_topics + topics

    asked_topics = set()
    for qa in prior_qa:
        q_text = qa.get("question", "").lower()
        for t in topics:
            if t.lower() in q_text:
                asked_topics.add(t)

    available_topics = [t for t in topics if t not in asked_topics] or topics
    topic = random.choice(available_topics)

    difficulty_index = min(len(prior_qa), len(DIFFICULTY_ORDER) - 1)
    if len(prior_qa) > 0:
        last_answer = prior_qa[-1].get("answer", "")
        if len(last_answer) > 150:
            difficulty_index = min(difficulty_index + 1, len(DIFFICULTY_ORDER) - 1)

    difficulty = DIFFICULTY_ORDER[difficulty_index]

    context_text = ""
    if context_chunks:
        context_text = context_chunks[0]["content"][:400].strip()

    templates = QUESTION_TEMPLATES[difficulty]
    template = random.choice(templates)

    question_text = template.format(topic=topic, role=role.replace("_", " "), context=context_text or "general industry knowledge")

    hint_map = {
        "beginner": f"Cover the core definition and a simple example of {topic}.",
        "intermediate": f"Discuss implementation steps, trade-offs, and practical considerations for {topic}.",
        "advanced": f"Demonstrate deep understanding of {topic} including edge cases, optimization, and architectural impact.",
    }

    return {
        "question": question_text,
        "difficulty": difficulty,
        "topic": topic,
        "hint": hint_map[difficulty],
    }


def evaluate_session(qa_records: list, role: str) -> dict:
    total = len(qa_records)
    if total == 0:
        return {"overall_score": 0, "verdict": "no hire", "summary": "No answers were recorded."}

    word_counts = [len(qa.get("answer", "").split()) for qa in qa_records]
    avg_words = sum(word_counts) / total

    technical_depth = min(100, int(avg_words * 2.5))
    communication = min(100, int(avg_words * 2.2 + 10))
    problem_solving = min(100, int(avg_words * 2.0 + 15))
    role_fit = min(100, int((technical_depth + communication + problem_solving) / 3))

    overall_score = int((technical_depth + communication + problem_solving + role_fit) / 4)

    if overall_score >= 75:
        verdict = "strong hire"
    elif overall_score >= 50:
        verdict = "moderate hire"
    else:
        verdict = "no hire"

    strengths = []
    improvements = []

    if avg_words > 40:
        strengths.append("Provided detailed, thorough answers")
    else:
        improvements.append("Answers could be more detailed and elaborated")

    if technical_depth >= 60:
        strengths.append("Demonstrated solid technical understanding")
    else:
        improvements.append("Technical depth could be strengthened with more specific examples")

    if not strengths:
        strengths.append("Completed the full interview session")
    if not improvements:
        improvements.append("Continue practicing system design and edge case discussions")

    summary = (
        f"The candidate completed {total} question(s) for the {role.replace('_', ' ')} role "
        f"with an average response length of {int(avg_words)} words. "
        f"Overall, the responses suggest a {verdict} based on depth, communication, and problem-solving indicators."
    )

    return {
        "overall_score": overall_score,
        "verdict": verdict,
        "technical_depth": technical_depth,
        "communication": communication,
        "problem_solving": problem_solving,
        "role_fit": role_fit,
        "strengths": strengths,
        "improvements": improvements,
        "summary": summary,
    }