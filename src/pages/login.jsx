import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    if (email === "" || password === "") {
      alert("Please fill all the fields.");
      return;
    }

    alert("Login Successful!");
    navigate("/dashboard");
  };

  return (
    <div className="login-page">
      <div className="login-card">

        <h1>Welcome Back 👋</h1>

        <p>Login to continue learning.</p>

        <div className="form-group">
          <label>Email</label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

        </div>

        <div className="form-group">
          <label>Password</label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

        </div>

        <button
          className="login-btn"
          onClick={handleLogin}
        >
          Login
        </button>

        <div className="signup-link">
          Don't have an account?{" "}
          <Link to="/signup">
            Sign Up
          </Link>
        </div>

      </div>
    </div>
  );
}

export default Login;