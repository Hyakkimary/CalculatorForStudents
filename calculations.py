def calculate_ratings(students):
    results = ""
    for student in students:
        if not student['scores']:
            continue
        total_points = sum(student['scores'])
        weighted_avg = total_points / len(student['scores'])
        total_rating = 0.9 * weighted_avg + student['extra_points']
        results += f"Студент: {student['name']}, Рейтинг загальний: {total_rating:.2f}, Сер. зважений бал: {weighted_avg: .2f}\n"
    return results
