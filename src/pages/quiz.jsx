import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Quiz.css";

function Quiz() {

  const navigate = useNavigate();

  const questions = [
    {
      question: "What is the time complexity of Binary Search?",
      options: ["O(n)", "O(log n)", "O(n²)", "O(1)"],
      answer: "O(log n)",
    },
    {
      question: "Which data structure follows FIFO?",
      options: ["Stack", "Queue", "Tree", "Graph"],
      answer: "Queue",
    },
    {
      question: "Which data structure follows LIFO?",
      options: ["Queue", "Tree", "Stack", "Graph"],
      answer: "Stack",
    },
    {
      question: "Which traversal visits Root first?",
      options: ["Inorder", "Preorder", "Postorder", "Level Order"],
      answer: "Preorder",
    },
    {
      question: "Which algorithm is used to find the shortest path?",
      options: [
        "Bubble Sort",
        "Binary Search",
        "Dijkstra",
        "Merge Sort",
      ],
      answer: "Dijkstra",
    },
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selected, setSelected] = useState("");
  const [score, setScore] = useState(0);

  const handleNext = () => {

    if (selected === "") {
      alert("Please select an answer.");
      return;
    }

    if (selected === questions[currentQuestion].answer) {
      setScore(score + 1);
    }

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
      setSelected("");
    } else {
      navigate("/result", {
        state: {
          score:
            selected === questions[currentQuestion].answer
              ? score + 1
              : score,
          total: questions.length,
        },
      });
    }
  };

  return (
    <div className="quiz-page">

      <div className="quiz-card">

        <h1>📝 Quiz Time</h1>

        <h2>
          Question {currentQuestion + 1} of {questions.length}
        </h2>

        <p className="question">
          {questions[currentQuestion].question}
        </p>

        {questions[currentQuestion].options.map((option) => (
          <button
            key={option}
            className={`option ${
              selected === option ? "selected" : ""
            }`}
            onClick={() => setSelected(option)}
          >
            {option}
          </button>
        ))}

        <button className="next-btn" onClick={handleNext}>
          Next Question →
        </button>

      </div>

    </div>
  );
}

export default Quiz;