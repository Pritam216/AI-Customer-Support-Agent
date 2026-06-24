import React from "react";
import styles from "./OrderBar.module.css";

function OrderBar({ onNewChat, currentOrder }) {
  return (
    <div className={styles.orderBar}>
      <span>Active Session ID: {currentOrder}</span>
      <button onClick={onNewChat} className={styles.newChatBtn}>
        New Chat
      </button>
    </div>
  );
}

export default OrderBar;
