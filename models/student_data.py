from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Assessment:
    """
    Represents a single graded item within a category (e.g., Quiz 1, Assignment 2).
    """
    name: str = ""
    max_mark: str = "0.00"
    obtained_mark: str = "0.00"
    class_average: str = "0.00"
    percentage: str = "0.00"

@dataclass
class GradeCategory:
    """
    Represents a grade category (e.g., Quiz, Mid Term, Assignments)
    containing weightage and a list of assessments.
    """
    name: str = ""
    weightage: str = "0.0"  # e.g., "15.0"
    total_obtained: str = "0.00"  # The total score for this category (e.g., 18.75)
    assessments: List[Assessment] = field(default_factory=list)

@dataclass
class Course:
    course_identifier: str
    course_name: str
    teacher: str
    course_code: str
    credit_hours: str
    attendance: str
    # New field for detailed grade breakdown
    grade_categories: List[GradeCategory] = field(default_factory=list)

@dataclass
class PersonalInfo:
    name: str
    reg_no: str
    cgpa: str

@dataclass
class Summary:
    earned_credits: str = "N/A"
    total_credits: str = "N/A"
    inprogress_credits: str = "N/A"

@dataclass
class StudentData:
    personal_info: PersonalInfo
    courses: List[Course]
    summary: Summary

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the data structure to a dictionary.
        Useful for debugging or passing data to visualization modules.
        """
        return {
            "personal_info": self.personal_info.__dict__,
            "courses": [
                {
                    **c.__dict__,
                    # Ensure nested grade categories are also converted to dicts
                    "grade_categories": [gc.__dict__ for gc in c.grade_categories]
                }
                for c in self.courses
            ],
            "summary": self.summary.__dict__
        }

    def get_course_by_code(self, code: str) -> Optional[Course]:
        """Helper to find a specific course quickly."""
        for course in self.courses:
            if course.course_code == code:
                return course
        return None