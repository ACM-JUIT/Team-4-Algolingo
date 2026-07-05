import "./dashboard.css";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">

      <div className="dashboard-header">
        <div>
          <h1>🐍 Python Galaxy</h1>
          <p>Welcome back, Explorer!</p>
        </div>

        <button className="xp-btn">
          ⚡ 350 XP
        </button>
      </div>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>🚀 Continue Journey</h2>
          <p>Next Planet</p>
          <h3>Functions Planet</h3>

          <button onClick={() => navigate("/learning")}>
            Launch Mission 🚀
          </button>
        </div>

        <div className="dashboard-card">
          <h2>🔥 Current Streak</h2>
          <h1>7 Days</h1>
          <p>Keep solving daily missions.</p>
        </div>

        <div className="dashboard-card">
          <h2>🏆 Daily Challenge</h2>
          <p>Solve one recursion problem.</p>

          <button onClick={() => navigate("/quiz")}>
            Start Challenge
          </button>
        </div>

        <div className="dashboard-card progress">
          <h2>Mission Progress</h2>

          <div className="progress-bar">
            <div className="progress-fill"></div>
          </div>

          <p>72% Completed</p>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;