import React from "react";
import styles from "./Header.module.css";

function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>AI Customer Support Agent</h1>
    </header>
  );
}

export default Header;
