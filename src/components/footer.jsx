import "./footer.css";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        <div className="footer-column">
          <h2>🚀 AlgoLingo</h2>

          <p>
            Explore galaxies, unlock planets, complete coding missions,
            earn XP and become a Master Explorer.
          </p>
        </div>

        <div className="footer-column">
          <h3>Quick Links</h3>

          <ul>
            <li>Home</li>
            <li>Galaxies</li>
            <li>Leaderboard</li>
            <li>Daily Mission</li>
          </ul>
        </div>

        <div className="footer-column">
          <h3>Galaxies</h3>

          <ul>
            <li>🐍 Python Galaxy</li>
            <li>☕ Java Galaxy</li>
            <li>⚙️ C++ Galaxy</li>
          </ul>
        </div>

        <div className="footer-column">
          <h3>Contact</h3>

          <p>📧 support@algolingo.com</p>
          <p>🌍 Explore Beyond Limits</p>

          <div className="socials">
            🚀 ⭐ 💜 🌌
          </div>
        </div>

      </div>

      <hr />

      <p className="copyright">
        © 2026 AlgoLingo • Learn • Explore • Practice • Master 🚀
      </p>

    </footer>
  );
}

export default Footer;