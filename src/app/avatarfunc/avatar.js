"use client";

export default function UploadAvatar({ setUser }) {
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("avatar", file);

    const res = await fetch("http://localhost:5000/upload-avatar", {
      method: "POST",
      credentials: "include",
      body: formData
    });

    const data = await res.json();

    if (data.avatar) {
      setUser((prev) => ({
        ...prev,
        avatar: data.avatar
      }));
    }
  };

  return (
    <div style={{ marginTop: 10 }}>
      <label
        style={{
          display: "inline-block",
          padding: "10px 18px",
          background: "#0070f3",
          color: "white",
          borderRadius: 8,
          cursor: "pointer",
          fontSize: 14,
          transition: "0.2s",
        }}
      >
        Change profile picture
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          style={{ display: "none" }}
        />
      </label>
    </div>
  );
}
