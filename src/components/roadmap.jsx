import "./Roadmap.css";

function Roadmap() {
  return (
    <section className="roadmap">

      <h2>Choose Your Learning Path</h2>

      <div className="roadmap-container">

        <div className="roadmap-card">
          <h3>🟢 Beginner</h3>

          <ul>
            <li>✔ Variables</li>
            <li>✔ Data Types</li>
            <li>✔ Operators</li>
            <li>✔ Loops</li>
            <li>✔ Arrays</li>
          </ul>

          <button>Start Learning</button>

        </div>

        <div className="roadmap-card">

          <h3>🟡 Intermediate</h3>

          <ul>
            <li>✔ Linked List</li>
            <li>✔ Stack</li>
            <li>✔ Queue</li>
            <li>✔ Searching</li>
            <li>✔ Sorting</li>
          </ul>

          <button>Start Learning</button>

        </div>

        <div className="roadmap-card">

          <h3>🔴 Advanced</h3>

          <ul>
            <li>✔ Trees</li>
            <li>✔ Graphs</li>
            <li>✔ Greedy</li>
            <li>✔ Dynamic Programming</li>
            <li>✔ Backtracking</li>
          </ul>

          <button>Start Learning</button>

        </div>

      </div>

    </section>
  );
}

export default Roadmap;