import "./Stats.css";

function Stats() {
  return (
    <section className="stats">
      <div className="stat-card">
        <h1>50+</h1>
        <p>Interactive Lessons</p>
      </div>

      <div className="stat-card">
        <h1>500+</h1>
        <p>Practice Questions</p>
      </div>

      <div className="stat-card">
        <h1>100+</h1>
        <p>Daily Active Learners</p>
      </div>

      <div className="stat-card">
        <h1>10+</h1>
        <p>Algorithms Covered</p>
      </div>
    </section>
  );
}

export default Stats;