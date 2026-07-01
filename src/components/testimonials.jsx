import "./Testimonials.css";

function Testimonials() {
  return (
    <section className="testimonials">
      <h2>What Our Learners Say</h2>

      <div className="testimonial-container">

        <div className="testimonial-card">
          <div className="profile">👩‍🎓</div>
          <h3>Priya Sharma</h3>
          <p className="stars">⭐⭐⭐⭐⭐</p>
          <p>
            Algolingo made learning DSA easy and enjoyable. The quizzes helped
            me prepare for coding interviews.
          </p>
        </div>

        <div className="testimonial-card">
          <div className="profile">👨‍💻</div>
          <h3>Rahul Verma</h3>
          <p className="stars">⭐⭐⭐⭐⭐</p>
          <p>
            I loved the roadmap and XP system. It kept me motivated every day.
          </p>
        </div>

        <div className="testimonial-card">
          <div className="profile">👩‍💼</div>
          <h3>Ananya Gupta</h3>
          <p className="stars">⭐⭐⭐⭐⭐</p>
          <p>
            The interactive lessons are much better than reading long notes.
          </p>
        </div>

      </div>
    </section>
  );
}

export default Testimonials;