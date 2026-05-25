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


def get_relative_grade(score):

    if score >= 20:
        return {
            "grade": "A",
            "label": "Exceptional",
            "color": "text-emerald-400",
            "bg": "bg-emerald-900/30"
        }

    if score >= 12:
        return {
            "grade": "A-",
            "label": "Excellent",
            "color": "text-green-400",
            "bg": "bg-green-900/30"
        }

    if score >= 6:
        return {
            "grade": "B+",
            "label": "Very Good",
            "color": "text-blue-400",
            "bg": "bg-blue-900/30"
        }

    if score >= 0:
        return {
            "grade": "B",
            "label": "Above Avg",
            "color": "text-indigo-400",
            "bg": "bg-indigo-900/30"
        }

    if score >= -6:
        return {
            "grade": "B-",
            "label": "Average",
            "color": "text-sky-400",
            "bg": "bg-sky-900/30"
        }

    if score >= -12:
        return {
            "grade": "C+",
            "label": "Below Avg",
            "color": "text-amber-400",
            "bg": "bg-amber-900/30"
        }

    if score >= -18:
        return {
            "grade": "C",
            "label": "Satisfactory",
            "color": "text-orange-400",
            "bg": "bg-orange-900/30"
        }

    return {
        "grade": "F",
        "label": "Needs Improvement",
        "color": "text-red-400",
        "bg": "bg-red-900/30"
    }


def calculate_course_stats(course, name):

    total_weighted_obtained = 0.0
    total_weighted_class = 0.0
    total_weight_conducted = 0.0

    category_stats = []

    for cat in course['grade_categories']:

        weight = float(cat['weightage'])
        assessments = cat['assessments']

        # Raw totals
        cat_max = sum(
            float(a['max_mark'])
            for a in assessments
            if float(a['max_mark']) > 0
        )

        cat_obt = sum(
            float(a['obtained_mark'])
            for a in assessments
        )

        cat_cls = sum(
            float(a['class_average'])
            for a in assessments
        )

        # Skip empty categories
        if cat_max <= 0:
            continue

        # Category percentages
        student_category_pct = (
            cat_obt / cat_max
        ) * 100

        class_category_pct = (
            cat_cls / cat_max
        ) * 100

        # Weighted contribution
        weighted_student_score = (
            student_category_pct * weight
        ) / 100

        weighted_class_score = (
            class_category_pct * weight
        ) / 100

        # Add totals
        total_weighted_obtained += weighted_student_score
        total_weighted_class += weighted_class_score

        total_weight_conducted += weight

        # Store category data
        category_stats.append({

            'name': cat['name'],

            'student_marks': round(cat_obt, 1),
            'class_marks': round(cat_cls, 1),
            'max_marks': round(cat_max, 1),

            'weight': round(weight, 1),

            'weighted_score': round(
                weighted_student_score, 2
            ),

            'weighted_class_score': round(
                weighted_class_score, 2
            ),

            'weighted_max': round(weight, 1),

            'percentage': round(
                student_category_pct, 1
            )
        })

    # Final percentages
    if total_weight_conducted > 0:

        student_pct = (
            total_weighted_obtained /
            total_weight_conducted
        ) * 100

        class_pct = (
            total_weighted_class /
            total_weight_conducted
        ) * 100

    else:
        student_pct = 0
        class_pct = 0

    # Safety clamp
    student_pct = min(student_pct, 100)
    class_pct = min(class_pct, 100)

    # Difference
    diff = student_pct - class_pct

    # Relative advantage %
    if class_pct > 0:

        relative_advantage = (
            diff / class_pct
        ) * 100

    else:
        relative_advantage = 0

    # Final intelligent score
    score = (
        diff * 0.7
    ) + (
        relative_advantage * 0.3
    )

    stats = {

        'percentage': f"{student_pct:.2f}",
        'class_percentage': f"{class_pct:.2f}",

        'diff': f"{diff:+.2f}",
        'diff_val': round(diff, 2),

        'relative_advantage': round(
            relative_advantage, 2
        ),

        'prediction_score': round(score, 2),

        'estimated_grade': get_relative_grade(score),

        # Weighted totals
        'total_obtained': f"{total_weighted_obtained:.2f}",

        'class_total_obtained': f"{total_weighted_class:.2f}",

        'total_conducted_max': f"{total_weight_conducted:.2f}",

        'category_stats': category_stats,

        'gpa': estimate_gpa(student_pct),

        'student_name': name
    }

    stats["feedback"] = generate_feedback(
        stats,
        float(course.get("attendance", 0))
    )

    return stats