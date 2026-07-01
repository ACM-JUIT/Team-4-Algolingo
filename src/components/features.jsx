import "./Features.css";
import { FaBookOpen, FaQuestionCircle, FaTrophy } from "react-icons/fa";

function Features() {
  return (
    <section className="features" id="features">
      <h2>Why Choose Algolingo?</h2>

      <div className="feature-container">

        <div className="feature-card">
          <FaBookOpen className="feature-icon" />
          <h3>Interactive Lessons</h3>
          <p>
            Learn algorithms with simple explanations, examples,
            and visual learning.
          </p>
        </div>

        <div className="feature-card">
          <FaQuestionCircle className="feature-icon" />
          <h3>Practice Quizzes</h3>
          <p>
            Test your knowledge after every lesson with fun quizzes.
          </p>
        </div>

        <div className="feature-card">
          <FaTrophy className="feature-icon" />
          <h3>XP & Achievements</h3>
          <p>
            Earn XP, maintain streaks, unlock badges,
            and track your progress.
          </p>
        </div>

      </div>
    </section>
  );
}

export default Features;