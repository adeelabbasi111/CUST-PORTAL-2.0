// Dashboard Logic
document.addEventListener("DOMContentLoaded", async () => {
  // Check authentication
  const studentData = JSON.parse(localStorage.getItem("studentData"));
  if (!studentData) {
    window.location.href = "index.html";
    return;
  }

  // Logout functionality
  document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("studentData");
    window.location.href = "index.html";
  });

  // Load student data
  await loadDashboard(studentData);
});

async function loadDashboard(student) {
  try {
    // Update student info
    document.getElementById("studentName").textContent = student.name;
    document.getElementById("studentReg").textContent = student.student_id;
    document.getElementById("studentCGPA").textContent =
      student.cgpa.toFixed(2);

    // ✅ YAHAN CHANGE: supabaseClient use karein
    const { data: summary } = await supabaseClient
      .from("student_summaries")
      .select("*")
      .eq("student_id", student.student_id)
      .single();

    if (summary) {
      document.getElementById("creditsEarned").textContent =
        summary.earned_credits;
    }

    // ✅ YAHAN CHANGE: supabaseClient use karein
    const { data: studentCourses, error } = await supabaseClient
      .from("student_courses")
      .select(
        `
                *,
                courses:courses!inner(*),
                grade_categories:grade_categories(*, assessments:assessments(*))
            `,
      )
      .eq("student_id", student.student_id);

    if (error) {
      console.error("Error fetching courses:", error);
      throw error;
    }

    document.getElementById("totalCourses").textContent = studentCourses.length;

    // Render courses
    renderCourses(studentCourses);

    // Initialize analytics
    initializeAnalytics(studentCourses);

    // Initialize filters
    initializeFilters(studentCourses);

    // Initialize goal planner
    initializeGoalPlanner(student);
  } catch (error) {
    console.error("Error loading dashboard:", error);
    document.getElementById("coursesContainer").innerHTML =
      '<div class="error-message">Error loading data. Please try again.</div>';
  }
}

function renderCourses(courses) {
  const container = document.getElementById("coursesContainer");
  container.innerHTML = "";

  courses.forEach((item) => {
    const course = item.courses;
    const categories = item.grade_categories;

    // Calculate overall percentage
    let totalObtained = 0;
    let totalMax = 0;

    categories.forEach((cat) => {
      const weight = parseFloat(cat.weightage) / 100;
      const catMax = cat.assessments.reduce(
        (sum, a) => sum + parseFloat(a.max_mark),
        0,
      );
      const catObtained = cat.assessments.reduce(
        (sum, a) => sum + parseFloat(a.obtained_mark),
        0,
      );

      totalMax += catMax * weight;
      totalObtained += catObtained * weight;
    });

    const percentage = totalMax > 0 ? (totalObtained / totalMax) * 100 : 0;
    const grade = calculateGrade(percentage);

    const card = document.createElement("div");
    card.className = "course-card";
    card.innerHTML = `
            <div class="course-header">
                <div>
                    <div class="course-title">${course.course_name}</div>
                    <div class="course-code">${course.course_code}</div>
                </div>
                <div class="grade-badge grade-${grade.letter}">${grade.letter}</div>
            </div>
            
            <div class="course-meta">
                <div class="meta-item">🕒 ${course.credit_hours} Credits</div>
                <div class="meta-item">👨‍🏫 ${course.teacher}</div>
                <div class="meta-item">📅 ${item.attendance}% Attendance</div>
            </div>

            <div class="performance-bar">
                <div class="performance-fill" style="width: ${percentage}%"></div>
            </div>

            <div class="category-breakdown">
                ${categories
                  .map((cat) => {
                    const catMax = cat.assessments.reduce(
                      (sum, a) => sum + parseFloat(a.max_mark),
                      0,
                    );
                    const catObtained = cat.assessments.reduce(
                      (sum, a) => sum + parseFloat(a.obtained_mark),
                      0,
                    );
                    const catPercentage =
                      catMax > 0 ? (catObtained / catMax) * 100 : 0;

                    return `
                        <div class="category-item">
                            <span>${cat.name} (${cat.weightage}%)</span>
                            <span>${catObtained.toFixed(1)} / ${catMax.toFixed(1)} (${catPercentage.toFixed(1)}%)</span>
                        </div>
                    `;
                  })
                  .join("")}
            </div>
        `;

    container.appendChild(card);
  });
}

function calculateGrade(percentage) {
  if (percentage >= 90) return { letter: "A", label: "Excellent" };
  if (percentage >= 80) return { letter: "B", label: "Very Good" };
  if (percentage >= 70) return { letter: "C", label: "Good" };
  if (percentage >= 60) return { letter: "D", label: "Satisfactory" };
  if (percentage >= 50) return { letter: "E", label: "Pass" };
  return { letter: "F", label: "Fail" };
}
