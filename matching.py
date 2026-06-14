from models import Student

def find_match(student, db):

    candidates = db.query(Student).filter(
        Student.id != student.id
    ).all()

    best = None
    best_score = -1

    for c in candidates:

        score = 0

        if student.country != c.country:
            score += 30

        if student.interests == c.interests:
            score += 40

        if student.languages == c.languages:
            score += 30

        if score > best_score:
            best_score = score
            best = c

    return best