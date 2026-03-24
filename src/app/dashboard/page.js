"use client";
import UploadAvatar from "../avatarfunc/avatar";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [company, setCompany] = useState(null);
  const [schedule, setSchedule] = useState("Select a company to load schedule");
  const [checkedIn, setCheckedIn] = useState(false);
  const [shiftCalendar, setShiftCalendar] = useState([]);

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

  async function selectCompany(id) {
    await fetch("http://localhost:5000/set-company", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company_id: id })
    });

    setCompany(id);
    loadSchedule(id);
    loadShiftCalendar(id);
  }

  async function loadSchedule(selectedCompany = company) {
    if (!selectedCompany) return;

    const res = await fetch("http://localhost:5000/get-schedule", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company: selectedCompany })
    });

    const data = await res.json();
    setSchedule(data.schedule);
  }

  async function loadShiftCalendar(selectedCompany = company) {
    if (!selectedCompany) return;

    const res = await fetch("http://localhost:5000/get-shift-calendar", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company: selectedCompany })
    });

    const data = await res.json();
    setShiftCalendar(data.calendar || []);
  }

  async function requestLeave() {
    await fetch("http://localhost:5000/request-leave", {
      method: "POST",
      credentials: "include"
    });

    alert("Leave request sent");
  }

  async function handleCheckIn() {
    if (!company) return;

    const res = await fetch("http://localhost:5000/check-in", {
      method: "POST",
      credentials: "include"
    });

    const data = await res.json();
    if (!data.error) setCheckedIn(true);
  }

  async function handleCheckOut() {
    const res = await fetch("http://localhost:5000/check-out", {
      method: "POST",
      credentials: "include"
    });

    const data = await res.json();
    if (!data.error) setCheckedIn(false);
  }

  return (
    <div className="page">
      <a href="/" className="logo">
        <img src="/vercel.svg" alt="Logo" />
      </a>

      <div className="container">
        <h1 className="title">Dashboard</h1>

        {user && (
          <div className="card" style={{ textAlign: "center", position: "relative" }}>
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

            <button
              className="primaryButton"
              style={{
                marginTop: 20,
                padding: "10px 20px",
                backgroundColor: "#0070f3",
                color: "#fff",
                border: "none",
                borderRadius: 5,
                cursor: "pointer"
              }}
              onClick={() => setPanelOpen(true)}
            >
              Work Panel
            </button>
          </div>
        )}

        <div className="dashboardRow">
          <div className="dashboardCard">
            <h2>Your projects</h2>
            <p>Manage and view your projects here</p>
            <button>Go to Projects</button>
          </div>

          <div className="dashboardCard">
            <h2>Statistics</h2>
            <p>View your usage statistics and reports</p>
            <button>View Stats</button>
          </div>

          <div className="dashboardCard">
            <h2>Account</h2>
            <p>Username: {user?.username}</p>
            <p>Email: {user?.email}</p>
          </div>

          <div className="dashboardCard">
            <h2>Settings</h2>
            <p>Manage your account settings and preferences here</p>
            <button>Go to Settings</button>
          </div>
        </div>
      </div>

      
      <div className={`sidePanel ${panelOpen ? "open" : ""}`}>
        <div className="sidePanelHeader">
          <h2>Work Panel</h2>
          <button className="closeBtn" onClick={() => setPanelOpen(false)}>✕</button>
        </div>

        <div className="sidePanelContent">

          
          <div className="panelSection">
            <h3>Work Form</h3>
            <p>Select your company to load your work schedule</p>

            <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
              <button
                className="primaryButton"
                disabled={company !== null}
                style={{
                  opacity: company === null ? 1 : 0.5,
                  cursor: company === null ? "pointer" : "not-allowed"
                }}
                onClick={() => selectCompany(1)}
              >
                Company A
              </button>

              <button
                className="secondaryButton"
                disabled={company !== null}
                style={{
                  opacity: company === null ? 1 : 0.5,
                  cursor: company === null ? "pointer" : "not-allowed"
                }}
                onClick={() => selectCompany(2)}
              >
                Company B
              </button>
            </div>
          </div>

          
          <div className="panelSection">
            <h3>Attendance</h3>
            <p>Your check-in / check-out history</p>

            {!checkedIn ? (
              <button
                className="primaryButton"
                disabled={!company}
                style={{
                  marginTop: 10,
                  opacity: company ? 1 : 0.5,
                  cursor: company ? "pointer" : "not-allowed"
                }}
                onClick={handleCheckIn}
              >
                Check In
              </button>
            ) : (
              <button
                className="secondaryButton"
                style={{ marginTop: 10 }}
                onClick={handleCheckOut}
              >
                Check Out
              </button>
            )}
          </div>

    
          <div className="panelSection">
            <h3>Leave</h3>
            <p>Your vacation and leave requests</p>

            <button
              className="primaryButton"
              style={{ marginTop: 10 }}
              onClick={requestLeave}
            >
              Request Leave
            </button>
          </div>

          
          <div className="panelSection">
            <h3>Shift Time</h3>
            <pre style={{ whiteSpace: "pre-wrap", marginTop: 10 }}>
              {schedule}
            </pre>
          </div>

         
          <div className="panelSection">
            <h3>Shift Calendar</h3>
            <p>Your monthly shift schedule</p>

            <div
              style={{
                maxHeight: "250px",
                overflowY: "auto",
                marginTop: 10,
                border: "1px solid #eee",
                borderRadius: 8,
                padding: 10
              }}
            >
              {shiftCalendar.length === 0 ? (
                <p>Select a company to load calendar</p>
              ) : (
                shiftCalendar.map((day) => (
                  <div
                    key={day.day}
                    style={{
                      padding: "8px 0",
                      borderBottom: "1px solid #f0f0f0",
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 14
                    }}
                  >
                    <span>
                      <b>{day.day}</b> — {day.weekday}
                    </span>
                    <span>{day.shift}</span>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
