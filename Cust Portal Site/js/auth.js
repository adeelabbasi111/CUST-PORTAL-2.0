// Authentication Logic
document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("loginBtn");
  const regNoInput = document.getElementById("regNo");
  const cgpaInput = document.getElementById("cgpa");
  const errorMsg = document.getElementById("errorMsg");

  // Check if already logged in
  const storedStudent = localStorage.getItem("studentData");
  if (storedStudent) {
    window.location.href = "dashboard.html";
    return;
  }

  loginBtn.addEventListener("click", async () => {
    const regNo = regNoInput.value.trim().toUpperCase();
    const cgpa = parseFloat(cgpaInput.value);

    // Validation
    if (!regNo || !cgpa) {
      showError("Please fill in all fields");
      return;
    }

    if (cgpa < 0 || cgpa > 4) {
      showError("CGPA must be between 0 and 4");
      return;
    }

    // Disable button
    loginBtn.disabled = true;
    loginBtn.textContent = "🔄 Verifying...";
    errorMsg.style.display = "none";

    try {
      // ✅ YAHAN CHANGE: supabase ki jagah supabaseClient use karein
      const { data, error } = await supabaseClient
        .from("students")
        .select("*")
        .eq("student_id", regNo)
        .eq("cgpa", cgpa)
        .maybeSingle(); // .single() ki jagah .maybeSingle() use karein

      if (error) {
        console.error("Supabase error:", error);
        throw error;
      }

      if (data) {
        // Success - Store in localStorage and redirect
        localStorage.setItem("studentData", JSON.stringify(data));
        window.location.href = "dashboard.html";
      } else {
        showError("Invalid Registration Number or CGPA");
      }
    } catch (err) {
      console.error("Login error:", err);
      showError("Invalid Registration Number or CGPA");
    } finally {
      loginBtn.disabled = false;
      loginBtn.textContent = "🔐 Login";
    }
  });

  // Enter key support
  cgpaInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      loginBtn.click();
    }
  });

  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.style.display = "block";
  }
});
