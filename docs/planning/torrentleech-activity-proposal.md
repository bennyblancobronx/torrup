# TorrentLeech Activity Enforcement Proposal

## Summary
Add a strict activity enforcement mode for TorrentLeech that warns users when projected monthly uploads fall below the tracker minimum. The system uses existing queue and history data to compute risk and surfaces a critical banner in the Dashboard and Queue pages.

## Goals
- Enforce TorrentLeech activity minimums by default.
- Warn early when projected uploads are below the monthly requirement.
- Keep logic simple, transparent, and auditable.

## Non-Goals
- Automated uploads or forced publishing.
- Complex forecasting beyond current month counts and ready queue size.
- Multi-tracker rule resolution beyond TorrentLeech.

## Tracker Minimums (TorrentLeech)
- Minimum uploads per month: 10.
- Minimum seeding: 10 copies or 7 days, whichever comes first.
- Inactivity warning: after a few weeks.
- Absence notice: 4+ weeks.

## Settings Additions
Stored in `settings` table and editable in Settings UI under “TorrentLeech Preferences”.
- `tl_min_uploads_per_month` (default `10`)
- `tl_min_seed_copies` (default `10`)
- `tl_min_seed_days` (default `7`)
- `tl_inactivity_warning_weeks` (default `3`)
- `tl_absence_notice_weeks` (default `4`)
- `tl_enforce_activity` (default `1`, enforced on)

## Health Calculation
Computed monthly on current UTC month.
- `uploads_this_month`: count of history items with status `success` or `duplicate` and created_at in current month.
- `ready_count`: count of queue items with status `queued`.
- `projected = uploads_this_month + ready_count`
- `critical = (tl_enforce_activity == 1) AND (projected < tl_min_uploads_per_month)`

## UI Notifications
Add a critical warning banner when `critical` is true.
- Dashboard: banner at top of page.
- Queue: banner above filters.

Banner content should include:
- “Projected uploads: X / Y”
- “Ready queue: N”
- “Action: add items or increase monthly target”

## API Additions
New endpoint to supply the health data:
- `GET /api/activity/health`
- Response:
```json
{
  "uploads_this_month": 4,
  "ready_count": 3,
  "projected": 7,
  "minimum": 10,
  "critical": true
}
```

## Enforcement Behavior
- If `tl_enforce_activity` is enabled, show banners and include TL minimums in any queue planning UI.
- No hard blocks on uploads or auto-scan in v0.1.x.
- Optional future enhancement: block auto-scan when `critical` is true.

## Implementation Notes
- History queries should use UTC month boundaries for consistency.
- “Ready queue” is defined as `status = queued` only.
- Keep calculations server-side to avoid client drift.

## Testing Checklist
- Toggle `tl_enforce_activity` off and verify banners disappear.
- Set `tl_min_uploads_per_month` below projected and verify no warning.
- Set minimum above projected and verify warning shows in Dashboard and Queue.
- Verify month boundary logic on the first day of a month.
