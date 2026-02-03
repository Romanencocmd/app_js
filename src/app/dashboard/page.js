"use client";
import UploadAvatar from "../avatarfunc/avatar";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function loadUser() {
      const res = await fetch("http://localhost:5000/dashboard", {
        method: "GET",
        credentials: "include"
      });

      const data = await res.json();

      if (data.error) {
        window.location.href = "/login";
      } else {
        setUser(data);
      }
    }

    loadUser();
  }, []);

  return (
    <div className="page">
      <a href="/" className="logo">
        <img src="/vercel.svg" alt="Logo" />
      </a>

      <div className="container">
        <h1 className="title">Dashboard</h1>
      

        {user && (
          <div className="card" style={{ textAlign: "center" }}>
            <img
              src={`http://localhost:5000${user.avatar}`}
              style={{
                width: 120,
                height: 120,
                borderRadius: "50%",
                objectFit: "cover",
                marginBottom: 20,
                border: "3px solid #eee"
              }}
            />
            <h2>Hello, {user.username}</h2>
            <UploadAvatar setUser={setUser} />
          </div>
        )}
        <div className="dashboardRow">
          <div className="dashboardCard">
            <h2>Your projects</h2>
            <p>Manage and view your projects here.</p>
            <button>Go to Projects</button>
          </div>

          <div className="dashboardCard">
            <h2>Statistics</h2>
            <p>View your usage statistics and reports.</p>
            <button>View Stats</button>
          </div>

          <div className="dashboardCard">
            <h2>Account</h2>
            <p>Username: {user?.username}</p>
            <p>Email: {user?.email}</p>
          </div>

          <div className="dashboardCard">
            <h2>Settings</h2>
            <p>Manage your account settings and preferences here.</p>
            <button>Go to Settings</button>
          </div>
        </div>
      </div>
    </div>
  );
}
