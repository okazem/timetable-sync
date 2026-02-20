import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [baseDate, setBaseDate] = useState(null);
  const [dates, setDates] = useState([]);

  useEffect(() => {
    const today = new Date();
    const dayOfWeek = today.getDay();
    const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
    const monday = new Date(today);
    monday.setDate(today.getDate() + diffToMonday);
    monday.setHours(0, 0, 0, 0);
    setBaseDate(monday);
  }, []);

  useEffect(() => {
    if (!baseDate) return;
    const newDates = Array.from({ length: 5 }).map((_, i) => {
      const d = new Date(baseDate);
      d.setDate(baseDate.getDate() + i);
      return `${d.getMonth() + 1}/${d.getDate()}`;
    });
    setDates(newDates);
  }, [baseDate]);

  if (!baseDate) return null;

  return (
    <div className="page-wrapper">
      <div className="container-stack">
        <div className="grid-container">
          {/* 1行目 */}
          {dates.map((date, i) => (
            <div key={`h-${i}`} className="grid-cell header-cell">{date}</div>
          ))}

          {/* 2行目以降（フラットに展開することでズレを防止） */}
          {Array.from({ length: 25 }).map((_, i) => (
            <div key={`c-${i}`} className="grid-cell content-cell">
              {i === 0 && <span className="subject-tag">代数</span>}
            </div>
          ))}
        </div>

        <div className="button-group">
          <button className="nav-btn" onClick={() => setBaseDate(new Date(baseDate.setDate(baseDate.getDate() - 7)))}>先週</button>
          <button className="nav-btn" onClick={() => setBaseDate(new Date(baseDate.setDate(baseDate.getDate() + 7)))}>次週</button>
        </div>
      </div>
    </div>
  )
}

export default App