import "./Learning.css";

function Learning() {

  const lessons = [
    { title: "Arrays", xp: 50, status: "completed" },
    { title: "Binary Search", xp: 60, status: "current" },
    { title: "Linked List", xp: 70, status: "available" },
    { title: "Stack", xp: 80, status: "locked" },
    { title: "Queue", xp: 80, status: "locked" },
    { title: "Tree", xp: 100, status: "locked" },
    { title: "Graph", xp: 120, status: "locked" },
    { title: "Dynamic Programming", xp: 150, status: "locked" }
  ];

  return (
    <div className="learning-page">

      <h1>📚 Algolingo Learning Path</h1>

      <p className="subtitle">
        Complete lessons to unlock the next topic.
      </p>

      <div className="roadmap">

        {lessons.map((lesson, index) => (

          <div className="lesson-container" key={index}>

            <div className={`lesson-circle ${lesson.status}`}>

              {lesson.status === "completed" && "✅"}

              {lesson.status === "current" && "▶"}

              {lesson.status === "available" && "📘"}

              {lesson.status === "locked" && "🔒"}

            </div>

            <h3>{lesson.title}</h3>

            <p>⭐ {lesson.xp} XP</p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Learning;