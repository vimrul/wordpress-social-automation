def generate_hashtags(text: str, num_tags: int = 5):
    words = [word.strip("#,.!?") for word in text.lower().split() if len(word) > 4]
    hashtags = list(set(words))[:num_tags]
    return ["#" + tag for tag in hashtags]
