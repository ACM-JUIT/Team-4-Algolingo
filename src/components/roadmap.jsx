import "./roadmap.css";

function Roadmap() {
  return (
    <section className="roadmap">

      <h2>🌌 Choose Your Galaxy</h2>

      <p className="roadmap-subtitle">
        Every programming language is its own galaxy full of planets,
        coding missions and rewards.
      </p>

      <div className="roadmap-container">

        <div className="planet-card active">
          <div className="planet">🐍</div>

          <h3>Python Galaxy</h3>

          <p>
            Begin your journey with variables, loops, functions,
            OOP and DSA.
          </p>

          <button>Enter Galaxy</button>
        </div>

        <div className="planet-card">
          <div className="planet">☕</div>

          <h3>Java Galaxy</h3>

          <p>
            Explore object-oriented programming and coding quests.
          </p>

          <button>Coming Soon</button>
        </div>

        <div className="planet-card">
          <div className="planet">⚙️</div>

          <h3>C++ Galaxy</h3>

          <p>
            Learn STL, competitive programming and advanced algorithms.
          </p>

          <button>Coming Soon</button>
        </div>

      </div>

    </section>
  );
}

export default Roadmap;