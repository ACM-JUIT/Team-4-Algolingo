import "./stats.css";

function Stats() {
  return (
    <section className="stats">

      <h2>
        🚀 Mission Control
      </h2>

      <p className="stats-subtitle">
        Join thousands of explorers mastering algorithms across the universe.
      </p>

      <div className="stats-container">

        <div className="stat-card">
          <div className="stat-icon">👨‍🚀</div>
          <h1>15K+</h1>
          <p>Space Explorers</p>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🪐</div>
          <h1>120+</h1>
          <p>Coding Missions</p>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🌌</div>
          <h1>45</h1>
          <p>Learning Planets</p>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <h1>98%</h1>
          <p>Mission Success</p>
        </div>

      </div>

    </section>
  );
}

export default Stats;