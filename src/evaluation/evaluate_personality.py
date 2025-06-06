def evaluate_personality(user_feedback):
    """
    Evaluates the chatbot's personality based on user feedback.

    Parameters:
    user_feedback (list): A list of feedback strings provided by users.

    Returns:
    dict: A dictionary containing personality traits and their corresponding scores.
    """
    personality_traits = {
        "friendly": 0,
        "helpful": 0,
        "knowledgeable": 0,
        "engaging": 0,
        "concise": 0
    }

    for feedback in user_feedback:
        if "friendly" in feedback.lower():
            personality_traits["friendly"] += 1
        if "helpful" in feedback.lower():
            personality_traits["helpful"] += 1
        if "knowledgeable" in feedback.lower():
            personality_traits["knowledgeable"] += 1
        if "engaging" in feedback.lower():
            personality_traits["engaging"] += 1
        if "concise" in feedback.lower():
            personality_traits["concise"] += 1

    total_feedback = len(user_feedback)
    if total_feedback > 0:
        for trait in personality_traits:
            personality_traits[trait] = personality_traits[trait] / total_feedback

    return personality_traits

def collect_user_feedback():
    """
    Placeholder function to collect user feedback for personality evaluation.

    Returns:
    list: A list of feedback strings from users.
    """
    feedback = []
    print("Please provide your feedback about the chatbot (type 'exit' to finish):")
    while True:
        user_input = input("Feedback: ")
        if user_input.lower() == 'exit':
            break
        feedback.append(user_input)
    return feedback

def main():
    feedback = collect_user_feedback()
    personality_scores = evaluate_personality(feedback)
    print("Personality Evaluation Scores:")
    for trait, score in personality_scores.items():
        print(f"{trait.capitalize()}: {score:.2f}")

if __name__ == "__main__":
    main()