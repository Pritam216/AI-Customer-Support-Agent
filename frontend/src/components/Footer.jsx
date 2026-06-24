import React from "react";
import styles from "./Footer.module.css";

function Footer() {
  return (
    <footer className={styles.footer}>
      <span>Status: Active</span>
      <span className={styles.divider}>|</span>
      <span>Connected</span>
      <span className={styles.divider}>|</span>
      <span>Policy Version: 3.1</span>
    </footer>
  );
}

export default Footer;
