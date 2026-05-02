def calculate_mbti(answers: dict) -> str:
    from models.questions import Question

    scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

    def get_letter(q_id, score):
        if 1 <= q_id <= 8:    return 'E' if score >= 3 else 'I'
        if 9 <= q_id <= 18:   return 'I' if score >= 3 else 'E'
        if 19 <= q_id <= 26:  return 'S' if score >= 3 else 'N'
        if 27 <= q_id <= 36:  return 'N' if score >= 3 else 'S'
        if 37 <= q_id <= 44:  return 'T' if score >= 3 else 'F'
        if 45 <= q_id <= 54:  return 'F' if score >= 3 else 'T'
        if 55 <= q_id <= 62:  return 'J' if score >= 3 else 'P'
        if 63 <= q_id <= 70:  return 'P' if score >= 3 else 'J'
        return None

    for q_id, score in answers.items():
        letter = get_letter(int(q_id), int(score))
        if letter:
            scores[letter] += 1

    mbti = ''
    mbti += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti += 'J' if scores['J'] >= scores['P'] else 'P'
    return mbti