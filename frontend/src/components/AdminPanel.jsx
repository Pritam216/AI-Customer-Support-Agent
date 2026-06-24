// import React from "react";
// import styles from "./AdminPanel.module.css";

// function AdminPanel({ logs, onOverride }) {
//   return (
//     <div className={styles.panel}>
//       <div className={styles.panelHeader}>Agent Decisions (Real-time Logs)</div>

//       <div className={styles.logContainer}>
//         {logs.map((log) => (
//           <div key={log.id} className={styles.logRow}>
//             <span className={styles.timeTag}>
//               [{log.time}]
//             </span>
//             <span className={styles.stepName}>{log.step}</span>
//             <span
//               className={`${styles.statusBadge} ${log.variant === "success" ? styles.success : styles.warning}`}
//             >
//               {log.variant === "success" ? "✓" : "⚠️"} {log.status}
//             </span>
//           </div>
//         ))}
//       </div>

//       <button type="button" onClick={onOverride} className={styles.overrideBtn}>
//         OVERRIDE APPROVAL (Human)
//       </button>
//     </div>
//   );
// }

// export default AdminPanel;

import React from "react";
import styles from "./AdminPanel.module.css";

function AdminPanel({ logs, tools = [], onOverride }) {
  return (
    <div className={styles.panel}>
      <div className={styles.panelHeader}>Agent Decisions (Real-time Logs)</div>

      <div className={styles.logContainer}>
        {logs.map((log) => (
          <div key={log.id} className={styles.logRow}>
            <span className={styles.timeTag}>[{log.time}]</span>

            <span className={styles.stepName}>{log.step}</span>

            <span
              className={`${styles.statusBadge} ${
                log.variant === "success" ? styles.success : styles.warning
              }`}
            >
              {log.variant === "success" ? "✓" : "⚠️"} {log.status}
            </span>
          </div>
        ))}
      </div>

      {tools.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h4>Tools Used</h4>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "8px",
              marginTop: "10px",
            }}
          >
            {tools.map((tool, index) => (
              <span
                key={`${tool}-${index}`}
                style={{
                  padding: "6px 12px",
                  borderRadius: "12px",
                  background: "#1f2937",
                  color: "white",
                  fontSize: "12px",
                }}
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      )}

      <button type="button" onClick={onOverride} className={styles.overrideBtn}>
        OVERRIDE APPROVAL (Human)
      </button>
    </div>
  );
}

export default AdminPanel;