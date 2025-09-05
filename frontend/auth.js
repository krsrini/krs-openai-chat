async function postJSON(url, data) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data || {})
  });
  return r.json();
}

async function getMe() {
  const r = await fetch("/api/me", { credentials: "include" });
  return r.json();
}

window.handleGoogle = async (response) => {
  try {
    const data = await postJSON("/api/google-login", { id_token: response.credential });
    if (data.ok) window.location.href = "/chat";
    else document.getElementById("auth-error").textContent = data.error || "Google login failed";
  } catch (e) {
    document.getElementById("auth-error").textContent = e.message;
  }
};

window.addEventListener("DOMContentLoaded", async () => {
  const me = await getMe();
  if (me.username) {
    window.location.href = "/chat";
    return;
  }

  const $ = (id) => document.getElementById(id);
  $("btn-login").onclick = async () => {
    const username = $("username").value.trim();
    const password = $("password").value;
    const data = await postJSON("/api/login", { username, password });
    if (data.ok) window.location.href = "/chat";
    else $("auth-error").textContent = data.error || "Login failed";
  };

  $("btn-signup").onclick = async () => {
    const username = $("username").value.trim();
    const password = $("password").value;
    const data = await postJSON("/api/signup", { username, password });
    if (data.ok) {
      // autologin after signup
      const l = await postJSON("/api/login", { username, password });
      if (l.ok) window.location.href = "/chat";
    } else {
      $("auth-error").textContent = data.error || "Signup failed";
    }
  };
});
