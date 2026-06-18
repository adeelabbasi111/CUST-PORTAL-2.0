// Analytics Logic
function initializeAnalytics(courses) {
  renderStrongestWeakest(courses);
  renderCategoryChart(courses);
  renderAlerts(courses);
}

function renderStrongestWeakest(courses) {
  const coursePercentages = courses.map((item) => ({
    name: item.courses.course_name,
    code: item.courses.course_code,
    percentage: calculateCoursePercentage(item),
  }));

  // Sort by percentage
  const sorted = [...coursePercentages].sort(
    (a, b) => b.percentage - a.percentage,
  );

  // Strongest (top 3)
  const strongest = sorted.slice(0, 3);
  const strongestContainer = document.getElementById("strongestSubjects");
  strongestContainer.innerHTML = strongest
    .map(
      (c) => `
        <div class="analytics-item">
            <span class="course-name">${c.name}</span>
            <span class="percentage">${c.percentage.toFixed(1)}%</span>
        </div>
    `,
    )
    .join("");

  // Weakest (bottom 3)
  const weakest = sorted.slice(-3).reverse();
  const weakContainer = document.getElementById("weakSubjects");
  weakContainer.innerHTML = weakest
    .map(
      (c) => `
        <div class="analytics-item">
            <span class="course-name">${c.name}</span>
            <span class="percentage">${c.percentage.toFixed(1)}%</span>
        </div>
    `,
    )
    .join("");
}

function renderCategoryChart(courses) {
  // Aggregate category performance
  const categoryStats = {};

  courses.forEach((item) => {
    item.grade_categories.forEach((cat) => {
      if (!categoryStats[cat.name]) {
        categoryStats[cat.name] = { total: 0, count: 0 };
      }

      const catMax = cat.assessments.reduce(
        (sum, a) => sum + parseFloat(a.max_mark),
        0,
      );
      const catObtained = cat.assessments.reduce(
        (sum, a) => sum + parseFloat(a.obtained_mark),
        0,
      );
      const percentage = catMax > 0 ? (catObtained / catMax) * 100 : 0;

      categoryStats[cat.name].total += percentage;
      categoryStats[cat.name].count++;
    });
  });

  // Calculate averages
  const labels = Object.keys(categoryStats);
  const data = labels.map((label) => {
    const stat = categoryStats[label];
    return (stat.total / stat.count).toFixed(1);
  });

  // Render chart
  const ctx = document.getElementById("categoryChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Average Performance (%)",
          data: data,
          backgroundColor: [
            "rgba(99, 102, 241, 0.8)",
            "rgba(0, 242, 254, 0.8)",
            "rgba(139, 92, 246, 0.8)",
          ],
          borderColor: [
            "rgba(99, 102, 241, 1)",
            "rgba(0, 242, 254, 1)",
            "rgba(139, 92, 246, 1)",
          ],
          borderWidth: 2,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            color: "#94a3b8",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.05)",
          },
        },
        x: {
          ticks: {
            color: "#94a3b8",
          },
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

function renderAlerts(courses) {
  const alerts = [];

  courses.forEach((item) => {
    const course = item.courses;
    const attendance = parseFloat(item.attendance);

    // Low attendance alert
    if (attendance < 75) {
      alerts.push({
        type: "danger",
        icon: "⚠️",
        message: `Low attendance in ${course.course_name} (${attendance}%)`,
      });
    } else if (attendance < 85) {
      alerts.push({
        type: "warning",
        icon: "📉",
        message: `Attendance below 85% in ${course.course_name} (${attendance}%)`,
      });
    }

    // Low performance alert
    const percentage = calculateCoursePercentage(item);
    if (percentage < 50) {
      alerts.push({
        type: "danger",
        icon: "📊",
        message: `Poor performance in ${course.course_name} (${percentage.toFixed(1)}%)`,
      });
    }
  });

  const alertsContainer = document.getElementById("alertsList");

  if (alerts.length === 0) {
    alertsContainer.innerHTML = `
            <div class="alert-item success">
                <span>✅</span>
                <span>No alerts! You're doing great!</span>
            </div>
        `;
  } else {
    alertsContainer.innerHTML = alerts
      .map(
        (alert) => `
            <div class="alert-item ${alert.type}">
                <span>${alert.icon}</span>
                <span>${alert.message}</span>
            </div>
        `,
      )
      .join("");
  }
}

// Goal Planner
function initializeGoalPlanner(student) {
  const targetCGPAInput = document.getElementById("targetCGPA");
  const currentSemesterSelect = document.getElementById("currentSemester");
  const requiredGPADisplay = document.getElementById("requiredGPA");
  const gpaFill = document.getElementById("gpaFill");
  const statusMsg = document.getElementById("statusMsg");

  function calculateRequiredGPA() {
    const targetCGPA = parseFloat(targetCGPAInput.value);
    const currentSemester = parseInt(currentSemesterSelect.value);
    const currentCGPA = student.cgpa;
    const earnedCredits = parseFloat(
      document.getElementById("creditsEarned").textContent,
    );

    if (!targetCGPA || targetCGPA <= currentCGPA) {
      requiredGPADisplay.textContent = "--";
      gpaFill.style.width = "0%";
      statusMsg.textContent = "Set your goal & semester to calculate";
      statusMsg.className = "status-msg";
      return;
    }

    // Calculate required GPA for remaining semesters
    const totalSemesters = 8;
    const remainingSemesters = totalSemesters - currentSemester + 1;
    const assumedCreditsPerSemester = 18; // Average
    const remainingCredits = remainingSemesters * assumedCreditsPerSemester;

    const requiredGPA =
      (targetCGPA * (earnedCredits + remainingCredits) -
        currentCGPA * earnedCredits) /
      remainingCredits;

    requiredGPADisplay.textContent = requiredGPA.toFixed(2);

    // Update progress bar
    const progress = Math.min((requiredGPA / 4) * 100, 100);
    gpaFill.style.width = progress + "%";

    // Update status message
    if (requiredGPA > 4) {
      statusMsg.textContent = "⚠️ Target not achievable with current credits";
      statusMsg.className = "status-msg impossible";
    } else if (requiredGPA > 3.5) {
      statusMsg.textContent =
        "🔥 Challenging but achievable with consistent effort";
      statusMsg.className = "status-msg challenging";
    } else if (requiredGPA > 3.0) {
      statusMsg.textContent = "✅ Achievable with good study habits";
      statusMsg.className = "status-msg achievable";
    } else {
      statusMsg.textContent = "🎯 Easily achievable! Keep it up!";
      statusMsg.className = "status-msg achievable";
    }
  }

  targetCGPAInput.addEventListener("input", calculateRequiredGPA);
  currentSemesterSelect.addEventListener("change", calculateRequiredGPA);
}
