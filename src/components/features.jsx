import "./features.css";

function Features() {
  return (
    <section className="features">

      <h2>
        Your Space Learning Journey 🚀
      </h2>

      <p className="feature-subtitle">
        Every coding concept becomes an exciting mission across the universe.
      </p>

      <div className="feature-container">

        <div className="feature-card">
          <div className="feature-icon">🪐</div>

          <h3>Explore Planets</h3>

          <p>
            Learn every topic as a new planet filled with missions and
            discoveries.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">⚡</div>

          <h3>Earn XP</h3>

          <p>
            Complete quizzes and coding challenges to collect XP and unlock
            galaxies.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🏆</div>

          <h3>Collect Artifacts</h3>

          <p>
            Unlock badges, cosmic rewards and legendary explorer achievements.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🤖</div>

          <h3>AI Space Guide</h3>

          <p>
            Get hints from your AI robot while exploring difficult coding
            missions.
          </p>
        </div>

      </div>

    </section>
  );
}

export default Features;