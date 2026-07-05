import { useLocation, useNavigate } from "react-router-dom";
import "./Result.css";

function Result() {

  const location = useLocation();
  const navigate = useNavigate();

  const score = location.state?.score || 0;
  const total = location.state?.total || 5;

  const percentage = Math.round((score / total) * 100);

  let message = "";

  if (percentage >= 80) {
    message = "🏆 Outstanding Explorer!";
  } else if (percentage >= 60) {
    message = "🚀 Great Mission!";
  } else {
    message = "🌟 Keep Exploring!";
  }

  return (
    <div className="result-page">

      <div className="result-card">

        <div className="trophy">
          🏆
        </div>

        <h1>Mission Complete!</h1>

        <h2>{message}</h2>

        <div className="score-circle">
          {score}/{total}
        </div>

        <p className="xp">
          ⭐ You earned <span>{score * 50} XP</span>
        </p>

        <p className="subtitle">
          Keep completing missions to unlock new planets.
        </p>

        <div className="button-group">

          <button
            className="retry-btn"
            onClick={() => navigate("/quiz")}
          >
            🔄 Retry Mission
          </button>

          <button
            className="dashboard-btn"
            onClick={() => navigate("/dashboard")}
          >
            🚀 Dashboard
          </button>

        </div>

      </div>

    </div>
  );
}

export default Result;