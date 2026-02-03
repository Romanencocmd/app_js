
export default function Home() {
  return (
    <div className="page">
      <a href="/" className="logo">
        <img src="/vercel.svg" alt="Logo" />
      </a>
      <div className="card">
        <h1 className="title">Nexly</h1>
        

        <div className="heroButtons">
          <button className="heroButton heroPrimary"><a href="/register">Sign-Up</a></button>
          <button className="heroButton heroSecondary"><a href="/login">Sign-In</a></button>
        </div>

      </div>
    </div>
  );
}
