async function login(email, password) {
  const url = "http://23.20.175.90/api/cafeadmin/api/admin-auth/login";

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  const data = await response.json();
  console.log(data);

  if (response.ok) {
    console.log("Login successful:", data);
    localStorage.setItem("access_token", data.access_token);
    return data; // Might contain a token
  } else {
    console.error("Login failed:", data);
    alert(data.message || "Login failed");
  }
}

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // ✅ Prevents page refresh

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
      alert("Please enter both email and password.");
      return;
    }

    login(email, password);

    // Real URL
    window.location.href =
      "http://23.20.175.90/api/cafeadmin/cafe-admin-my-accout-page";

    // Test URL
    // window.location.href = "../../pages/cafeAdminMyAccount.html";
  });
