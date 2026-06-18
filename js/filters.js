// Filters Logic
let allCourses = [];

function initializeFilters(courses) {
  allCourses = courses;

  const searchInput = document.getElementById("searchInput");
  const categoryFilter = document.getElementById("categoryFilter");
  const creditFilter = document.getElementById("creditFilter");
  const performanceFilter = document.getElementById("performanceFilter");

  searchInput.addEventListener("input", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);
  creditFilter.addEventListener("change", applyFilters);
  performanceFilter.addEventListener("change", applyFilters);
}

function applyFilters() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const categoryFilter = document.getElementById("categoryFilter").value;
  const creditFilter = document.getElementById("creditFilter").value;
  const performanceFilter = document.getElementById("performanceFilter").value;

  let filtered = allCourses.filter((item) => {
    const course = item.courses;

    // Search filter
    const matchesSearch =
      course.course_name.toLowerCase().includes(searchTerm) ||
      course.course_code.toLowerCase().includes(searchTerm);

    // Credit filter
    const matchesCredit =
      creditFilter === "all" || course.credit_hours.toString() === creditFilter;

    // Performance filter
    let percentage = calculateCoursePercentage(item);
    let matchesPerformance = true;

    if (performanceFilter !== "all") {
      if (performanceFilter === "excellent")
        matchesPerformance = percentage > 85;
      else if (performanceFilter === "good")
        matchesPerformance = percentage >= 70 && percentage <= 85;
      else if (performanceFilter === "average")
        matchesPerformance = percentage >= 50 && percentage < 70;
      else if (performanceFilter === "poor")
        matchesPerformance = percentage < 50;
    }

    // Category filter (check if course has this category)
    let matchesCategory = true;
    if (categoryFilter !== "all") {
      matchesCategory = item.grade_categories.some(
        (cat) => cat.name === categoryFilter,
      );
    }

    return (
      matchesSearch && matchesCredit && matchesPerformance && matchesCategory
    );
  });

  renderCourses(filtered);
}

function calculateCoursePercentage(item) {
  let totalObtained = 0;
  let totalMax = 0;

  item.grade_categories.forEach((cat) => {
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

  return totalMax > 0 ? (totalObtained / totalMax) * 100 : 0;
}
