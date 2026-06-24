// import React, { useState } from "react";
// import styles from "./ChatPanel.module.css";
// import { LuSend } from "react-icons/lu";
// import { IoMicSharp } from "react-icons/io5";
// import { IoMicOffSharp } from "react-icons/io5";
// import { TbMessageChatbot } from "react-icons/tb";
// import { FaUser } from "react-icons/fa";

// function ChatPanel({ messages, onSendMessage, isListening, onToggleVoice }) {
//   const [inputValue, setInputValue] = useState("");

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     onSendMessage(inputValue);
//     setInputValue("");
//   };

//   return (
//     <div className={styles.panel}>
//       <div className={styles.panelHeader}>
//         <span>Live Chat</span>
//         <button
//           type="button"
//           onClick={onToggleVoice}
//           className={`${styles.voiceBtn} ${isListening ? styles.activeVoice : ""}`}
//         >
//           {isListening ? <IoMicSharp /> : <IoMicOffSharp />}
//         </button>
//       </div>

//       <div className={styles.chatArea}>
//         {messages.map((msg) => (
//           <div
//             key={msg.id}
//             className={`${styles.messageRow} ${msg.sender === "user" ? styles.userRow : styles.agentRow}`}
//           >
//             {msg.sender === "agent" && (
//               <div className={`${styles.avatar} ${styles.agentAvatar}`}>
//                 <TbMessageChatbot />
//               </div>
//             )}
//             <div className={styles.bubble}>{msg.text}</div>
//             {msg.sender === "user" && (
//               <div className={`${styles.avatar} ${styles.userAvatar}`}>
//                 <FaUser />
//               </div>
//             )}
//           </div>
//         ))}
//       </div>

//       <form onSubmit={handleSubmit} className={styles.inputArea}>
//         <input
//           type="text"
//           value={inputValue}
//           onChange={(e) => setInputValue(e.target.value)}
//           placeholder="Type your message..."
//           className={styles.input}
//         />
//         <button type="submit" className={styles.sendBtn}>
//           <LuSend />
//         </button>
//       </form>
//     </div>
//   );
// }

// export default ChatPanel;

// import React, { useState, useEffect } from "react";
// import styles from "./ChatPanel.module.css";
// import { LuSend } from "react-icons/lu";
// import { IoMicSharp, IoMicOffSharp } from "react-icons/io5";
// import { TbMessageChatbot } from "react-icons/tb";
// import { FaUser } from "react-icons/fa";
// import { Room, RoomEvent } from "livekit-client";

// function ChatPanel({
//   messages,
//   setMessages,
//   onSendMessage,
//   isListening,
//   onToggleVoice,
// }) {
//   const [inputValue, setInputValue] = useState("");
//   const [roomConnected, setRoomConnected] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!inputValue.trim()) return;

//     const userText = inputValue;
//     setInputValue("");

//     // 1. ROUTE TO APP.JSX VIA HTTP STREAM (Ensures AdminPanel logs get populated)
//     onSendMessage(userText);

//     // 2. ROUTE TO WEBRTC LIVEKIT DATA CHANNEL (Only if connected)
//     if (window.currentVoiceRoom && roomConnected) {
//       try {
//         const encoder = new TextEncoder();
//         const data = encoder.encode(JSON.stringify({ text: userText }));

//         // Publish text down the data track using the default LiveKit chat channel
//         await window.currentVoiceRoom.localParticipant.publishData(data, {
//           topic: "lk.chat",
//         });
//         console.log(
//           "[LiveKit Chat] Message synchronized to voice room session.",
//         );
//       } catch (err) {
//         console.error("Failed to broadcast text track over LiveKit:", err);
//       }
//     }
//   };

//   const handleVoiceClick = async () => {
//     if (!isListening) {
//       try {
//         const res = await fetch(
//           "http://127.0.0.1:8000/api/voice-token?room=refund-room",
//         );
//         const data = await res.json();

//         const room = new Room();

//         // Setup data channel packet stream listeners before initializing connection
//         room.on(RoomEvent.DataReceived, (payload, participant) => {
//           try {
//             const decoder = new TextDecoder();
//             const rawJson = JSON.parse(decoder.decode(payload));

//             if (rawJson.text) {
//               // Safety filter: instantly drop technical backend records or tool data logs
//               const isTechnicalLog =
//                 rawJson.text.includes("crm_lookup") ||
//                 rawJson.text.includes("rag_tool") ||
//                 rawJson.text.includes("{") ||
//                 rawJson.text.includes("Document");

//               if (isTechnicalLog) return;

//               // FIX: Check if the incoming packet came from yourself or the background worker agent
//               const isMe =
//                 participant?.identity === room.localParticipant.identity;

//               const agentMsg = {
//                 id: Math.random().toString(),
//                 sender: isMe ? "user" : "agent", // Properly tracks the remote agent response block
//                 text: rawJson.text,
//               };

//               if (setMessages) {
//                 setMessages((prev) => [...prev, agentMsg]);
//               }
//             }
//           } catch (err) {
//             console.error("Error unpacking incoming data channel frame:", err);
//           }
//         });

//         await room.connect("wss://samvaad-0o3lw0w1.livekit.cloud", data.token);
//         await room.localParticipant.setMicrophoneEnabled(true);

//         window.currentVoiceRoom = room;
//         setRoomConnected(true);
//         onToggleVoice();
//         console.log("[LiveKit] Room connection initialized successfully.");
//       } catch (error) {
//         console.error("Failed to connect to LiveKit room:", error);
//       }
//     } else {
//       if (window.currentVoiceRoom) {
//         window.currentVoiceRoom.disconnect();
//       }
//       window.currentVoiceRoom = null;
//       setRoomConnected(false);
//       onToggleVoice();
//     }
//   };

//   return (
//     <div className={styles.panel}>
//       <div className={styles.panelHeader}>
//         <span>Live Assistant Chat & Voice</span>
//         <button
//           type="button"
//           onClick={handleVoiceClick}
//           className={`${styles.voiceBtn} ${isListening ? styles.activeVoice : ""}`}
//         >
//           {isListening ? <IoMicSharp /> : <IoMicOffSharp />}
//         </button>
//       </div>

//       <div className={styles.chatArea}>
//         {messages.map((msg) => (
//           <div
//             key={msg.id}
//             className={`${styles.messageRow} ${msg.sender === "user" ? styles.userRow : styles.agentRow}`}
//           >
//             {msg.sender === "agent" && (
//               <div className={`${styles.avatar} ${styles.agentAvatar}`}>
//                 <TbMessageChatbot />
//               </div>
//             )}
//             <div className={styles.bubble}>{msg.text}</div>
//             {msg.sender === "user" && (
//               <div className={`${styles.avatar} ${styles.userAvatar}`}>
//                 <FaUser />
//               </div>
//             )}
//           </div>
//         ))}
//       </div>

//       <form onSubmit={handleSubmit} className={styles.inputArea}>
//         <input
//           type="text"
//           value={inputValue}
//           onChange={(e) => setInputValue(e.target.value)}
//           placeholder={
//             roomConnected
//               ? "Type here or talk seamlessly..."
//               : "Click mic to connect assistant room..."
//           }
//           className={styles.input}
//         />
//         <button type="submit" className={styles.sendBtn}>
//           <LuSend />
//         </button>
//       </form>
//     </div>
//   );
// }

// export default ChatPanel;








import React, { useState, useEffect } from "react";
import styles from "./ChatPanel.module.css";
import { LuSend } from "react-icons/lu";
import { IoMicSharp, IoMicOffSharp } from "react-icons/io5";
import { TbMessageChatbot } from "react-icons/tb";
import { FaUser } from "react-icons/fa";
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useRoomContext,
} from "@livekit/components-react";
import "@livekit/components-styles";
import Markdown from "react-markdown"

// 1. ISOLATED COMPONENT TO HANDLE DATA CHANNEL EVENTS SAFELY
function LiveKitDataSubscriber({ setMessages, setRoomConnected }) {
  const room = useRoomContext();

  useEffect(() => {
    if (!room) return;

    // Cache instance globally for the text send handler
    window.currentVoiceRoom = room;
    setRoomConnected(true);

    const handleDataReceived = (payload, participant) => {
      try {
        const decoder = new TextDecoder();
        const rawJson = JSON.parse(decoder.decode(payload));

        if (rawJson.text) {
          const isTechnicalLog =
            rawJson.text.includes("crm_lookup") ||
            rawJson.text.includes("rag_tool") ||
            rawJson.text.includes("{") ||
            rawJson.text.includes("Document");

          if (isTechnicalLog) return;

          const isMe = participant?.identity === room.localParticipant.identity;

          const agentMsg = {
            id: Math.random().toString(),
            sender: isMe ? "user" : "agent",
            text: rawJson.text,
          };

          if (setMessages) {
            setMessages((prev) => [...prev, agentMsg]);
          }
        }
      } catch (err) {
        console.error("Error unpacking incoming data channel frame:", err);
      }
    };

    room.on("dataReceived", handleDataReceived);
    console.log(
      "[LiveKit Room] Audio and Data track pipeline attached successfully.",
    );

    return () => {
      room.off("dataReceived", handleDataReceived);
      window.currentVoiceRoom = null;
      setRoomConnected(false);
    };
  }, [room, setMessages, setRoomConnected]);

  return null;
}

// 2. MAIN CHAT PANEL COMPONENT
function ChatPanel({
  messages,
  setMessages,
  onSendMessage,
  isListening,
  onToggleVoice,
}) {
  const [inputValue, setInputValue] = useState("");
  const [token, setToken] = useState(null);
  const [roomConnected, setRoomConnected] = useState(false);

  const LIVEKIT_URL = "wss://samvaad-0o3lw0w1.livekit.cloud";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userText = inputValue;
    setInputValue("");

    onSendMessage(userText);

    if (window.currentVoiceRoom && roomConnected) {
      try {
        const encoder = new TextEncoder();
        const data = encoder.encode(JSON.stringify({ text: userText }));

        await window.currentVoiceRoom.localParticipant.publishData(data, {
          topic: "lk.chat",
        });
        console.log(
          "[LiveKit Chat] Message synchronized to voice room session.",
        );
      } catch (err) {
        console.error("Failed to broadcast text track over LiveKit:", err);
      }
    }
  };

  const handleVoiceClick = async () => {
    if (!isListening) {
      try {
        const res = await fetch(
          "http://127.0.0.1:8000/api/voice-token?room=refund-room",
        );
        const data = await res.json();
        setToken(data.token);
        onToggleVoice();
      } catch (error) {
        console.error("Failed to fetch LiveKit voice room token:", error);
      }
    } else {
      setToken(null);
      setRoomConnected(false);
      window.currentVoiceRoom = null;
      onToggleVoice();
    }
  };

  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>
        <span>Live Assistant Chat & Voice</span>
        <button
          type="button"
          onClick={handleVoiceClick}
          className={`${styles.voiceBtn} ${isListening ? styles.activeVoice : ""}`}
        >
          {isListening ? <IoMicSharp /> : <IoMicOffSharp />}
        </button>
      </div>

      {isListening && token && (
        <LiveKitRoom
          key={token}
          serverUrl={LIVEKIT_URL}
          token={token}
          connect={true}
          audio={true}
          onDisconnected={() => {
            setToken(null);
            setRoomConnected(false);
            window.currentVoiceRoom = null;
          }}
        >
          <RoomAudioRenderer />
          {/* Internal context subscriber to safely bind 'dataReceived' */}
          <LiveKitDataSubscriber
            setMessages={setMessages}
            setRoomConnected={setRoomConnected}
          />
        </LiveKitRoom>
      )}

      <div className={styles.chatArea}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.messageRow} ${msg.sender === "user" ? styles.userRow : styles.agentRow}`}
          >
            {msg.sender === "agent" && (
              <div className={`${styles.avatar} ${styles.agentAvatar}`}>
                <TbMessageChatbot />
              </div>
            )}
            <div className={styles.bubble}>
              <Markdown>{msg.text}</Markdown>
            </div>
            {msg.sender === "user" && (
              <div className={`${styles.avatar} ${styles.userAvatar}`}>
                <FaUser />
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className={styles.inputArea}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={
            roomConnected
              ? "Type here or talk seamlessly..."
              : "Click mic to connect assistant room..."
          }
          className={styles.input}
        />
        <button type="submit" className={styles.sendBtn}>
          <LuSend />
        </button>
      </form>
    </div>
  );
}

export default ChatPanel;