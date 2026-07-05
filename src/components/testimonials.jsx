import "./testimonials.css";

function Testimonials() {
  return (
    <section className="testimonials">

      <h2>⭐ Explorer Reviews</h2>

      <p className="testimonial-subtitle">
        Hear from fellow explorers who conquered the Algorithm Galaxy.
      </p>

      <div className="testimonial-container">

        <div className="review-card">
          <div className="avatar">👨‍🚀</div>

          <h3>Alex</h3>

          <p>
            "Learning DSA feels like exploring planets instead of reading
            boring notes. The missions are addictive!"
          </p>

          <span>⭐⭐⭐⭐⭐</span>
        </div>

        <div className="review-card">
          <div className="avatar">👩‍🚀</div>

          <h3>Sophia</h3>

          <p>
            "The XP system keeps me motivated every day. I actually enjoy
            solving algorithms now."
          </p>

          <span>⭐⭐⭐⭐⭐</span>
        </div>

        <div className="review-card">
          <div className="avatar">🤖</div>

          <h3>Nova Bot</h3>

          <p>
            "Mission Complete! Thousands of learners have successfully
            upgraded their coding skills."
          </p>

          <span>⭐⭐⭐⭐⭐</span>
        </div>

      </div>

    </section>
  );
}

export default Testimonials;