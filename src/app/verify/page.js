"use client";

import { useSearchParams } from "next/navigation";
import { useState } from "react";

export default function VerifyPage() {
  const searchParams = useSearchParams();
  const email = searchParams.get("email");

  const [code, setCode] = useState("");

  const handleVerify = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:5000/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, code })
    });

    const data = await res.json();
    console.log("VERIFY RESPONSE:", data);

    if (data.message === "Email verified successfully") {
      window.location.href = "/login";
    } else {
      alert("Verification failed: " + data.error);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1 className="title">Email Verification</h1>

        <p className="subtitle">We sent a code to: <b>{email}</b></p>

        <form className="form" onSubmit={handleVerify}>
          <input
            type="text"
            placeholder="Enter verification code"
            className="input"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
          />

          <button type="submit" className="primaryButton">
            Verify Email
          </button>
        </form>
      </div>
    </div>
  );
}

