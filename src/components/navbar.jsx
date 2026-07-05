import { Link } from "react-router-dom";
import "./navbar.css";

function Navbar() {
  return (
    <nav className="navbar">

      <h2 className="logo">
        🚀 AlgoLingo
      </h2>

      <div className="nav-links">
        <a href="#">Galaxies</a>
        <a href="#">Leaderboard</a>
        <a href="#">Museum</a>
        <a href="#">Daily Mission</a>
      </div>

      <div className="nav-buttons">
        <Link to="/login">
          <button className="login-btn">Login</button>
        </Link>

        <Link to="/signup">
          <button className="signup-btn">Sign Up</button>
        </Link>
      </div>

    </nav>
  );
}

export default Navbar;