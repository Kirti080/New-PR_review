"""Inject malformed records into local task storage, or restore its backup."""

import argparse
import json
import os
from pathlib import Path


def run(action: str, data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    tasks = data_dir / "tasks.json"
    backup = data_dir / "tasks.chaos-backup.json"
    temporary = data_dir / "tasks.chaos.tmp"

    if action == "restore":
        if not backup.exists():
            raise ValueError("No chaos backup exists. Nothing was changed.")
        os.replace(backup, tasks)
        print("Original task data restored.")
        return

    if backup.exists():
        raise ValueError("A backup already exists. Run restore before injecting again.")

    original = tasks.read_bytes() if tasks.exists() else b"[]\n"
    records = json.loads(original)
    if not isinstance(records, list):
        raise ValueError("Expected a JSON list. Nothing was changed.")

    records.extend([
        None,
        42,
        "unexpected scalar task",
        [],
        {},
        {"id": "missing-done", "title": "Missing completion flag"},
        {"id": "wrong-done", "title": "String instead of boolean", "done": "yes"},
        {"id": ["wrong-id"], "title": "Array instead of ID", "done": False},
        {"id": "wrong-title", "title": {"unexpected": "object"}, "done": False},
        {"id": "empty-title", "title": "  ", "done": False},
    ])
    # Exclusive creation protects the recovery copy from repeated injections.
    with backup.open("xb") as handle:
        handle.write(original)
    try:
        temporary.write_text(json.dumps(records, indent=2), encoding="utf-8")
        os.replace(temporary, tasks)
    finally:
        temporary.unlink(missing_ok=True)
    print("Injected 10 malformed records. Valid tasks should still render normally.")
    print("Recovery: python tools/chaos.py restore")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inject", "restore"])
    args = parser.parse_args()
    try:
        run(args.action, Path(__file__).resolve().parents[1] / "data")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
















import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h2>{count}</h2>

      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>

      <button onClick={() => setCount(count - 1)}>
        Decrement
      </button>

      <button onClick={() => setCount(0)}>
        Reset
      </button>
    </div>
  );
}












function StudentList() {
  const students = ["Aman", "Priya", "Rahul"];

  return (
    <ul>
      {students.map((student, index) => (
        <li key={index}>{student}</li>
      ))}
    </ul> 
  );
}

export default StudentList;





import { useState } from "react";

function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <div>
      <p>{isDark ? "Dark Mode" : "Light Mode"}</p>

      <button onClick={() => setIsDark(!isDark)}>
        Toggle Mode
      </button>
    </div>
  );
}

export default App;


























import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

function App() {
  return (
    <div className="p-6">
      <Card>
        <CardHeader>
          <CardTitle>My First Card</CardTitle>
        </CardHeader>

        <CardContent>
          <p>This is a shadcn component.</p>

          <Button onClick={() => alert("Button clicked!")}>
            Click Me
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;











import { BrowserRouter, Routes, Route, Link } from "react-router";

function Home() {
  return <h1>Home Page</h1>;
}

function About() {
  return <h1>About Page</h1>;
}

function Dashboard() {
  return <h1>Dashboard Page</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>{" | "}
        <Link to="/about">About</Link>{" | "}
        <Link to="/dashboard">Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;













































import "./App.css";

const projects = [
  {
    title: "Portfolio Website",
    description: "A personal website built with React.",
    status: "Completed",
  },
  {
    title: "AI Chatbot",
    description: "A chatbot powered by an AI API.",
    status: "In Progress",
  },
  {
    title: "Student Dashboard",
    description: "A responsive dashboard for students.",
    status: "Completed",
  },
];

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <h2 className="logo">DevSpace</h2>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#projects">Projects</a>
          <a href="#about">About</a>
        </div>

        <button className="profile-button">My Profile</button>
      </nav>

      <main className="container" id="home">
        <section className="welcome">
          <p className="eyebrow">YOUR WORKSPACE</p>
          <h1>Welcome back!</h1>
          <p>
            Manage your projects and track your progress.
          </p>
        </section>

        <section className="stats">
          <div className="stat-card">
            <span>Total Projects</span>
            <h2>12</h2>
          </div>

          <div className="stat-card">
            <span>Completed</span>
            <h2>8</h2>
          </div>

          <div className="stat-card">
            <span>In Progress</span>
            <h2>4</h2>
          </div>
        </section>

        <section className="projects" id="projects">
          <h2>Recent Projects</h2>

          <div className="project-grid">
            {projects.map((project) => (
              <article
                className="project-card"
                key={project.title}
              >
                <h3>{project.title}</h3>
                <p>{project.description}</p>

                <span
                  className={`status ${
                    project.status === "Completed"
                      ? "completed"
                      : "in-progress"
                  }`}
                >
                  {project.status}
                </span>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;






