from utils.feedback import generate_feedback

def estimate_gpa(pct):
    if pct >= 90: return 4.0
    if pct >= 85: return 3.7
    if pct >= 80: return 3.3
    if pct >= 75: return 3.0
    if pct >= 70: return 2.7
    if pct >= 65: return 2.3
    if pct >= 60: return 2.0
    if pct >= 50: return 1.0
    return 0.0

def get_relative_grade(diff):
    if diff >= 15: return {"grade": "A", "label": "Exceptional", "color": "text-emerald-400", "bg": "bg-emerald-900/30"}
    if diff >= 10: return {"grade": "A-", "label": "Excellent", "color": "text-green-400", "bg": "bg-green-900/30"}
    if diff >= 5:  return {"grade": "B+", "label": "Very Good", "color": "text-blue-400", "bg": "bg-blue-900/30"}
    if diff >= 0:  return {"grade": "B", "label": "Above Avg", "color": "text-indigo-400", "bg": "bg-indigo-900/30"}
    if diff >= -5: return {"grade": "B-", "label": "Average", "color": "text-sky-400", "bg": "bg-sky-900/30"}
    if diff >= -10: return {"grade": "C+", "label": "Below Avg", "color": "text-amber-400", "bg": "bg-amber-900/30"}
    if diff >= -15: return {"grade": "C", "label": "Satisfactory", "color": "text-orange-400", "bg": "bg-orange-900/30"}
    return {"grade": "F", "label": "Needs Improvement", "color": "text-red-400", "bg": "bg-red-900/30"}

def calculate_course_stats(course,name):
    total_obtained = total_class_obtained = total_conducted_max = 0.0
    total_weighted = total_class_weighted = 0.0
    category_stats = []


    for cat in course['grade_categories']:
        weight = float(cat['weightage'])
        assessments = cat['assessments']
        cat_max = sum(float(a['max_mark']) for a in assessments if float(a['max_mark']) > 0)
        cat_obt = sum(float(a['obtained_mark']) for a in assessments)
        cat_cls = sum(float(a['class_average']) for a in assessments)

        total_obtained += cat_obt
        total_class_obtained += cat_cls
        total_conducted_max += cat_max

        cat_weighted = (cat_obt / cat_max * weight) if cat_max > 0 else 0
        cat_class_weighted = (cat_cls / cat_max * weight) if cat_max > 0 else 0

        total_weighted += cat_weighted
        total_class_weighted += cat_class_weighted

        category_stats.append({
            'name': cat['name'], 'weight': weight,
            'student_marks': cat_obt, 'class_marks': cat_cls,
            'max_marks': cat_max, 'weighted_score': cat_weighted,
        })

    student_pct = (total_obtained / total_conducted_max * 100) if total_conducted_max > 0 else 0
    class_pct = (total_class_obtained / total_conducted_max * 100) if total_conducted_max > 0 else 0
    diff = student_pct - class_pct

    stats = {
        'percentage': f"{student_pct:.2f}", 'class_percentage': f"{class_pct:.2f}",
        'diff': f"{diff:+.2f}", 'diff_val': diff,
        'estimated_grade': get_relative_grade(diff),
        'total_obtained': f"{total_obtained:.1f}", 'total_conducted_max': f"{total_conducted_max:.1f}",
        'class_total_obtained': f"{total_class_obtained:.1f}",
        'category_stats': category_stats, 'gpa': estimate_gpa(student_pct),
        'student_name' : name
    }


    stats["feedback"] = generate_feedback(stats, float(course.get("attendance", 0)))
    return stats