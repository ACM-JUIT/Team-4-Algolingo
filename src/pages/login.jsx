import "./login.css";
import { Link, useNavigate } from "react-router-dom";

function Login() {

  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/dashboard");
  };

  return (
    <div className="login-page">

      <div className="stars"></div>

      <div className="login-card">

        <div className="robot">
          🤖
        </div>

        <h1>Welcome Back, Explorer</h1>

        <p>Login to continue your mission through the Algorithm Galaxy.</p>

        <input
          type="email"
          placeholder="Email"
        />

        <input
          type="password"
          placeholder="Password"
        />

        <button
          className="login-button"
          onClick={handleLogin}
        >
          Launch Mission 🚀
        </button>

        <p className="signup-text">
          New Explorer?{" "}

          <Link to="/signup">
            Create Account
          </Link>

        </p>

      </div>

    </div>
  );
}

export default Login;