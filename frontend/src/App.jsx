import { useState } from 'react'
import './App.css'

function App() {
  // ■ 1. 時間割データを保存する「箱」 (例: { "MON-1": "線形代数", "TUE-3": "英語" })
  const [timetable, setTimetable] = useState({});

  // フォームの入力状態
  const [subject, setSubject] = useState("");
  const [day, setDay] = useState("MON");
  const [period, setPeriod] = useState(1);
  const [room, setRoom] = useState("");

  // 定数：曜日と時限のリスト
  const DAYS = ["MON", "TUE", "WED", "THU", "FRI"];
  const PERIODS = [1, 2, 3, 4, 5];

  // ■ 2. 「追加」ボタンを押した時の処理（画面の更新のみ）
  const handleAddClass = () => {
    if (!subject) {
      alert("科目名を入力してください");
      return;
    }

    // "MON-1" のようなキーを作る
    const key = `${day}-${period}`;

    // 時間割データを更新（前のデータ + 新しいデータ）
    setTimetable(prev => ({
      ...prev,
      [key]: { subject, room }
    }));

    // 入力欄をクリア
    setSubject("");
    setRoom("");
  };

  return (
    <div style={{ padding: "30px", maxWidth: "800px", margin: "0 auto", fontFamily: "sans-serif" }}>
      <h1>🎓 マイ時間割アプリ</h1>

      {/* --- 入力エリア --- */}
      <div style={{ 
        backgroundColor: "#f0f2f5", padding: "20px", borderRadius: "10px", marginBottom: "30px",
        display: "flex", flexWrap: "wrap", gap: "10px", alignItems: "flex-end"
      }}>
        <div>
          <label style={{display:"block", fontSize:"12px"}}>曜日</label>
          <select value={day} onChange={(e) => setDay(e.target.value)} style={{padding: "8px"}}>
            {DAYS.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        <div>
          <label style={{display:"block", fontSize:"12px"}}>時限</label>
          <select value={period} onChange={(e) => setPeriod(Number(e.target.value))} style={{padding: "8px"}}>
            {PERIODS.map(p => <option key={p} value={p}>{p}限</option>)}
          </select>
        </div>

        <div style={{flex: 1}}>
          <label style={{display:"block", fontSize:"12px"}}>科目名</label>
          <input 
            type="text" 
            value={subject} 
            onChange={(e) => setSubject(e.target.value)} 
            placeholder="例：線形代数"
            style={{padding: "8px", width: "100%", boxSizing: "border-box"}}
          />
        </div>

        <div style={{width: "120px"}}>
          <label style={{display:"block", fontSize:"12px"}}>教室</label>
          <input 
            type="text" 
            value={room} 
            onChange={(e) => setRoom(e.target.value)} 
            placeholder="301"
            style={{padding: "8px", width: "100%", boxSizing: "border-box"}}
          />
        </div>

        <button 
          onClick={handleAddClass}
          style={{padding: "10px 20px", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "5px", cursor: "pointer"}}
        >
          追加
        </button>
      </div>

      {/* --- 時間割表エリア --- */}
      <div style={{overflowX: "auto"}}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "center" }}>
          <thead>
            <tr style={{ backgroundColor: "#333", color: "white" }}>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>時限</th>
              {DAYS.map(d => (
                <th key={d} style={{ padding: "10px", border: "1px solid #ddd", width: "18%" }}>{d}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PERIODS.map(p => (
              <tr key={p}>
                {/* 左端の時限表示 (1限, 2限...) */}
                <td style={{ padding: "15px", backgroundColor: "#eee", border: "1px solid #ddd", fontWeight: "bold" }}>
                  {p}限
                </td>

                {/* 各曜日のセル */}
                {DAYS.map(d => {
                  const key = `${d}-${p}`;
                  const lesson = timetable[key]; // その曜日・時限に授業があるか探す

                  return (
                    <td key={key} style={{ padding: "10px", border: "1px solid #ddd", height: "80px", verticalAlign: "top" }}>
                      {lesson ? (
                        <div style={{ backgroundColor: "#e3f2fd", padding: "5px", borderRadius: "5px", height: "100%" }}>
                          <div style={{ fontWeight: "bold", color: "#1565c0" }}>{lesson.subject}</div>
                          <div style={{ fontSize: "12px", color: "#555" }}>{lesson.room}</div>
                        </div>
                      ) : (
                        <span style={{ color: "#ccc" }}>-</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App