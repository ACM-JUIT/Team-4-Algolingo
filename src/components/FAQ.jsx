import "./FAQ.css";

function FAQ() {
  return (
    <section className="faq">
      <h2>Frequently Asked Questions</h2>

      <div className="faq-container">

        <div className="faq-item">
          <h3>📚 What is Algolingo?</h3>
          <p>
            Algolingo is an interactive learning platform where students learn
            Data Structures and Algorithms through lessons and quizzes.
          </p>
        </div>

        <div className="faq-item">
          <h3>💰 Is Algolingo free?</h3>
          <p>
            Yes. You can access all beginner lessons and quizzes completely
            free.
          </p>
        </div>

        <div className="faq-item">
          <h3>💻 Do I need coding experience?</h3>
          <p>
            No. Algolingo starts from the basics and gradually moves to
            advanced algorithms.
          </p>
        </div>

        <div className="faq-item">
          <h3>🏆 Can I track my progress?</h3>
          <p>
            Yes. Your dashboard shows completed lessons, quiz scores, XP and
            learning streaks.
          </p>
        </div>

      </div>
    </section>
  );
}

export default FAQ;