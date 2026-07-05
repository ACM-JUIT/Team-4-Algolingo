import "./signup.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

function Signup() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = () => {
    if (!name || !email || !password) {
      alert("Please fill all fields!");
      return;
    }

    alert("Account Created Successfully! 🚀");
    navigate("/dashboard");
  };

  return (
    <div className="signup-page">
      <div className="stars"></div>

      <div className="signup-card">
        <div className="robot">🚀</div>

        <h1>Join AlgoLingo</h1>

        <p>
          Begin your journey through the Algorithm Galaxy.
        </p>

        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="signup-button"
          onClick={handleSignup}
        >
          Create Explorer 🚀
        </button>

        <p className="login-text">
          Already have an account?{" "}
          <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;