import "./Footer.css";
import { FaFacebook, FaInstagram, FaLinkedin, FaGithub } from "react-icons/fa";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        {/* Logo */}
        <div className="footer-section">
          <h2>Algolingo</h2>
          <p>
            Learn Data Structures and Algorithms in a fun,
            interactive and engaging way.
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer-section">
          <h3>Quick Links</h3>

          <ul>
            <li>Home</li>
            <li>Courses</li>
            <li>Quizzes</li>
            <li>Dashboard</li>
          </ul>
        </div>

        {/* Contact */}
        <div className="footer-section">
          <h3>Contact</h3>

          <p>Email: support@algolingo.com</p>
          <p>Phone: +91 9876543210</p>
          <p>India</p>
        </div>

        {/* Social */}
        <div className="footer-section">

          <h3>Follow Us</h3>

          <div className="social-icons">
            <FaFacebook />
            <FaInstagram />
            <FaLinkedin />
            <FaGithub />
          </div>

        </div>

      </div>

      <hr />

      <p className="copyright">
        © 2026 Algolingo. All Rights Reserved.
      </p>

    </footer>
  );
}

export default Footer;