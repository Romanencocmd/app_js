"use client";

export default function LoginPage() {
  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    const email = formData.get("email");
    const password = formData.get("password");

    const res = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      credentials: "include"
    });

    const data = await res.json();

    if (data.message === "Logged in") {
      window.location.href = "/dashboard";
    } else {
      console.log("Login error:", data.error);
    }
  };

  return (
    <div className="page">
      <a href="/" className="logo">
        <img src="/vercel.svg" alt="Logo" />
      </a>

      <div className="card">
        <h1 className="title">LOGIN</h1>

        <form className="form" onSubmit={handleLogin}>
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="input"
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            className="input"
            required
          />

          <button type="submit" className="primaryButton">
            Login
          </button>
        </form>

        <p className="linkText">
          Have no account? <a href="/register">Create</a>
        </p>
      </div>
    </div>
  );
}
