import "./learning.css";
import { useNavigate } from "react-router-dom";

function Learning() {

  const navigate = useNavigate();

  return (
    <div className="learning-page">

      <h1>🌌 Python Galaxy</h1>

      <p className="subtitle">
        Travel through planets and unlock new coding powers.
      </p>

      <div className="planet-container">

        {/* Variables */}
        <div
          className="planet completed"
          onClick={() => alert("Variables Planet Completed!")}
          style={{ cursor: "pointer" }}
        >
          <div className="planet-icon">🌍</div>
          <h3>Variables</h3>
          <p>Completed</p>
        </div>

        {/* Loops */}
        <div
          className="planet completed"
          onClick={() => alert("Loops Planet Completed!")}
          style={{ cursor: "pointer" }}
        >
          <div className="planet-icon">🪐</div>
          <h3>Loops</h3>
          <p>Completed</p>
        </div>

        {/* Functions */}
        <div className="planet current">
          <div className="planet-icon">🌕</div>

          <h3>Functions</h3>

          <button onClick={() => navigate("/quiz")}>
            Start Mission 🚀
          </button>
        </div>

        {/* Locked */}
        <div
          className="planet locked"
          onClick={() => alert("Complete Functions first!")}
          style={{ cursor: "not-allowed" }}
        >
          <div className="planet-icon">🌑</div>

          <h3>Recursion</h3>

          <p>Locked 🔒</p>
        </div>

        {/* Locked */}
        <div
          className="planet locked"
          onClick={() => alert("Complete previous planets first!")}
          style={{ cursor: "not-allowed" }}
        >
          <div className="planet-icon">☄️</div>

          <h3>Dynamic Programming</h3>

          <p>Locked 🔒</p>
        </div>

      </div>

    </div>
  );
}

export default Learning;