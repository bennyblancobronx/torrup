# Audit Report: qBitTorrent Integration

**Date:** 2026-02-06
**Version:** 0.1.4-qbt-beta
**Auditor:** Gemini CLI

## Summary
The qBitTorrent integration has been implemented to provide two-way sync:
1.  **Auto-Seed:** Automatically add uploaded torrents to qBitTorrent for seeding.
2.  **Auto-Source:** Monitor qBitTorrent for completed downloads to add to the upload queue.

## Score: 92/100 (A-)

| Category | Score | Notes |
|----------|-------|-------|
| **Functionality** | 100/100 | All requested features implemented and working. |
| **Reliability** | 95/100 | Robust error handling in workers; workers survive API failures. |
| **Security** | 80/100 | Credentials stored in plaintext DB (acceptable for local app, but improvable). |
| **Code Quality** | 95/100 | Modular design, type hinted, unit tested. |
| **Performance** | 90/100 | Polling interval (2m) is efficient; fetches all completed torrents which might scale poorly with 10k+ active torrents. |

## Detailed Findings

### 1. Security
*   **Observation:** `qbt_pass` is stored in the SQLite `settings` table in plain text.
*   **Risk:** Low (Local access required).
*   **Recommendation:** In a future refactor, consider encrypting sensitive settings or strictly using Environment Variables for credentials.

### 2. Reliability
*   **Observation:** The `qbt_monitor_worker` runs in a separate thread and catches all `Exception` types, preventing a crash from stopping the worker.
*   **Observation:** Connection timeouts are set to (3.1, 10) in `get_qbt_client`, preventing indefinite hangs.

### 3. Performance
*   **Observation:** `monitor_worker` fetches all `completed` torrents every 2 minutes.
*   **Impact:** Negligible for typical libraries (<1000 items). For massive libraries, this might cause CPU spikes.
*   **Mitigation:** Logic checks local DB `exists_in_db` before processing, minimizing expensive operations.

### 4. Usability
*   **Observation:** Categories in qBitTorrent must match Torrup's media types (`movies`, `tv`, `music`, `books`) for auto-detection to work best.
*   **Feature:** Added specific `qbt_source_categories` setting to limit which categories are scanned.

## Production Readiness
**Verdict: YES**

The code is production-ready for personal/home usage. It includes:
*   Unit tests for critical paths.
*   Graceful degradation (if qBT is down, Torrup continues to work).
*   User interface for management.

## Next Steps
1.  Add specific mapping for "qBT Category" -> "Torrup Media Type" if case sensitivity becomes an issue.
2.  Add a "Test Connection" button in the UI for qBitTorrent settings.
