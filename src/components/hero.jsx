import { Link } from "react-router-dom";
import "./Hero.css";

function Hero() {
  return (
    <section className="hero">
      <div className="hero-left">
        <h1>Learn Algorithms the Fun Way!</h1>

        <p>
          Master Data Structures and Algorithms through interactive lessons,
          quizzes, streaks, and rewards.
        </p>

        <div className="hero-buttons">
          <Link to="/signup">
            <button className="start-btn">Start Learning</button>
          </Link>

          <Link to="/login">
            <button className="learn-btn">Login</button>
          </Link>
        </div>
      </div>

      <div className="hero-right">
        <img
          src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
          alt="Learning"
        />
      </div>
    </section>
  );
}

export default Hero;