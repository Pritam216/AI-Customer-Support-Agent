import React, { useState } from "react";
import styles from "./App.module.css";
import Header from "./components/Header";
import OrderBar from "./components/OrderBar";
import ChatPanel from "./components/ChatPanel";
import AdminPanel from "./components/AdminPanel";
import Footer from "./components/Footer";

function App() {
  const [currentOrder, setCurrentOrder] = useState(() => crypto.randomUUID());
  // const [messages, setMessages] = useState([]);
  const [logs, setLogs] = useState([]);
  const [tools, setTools] = useState([]);
  const [isListening, setIsListening] = useState(false);

  const now = new Date();

  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");

  const [messages, setMessages] = useState([]);
  // const [isListening, setIsListening] = useState(false);

  // Fallback for regular text chat if Voice isn't activated yet
  // const handleSendMessage = async (text) => {
  //   // If the LiveKit room is active, ChatPanel will broadcast it via WebRTC instead of hitting this REST endpoint.
  //   console.log("Fallback HTTP message dispatch:", text);
  // };

  const handleNewChat = () => {
    // 1. Generate a new unique identifier
    const newChatId = crypto.randomUUID()

    // 2. Update the chat identifier state
    setCurrentOrder(newChatId);

    // 3. Reset messages back to the initial agent welcome message
    setMessages([
      {
        id: String(Date.now()),
        sender: "agent",
        text: "Hello! I am your refund assistant. How can I help you today?",
      },
    ]);

    // 4. Optional: Clear out logs from the previous session
    setLogs([]);
  };

  const handleToggleVoice = () => {
    setIsListening((prev) => !prev);
  };

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: "user", text, avatar: "PK" },
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          thread_id: `user-${currentOrder}`,
        }),
      });

      if (!response.ok) throw new Error("Network error");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const rawJson = line.replace("data: ", "").trim();
            if (!rawJson) continue;

            let parsed;
            try {
              parsed = JSON.parse(rawJson);
            } catch {
              continue;
            }

            if (parsed.type === "info") {
              setLogs((prev) => [
                ...prev,
                {
                  id: Date.now(),
                  step: parsed.message,
                  status: "Received",
                  variant: "success",
                  time: `${hours}:${minutes}:${seconds}`,
                },
              ]);
            } else if (parsed.type === "event") {
              let statusText = "Processing...";
              let cleanStep = "Graph Update";

              if (parsed.data.includes("crm_lookup")) {
                cleanStep = "Tool Call: crm_lookup()";
                statusText = "Checking database";
              } else if (parsed.data.includes("rag_tool")) {
                cleanStep = "Tool Call: rag_tool()";
                statusText = "Checking refund rules";
              } else if (parsed.data.includes("chatbot")) {
                cleanStep = "Agent Thinking";
                statusText = "Evaluating policy";
              }

              setLogs((prev) => [
                ...prev,
                {
                  id: Math.random(),
                  step: cleanStep,
                  status: statusText,
                  variant: "warning",
                  time: `${hours}:${minutes}:${seconds}`,
                },
              ]);
            } else if (parsed.type === "final") {
              setMessages((prev) => [
                ...prev,
                {
                  id: Date.now(),
                  sender: "agent",
                  text: parsed.message,
                },
              ]);

              // Add tool execution logs first
              if (parsed.tools?.length) {
                const toolLogs = parsed.tools.map((tool, index) => ({
                  id: `${Date.now()}-${index}`,
                  step: `Tool: ${tool}`,
                  status: "Executed",
                  variant: "success",
                  time: `${hours}:${minutes}:${seconds}`,
                }));

                setLogs((prev) => [
                  ...prev,
                  ...toolLogs,
                  {
                    id: Date.now(),
                    step: "Execution Completed",
                    status: "Done",
                    variant: "success",
                    time: `${hours}:${minutes}:${seconds}`,
                  },
                ]);
              } else {
                setLogs((prev) => [
                  ...prev,
                  {
                    id: Date.now(),
                    step: "Execution Completed",
                    status: "Done",
                    variant: "success",
                    time: `${hours}:${minutes}:${seconds}`,
                  },
                ]);
              }
            }
          }
        }
      }
    } catch (error) {
      setLogs((prev) => [
        ...prev,
        {
          id: Date.now(),
          step: "Streaming Error",
          status: "Failed",
          variant: "warning",
          time: `${hours}:${minutes}:${seconds}`,
        },
      ]);
    }
  };

  // const handleToggleVoice = () => {
  //   setIsListening(!isListening);
  // };

  const handleOverrideApproval = () => {
    setLogs((prev) => [
      ...prev,
      {
        id: Date.now(),
        step: "Manual Override",
        status: "Approved by Admin",
        variant: "success",
        time: `${hours}:${minutes}:${seconds}`,
      },
    ]);
  };

  return (
    <div className={styles.appContainer}>
      <div className={styles.windowFrame}>
        <div className={styles.windowHeader}>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
        </div>

        <Header />
        <OrderBar onNewChat={handleNewChat} currentOrder={currentOrder} />

        <div className={styles.mainContent}>
          <ChatPanel
            messages={messages}
            setMessages={setMessages}
            onSendMessage={handleSendMessage}
            isListening={isListening}
            onToggleVoice={handleToggleVoice}
          />
          <AdminPanel
            logs={logs}
            tools={tools}
            onOverride={handleOverrideApproval}
          />
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default App;
