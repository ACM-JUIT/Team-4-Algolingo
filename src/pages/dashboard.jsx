import "./Dashboard.css";
import { Link } from "react-router-dom";


function Dashboard() {
  return (
    <div className="dashboard">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Algolingo</h2>

        <ul>
          <li>
            <Link to="/dashboard">🏠 Dashboard</Link>
          </li>

          <li>
            <Link to="/learning">📚 Learning</Link>
          </li>

          <li>
            <Link to="/quiz">📝 Quizzes</Link>
          </li>
          <li>📊 Results</li>
          <li>👤 Profile</li>
          <li>⚙️ Settings</li>

          <li>
            <Link to="/">🚪 Logout</Link>
          </li>
        </ul>
      </aside>
      {/* Main Content */}
      <main className="main-content">

        <div className="welcome-card">
          <h1>Welcome Back 👋</h1>
          <p>Continue learning Data Structures & Algorithms.</p>
        </div>

        <div className="stats">

          <div className="stat-card">
            <h2>1200</h2>
            <p>XP Points</p>
          </div>

          <div className="stat-card">
            <h2>15 🔥</h2>
            <p>Day Streak</p>
          </div>

          <div className="stat-card">
            <h2>18</h2>
            <p>Lessons Completed</p>
          </div>

          <div className="stat-card">
            <h2>92%</h2>
            <p>Quiz Accuracy</p>
          </div>

        </div>

        <div className="continue-learning">

          <h2>Continue Learning</h2>

          <p>
            Next Lesson:
            <strong> Binary Search</strong>
          </p>

          <div className="progress-bar">

            <div className="progress-fill"></div>

          </div>

          <p>65% Completed</p>

          <button className="continue-btn">

            Continue Lesson

          </button>

        </div>
        {/* Achievements Section */}

        <div className="achievements">

          <h2>🏆 Achievements</h2>

          <div className="achievement-grid">

            <div className="achievement-card">
              <h3>🔥 15 Day Streak</h3>
              <p>Keep learning every day!</p>
            </div>

            <div className="achievement-card">
              <h3>⭐ 1200 XP</h3>
              <p>Great progress so far.</p>
            </div>

            <div className="achievement-card">
              <h3>🎯 Quiz Master</h3>
              <p>Scored above 90% in quizzes.</p>
            </div>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Dashboard;