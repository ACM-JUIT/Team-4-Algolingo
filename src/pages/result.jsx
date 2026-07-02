import { useLocation, Link } from "react-router-dom";
import "./Result.css";

function Result() {
  const location = useLocation();

  const score = location.state?.score || 0;
  const total = location.state?.total || 5;

  const percentage = Math.round((score / total) * 100);

  let message = "";

  if (percentage >= 80) {
    message = "🏆 Excellent!";
  } else if (percentage >= 60) {
    message = "👏 Good Job!";
  } else {
    message = "💪 Keep Practicing!";
  }

  return (
    <div className="result-page">

      <div className="result-card">

        <h1>🎉 Quiz Completed!</h1>

        <h2>{message}</h2>

        <div className="score-circle">
          {percentage}%
        </div>

        <h3>
          Score: {score} / {total}
        </h3>

        <div className="button-group">

          <Link to="/quiz">
            <button className="retry-btn">
              🔄 Retry Quiz
            </button>
          </Link>

          <Link to="/dashboard">
            <button className="dashboard-btn">
              🏠 Dashboard
            </button>
          </Link>

        </div>

      </div>

    </div>
  );
}

export default Result;