"use client";

export default function RegisterPage() {
  const handleRegister = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    const username = formData.get("username");
    const email = formData.get("email");
    const password = formData.get("password");

    const res = await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();
    console.log("REGISTER RESPONSE:", data);

    if (data.message === "Verification code sent") {
      window.location.href = `/verify?email=${email}`; 
    } else { 
      alert("Registration failed: " + data.message); 
    }
  };

  return (
    <div className="page">
  <a href="/" className="logo">
    <img src="/vercel.svg" alt="Logo" />
  </a>

  <div className="card">
    <h1 className="title">REGISTRATION</h1>

    <form className="form" onSubmit={handleRegister}>
      <input type="text" name="username" placeholder="Name" className="input" required />
      <input type="email" name="email" placeholder="Email" className="input" required />
      <input type="password" name="password" placeholder="Password" className="input" required />

      <button type="submit" className="primaryButton">
        Create an account
      </button>
    </form>

    <p className="linkText">
      Already have account? <a href="/login">Login</a>
    </p>
  </div>
</div>
  );
}
