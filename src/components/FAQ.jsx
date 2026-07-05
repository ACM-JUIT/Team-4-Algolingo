import "./FAQ.css";

function FAQ() {
  return (
    <section className="faq">

      <h2>🛰 Mission Support</h2>

      <p className="faq-subtitle">
        Everything you need before starting your coding adventure.
      </p>

      <div className="faq-container">

        <div className="faq-card">
          <h3>🌌 What is AlgoLingo?</h3>
          <p>
            AlgoLingo is a space-themed platform where programming languages
            become galaxies and DSA topics become planets to explore.
          </p>
        </div>

        <div className="faq-card">
          <h3>🚀 How do I earn XP?</h3>
          <p>
            Complete lessons, solve quizzes, finish daily missions and unlock
            achievements to earn XP.
          </p>
        </div>

        <div className="faq-card">
          <h3>🪐 Can I explore multiple galaxies?</h3>
          <p>
            Yes! You can switch between Python, Java and C++ galaxies anytime.
          </p>
        </div>

        <div className="faq-card">
          <h3>🏆 Are there rewards?</h3>
          <p>
            Yes. You'll unlock badges, artifacts, planets, streak rewards and
            higher explorer ranks as you progress.
          </p>
        </div>

      </div>

    </section>
  );
}

export default FAQ;