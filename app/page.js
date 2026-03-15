"use client";
import { useState, useRef, useEffect } from "react";

const LANGUAGES = [
  { code: "en", name: "İngilizce", flag: "🇬🇧" },
  { code: "de", name: "Almanca", flag: "🇩🇪" },
  { code: "fr", name: "Fransızca", flag: "🇫🇷" },
  { code: "es", name: "İspanyolca", flag: "🇪🇸" },
  { code: "it", name: "İtalyanca", flag: "🇮🇹" },
  { code: "ru", name: "Rusça", flag: "🇷🇺" },
  { code: "ja", name: "Japonca", flag: "🇯🇵" },
  { code: "zh", name: "Çince", flag: "🇨🇳" },
];

const LEVELS = [
  { id: "A1", label: "Başlangıç", color: "#4ade80" },
  { id: "B1", label: "Orta", color: "#facc15" },
  { id: "C1", label: "İleri", color: "#f87171" },
];

const MODES = [
  { id: "chat", icon: "💬", label: "Sohbet" },
  { id: "quiz", icon: "🧠", label: "Quiz" },
  { id: "translate", icon: "🔄", label: "Çeviri" },
  { id: "grammar", icon: "📖", label: "Gramer" },
];

export default function Home() {
  const [screen, setScreen] = useState("home");
  const [selectedLang, setSelectedLang] = useState(null);
  const [selectedLevel, setSelectedLevel] = useState("A1");
  const [selectedMode, setSelectedMode] = useState("chat");
  const [apiHistory, setApiHistory] = useState([]);
  const [displayMessages, setDisplayMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [xp, setXp] = useState(0);
  const [streak] = useState(3);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [displayMessages]);

  const getSystemPrompt = () => {
    const lang = LANGUAGES.find((l) => l.code === selectedLang);
    const level = LEVELS.find((l) => l.id === selectedLevel);
    const modeInstructions = {
      chat: `Kullanıcıyla ${lang?.name} üzerinde sohbet et. Her mesajda 1-2 yeni kelime öğret, hataları nazikçe düzelt.`,
      quiz: `Kullanıcıya ${lang?.name} dil quizleri yap. Seviyeye uygun sorular sor, doğru cevaplarda tebrik et.`,
      translate: `Kullanıcının verdiği Türkçe cümleleri ${lang?.name} diline çevir ve açıkla.`,
      grammar: `${lang?.name} grameri öğret. Kural açıkla, örnek ver, alıştırma yaptır.`,
    };
    return `Sen LinguaAI adlı bir dil öğrenme asistanısın. Kullanıcı ${lang?.name} öğreniyor, seviyesi ${level?.label} (${level?.id}). ${modeInstructions[selectedMode]} Yanıtların kısa, samimi ve teşvik edici olsun.`;
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userText = input;
    setInput("");
    setLoading(true);

    const newDisplay = [...displayMessages, { role: "user", content: userText }];
    setDisplayMessages(newDisplay);
    const newApiHistory = [...apiHistory, { role: "user", content: userText }];

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ system: getSystemPrompt(), messages: newApiHistory }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setDisplayMessages([...newDisplay, { role: "assistant", content: data.reply }]);
      setApiHistory([...newApiHistory, { role: "assistant", content: data.reply }]);
      setXp((x) => x + 10);
    } catch (err) {
      setDisplayMessages([...newDisplay, { role: "assistant", content: `⚠️ ${err.message}` }]);
      setApiHistory(newApiHistory);
    }
    setLoading(false);
  };

  const startApp = () => {
    if (!selectedLang) return;
    const lang = LANGUAGES.find((l) => l.code === selectedLang);
    const level = LEVELS.find((l) => l.id === selectedLevel);
    const mode = MODES.find((m) => m.id === selectedMode);
    setApiHistory([]);
    setDisplayMessages([{
      role: "assistant",
      content: `Merhaba! ${lang?.flag} ${lang?.name} öğrenmeye hoş geldin!\nSeviye: ${level?.label} · Mod: ${mode?.label}\n\nHazır olduğunda yaz, başlayalım! 🚀`,
    }]);
    setScreen("app");
  };

  if (screen === "home") {
    return (
      <div style={s.root}>
        <div style={s.bg} />
        <div style={s.homeWrap}>
          <div style={s.logo}>
            <div style={{ fontSize: 44 }}>🌍</div>
            <h1 style={s.logoText}>LinguaAI</h1>
            <p style={s.logoSub}>Yapay Zeka Destekli Dil Öğrenme</p>
          </div>

          <div style={s.card}>
            <p style={s.label}>Dil Seç</p>
            <div style={s.langGrid}>
              {LANGUAGES.map((l) => (
                <button key={l.code} onClick={() => setSelectedLang(l.code)}
                  style={{ ...s.langBtn, ...(selectedLang === l.code ? s.langActive : {}) }}>
                  <span style={{ fontSize: 22 }}>{l.flag}</span>
                  <span style={s.langName}>{l.name}</span>
                </button>
              ))}
            </div>

            <p style={s.label}>Seviye</p>
            <div style={s.row}>
              {LEVELS.map((l) => (
                <button key={l.id} onClick={() => setSelectedLevel(l.id)}
                  style={{ ...s.levelBtn, borderColor: selectedLevel === l.id ? l.color : "transparent", color: selectedLevel === l.id ? l.color : "#666", background: selectedLevel === l.id ? l.color + "18" : "#111" }}>
                  {l.id} · {l.label}
                </button>
              ))}
            </div>

            <p style={s.label}>Mod</p>
            <div style={s.row}>
              {MODES.map((m) => (
                <button key={m.id} onClick={() => setSelectedMode(m.id)}
                  style={{ ...s.modeBtn, ...(selectedMode === m.id ? s.modeActive : {}) }}>
                  <span style={{ fontSize: 18 }}>{m.icon}</span>
                  <span style={{ fontSize: 11 }}>{m.label}</span>
                </button>
              ))}
            </div>

            <button onClick={startApp} disabled={!selectedLang}
              style={{ ...s.startBtn, opacity: selectedLang ? 1 : 0.35, cursor: selectedLang ? "pointer" : "not-allowed" }}>
              Öğrenmeye Başla →
            </button>
          </div>

          <div style={s.statsRow}>
            <div style={s.stat}>🔥 {streak} Gün</div>
            <div style={s.stat}>⭐ {xp} XP</div>
            <div style={s.stat}>🏆 Lv.1</div>
          </div>
        </div>
      </div>
    );
  }

  const lang = LANGUAGES.find((l) => l.code === selectedLang);
  const mode = MODES.find((m) => m.id === selectedMode);

  return (
    <div style={s.root}>
      <div style={s.bg} />
      <div style={s.chatWrap}>
        <div style={s.header}>
          <button onClick={() => setScreen("home")} style={s.backBtn}>←</button>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flex: 1 }}>
            <span style={{ fontSize: 22 }}>{lang?.flag}</span>
            <div>
              <div style={s.headerTitle}>{lang?.name}</div>
              <div style={s.headerSub}>{mode?.icon} {mode?.label} · {selectedLevel}</div>
            </div>
          </div>
          <div style={s.xpBadge}>⭐ {xp} XP</div>
        </div>

        <div style={s.messages}>
          {displayMessages.map((msg, i) => (
            <div key={i} style={{ ...s.bubbleWrap, ...(msg.role === "user" ? s.bubbleWrapUser : {}) }}>
              {msg.role === "assistant" && <div style={s.avatar}>🤖</div>}
              <div style={{ ...s.bubble, ...(msg.role === "user" ? s.bubbleUser : s.bubbleAI) }}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div style={s.bubbleWrap}>
              <div style={s.avatar}>🤖</div>
              <div style={{ ...s.bubble, ...s.bubbleAI, padding: "14px 16px" }}>
                <div style={{ display: "flex", gap: 4 }}>
                  {[0, 0.2, 0.4].map((d, i) => (
                    <span key={i} style={{ ...s.dot, animationDelay: `${d}s` }} />
                  ))}
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div style={s.inputRow}>
          <input value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Mesajını yaz..." style={s.input} />
          <button onClick={sendMessage} disabled={loading} style={s.sendBtn}>➤</button>
        </div>
      </div>
      <style>{`@keyframes bounce{0%,80%,100%{transform:scale(0)}40%{transform:scale(1)}}`}</style>
    </div>
  );
}

const s = {
  root: { minHeight: "100vh", background: "#09090f", display: "flex", alignItems: "center", justifyContent: "center", padding: 16, position: "relative", overflow: "hidden", fontFamily: "system-ui, sans-serif" },
  bg: { position: "fixed", inset: 0, background: "radial-gradient(ellipse at 15% 15%, #1e0a4a 0%, transparent 55%), radial-gradient(ellipse at 85% 85%, #082a18 0%, transparent 55%)", zIndex: 0 },
  homeWrap: { position: "relative", zIndex: 1, width: "100%", maxWidth: 460, display: "flex", flexDirection: "column", gap: 18 },
  logo: { textAlign: "center" },
  logoText: { fontSize: 34, fontWeight: 700, background: "linear-gradient(135deg,#b794f4,#38d9a9)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", margin: 0 },
  logoSub: { color: "#555", fontSize: 13, marginTop: 4 },
  card: { background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 20, padding: 22, display: "flex", flexDirection: "column", gap: 14 },
  label: { color: "#666", fontSize: 10, fontWeight: 600, letterSpacing: "0.12em", textTransform: "uppercase", margin: 0 },
  langGrid: { display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 7 },
  langBtn: { background: "#111", border: "1.5px solid transparent", borderRadius: 11, padding: "9px 4px", cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", gap: 4 },
  langActive: { border: "1.5px solid #b794f4", background: "#b794f420" },
  langName: { color: "#bbb", fontSize: 9 },
  row: { display: "flex", gap: 7 },
  levelBtn: { flex: 1, padding: "9px 4px", borderRadius: 10, border: "1.5px solid", fontSize: 11, fontWeight: 600, cursor: "pointer" },
  modeBtn: { flex: 1, padding: "9px 4px", borderRadius: 10, background: "#111", border: "1.5px solid transparent", color: "#666", fontSize: 11, cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", gap: 3 },
  modeActive: { border: "1.5px solid #38d9a9", background: "#38d9a918", color: "#38d9a9" },
  startBtn: { background: "linear-gradient(135deg,#b794f4,#38d9a9)", color: "#000", border: "none", borderRadius: 13, padding: 13, fontSize: 15, fontWeight: 700 },
  statsRow: { display: "flex", gap: 7 },
  stat: { flex: 1, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 11, padding: "9px 4px", color: "#999", fontSize: 11, textAlign: "center", fontWeight: 600 },
  chatWrap: { position: "relative", zIndex: 1, width: "100%", maxWidth: 460, height: "88vh", display: "flex", flexDirection: "column", background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 22, overflow: "hidden" },
  header: { padding: "14px 18px", borderBottom: "1px solid rgba(255,255,255,0.05)", display: "flex", alignItems: "center", gap: 10 },
  backBtn: { background: "rgba(255,255,255,0.05)", border: "none", color: "#fff", fontSize: 17, width: 34, height: 34, borderRadius: 9, cursor: "pointer" },
  headerTitle: { color: "#fff", fontWeight: 700, fontSize: 14 },
  headerSub: { color: "#555", fontSize: 10 },
  xpBadge: { background: "rgba(183,148,244,0.12)", color: "#b794f4", borderRadius: 9, padding: "5px 11px", fontSize: 11, fontWeight: 700 },
  messages: { flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 10 },
  bubbleWrap: { display: "flex", alignItems: "flex-start", gap: 7, maxWidth: "83%" },
  bubbleWrapUser: { alignSelf: "flex-end", flexDirection: "row-reverse" },
  avatar: { width: 30, height: 30, borderRadius: 9, background: "rgba(183,148,244,0.12)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, flexShrink: 0 },
  bubble: { borderRadius: 14, padding: "9px 13px", fontSize: 13, lineHeight: 1.6, whiteSpace: "pre-wrap" },
  bubbleAI: { background: "rgba(255,255,255,0.05)", color: "#ccc", borderRadius: "3px 14px 14px 14px" },
  bubbleUser: { background: "linear-gradient(135deg,#b794f430,#38d9a930)", color: "#eee", borderRadius: "14px 3px 14px 14px" },
  dot: { width: 7, height: 7, borderRadius: "50%", background: "#b794f4", animation: "bounce 1.4s infinite", display: "inline-block" },
  inputRow: { padding: "11px 14px", borderTop: "1px solid rgba(255,255,255,0.05)", display: "flex", gap: 7 },
  input: { flex: 1, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 13, padding: "11px 14px", color: "#fff", fontSize: 13, outline: "none" },
  sendBtn: { background: "linear-gradient(135deg,#b794f4,#38d9a9)", border: "none", borderRadius: 13, width: 44, height: 44, fontSize: 16, cursor: "pointer", color: "#000", fontWeight: 700 },
};
