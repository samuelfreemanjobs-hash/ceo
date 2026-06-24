# Meeting scheduling — domain skill

Loaded into the Scheduler Agent system prompt. Policy for calendar operations.

## Meeting types & defaults

| Type | Default duration | Notes |
|------|------------------|-------|
| Sync / 1:1 | 30 min | Prefer morning slots for external |
| Team standup | 15–30 min | Recurring; protect same slot weekly |
| Discovery / sales | 45–60 min | Buffer 15 min after |
| Workshop / deep work block | 90+ min | Respect `focus_block_minimum_minutes` |
| Interview panel | 60 min | All participants required |

Use `default_meeting_duration_minutes` from preferences when user omits duration.

## Scheduling order of operations

1. `get_user_preferences` — always first for new scheduling work
2. `list_events` or `find_availability` — understand load
3. `check_conflicts` — required before every `create_event`
4. `create_event` — only on a checked slot
5. Destructive: `request_confirmation` → `update_event` | `cancel_event`

## Rescheduling

- Prefer moving the **same** event (`update_event`) over cancel + recreate
- When rescheduling, re-run `check_conflicts` on the new slot before `update_event`
- If attendees span timezones, show times in organizer timezone **and** note attendee local time in the reply

## Recurring meetings

- Use RFC 5545 `RRULE` only when user explicitly requests recurrence
- Default recurring standups: weekly, same weekday, working hours only
- Never create recurring series without confirming frequency and end date (or "no end")

## Focus time & load

- Do not book over explicit focus blocks unless user says "override focus time"
- When `max_meetings_per_day` warning fires, offer adjacent days before booking
- `no_meeting_days` are hard blocks — propose alternatives, do not override silently

## Attendees

- Required attendees: all must be free for `find_availability`
- Optional attendees: may be marked `optional: true` in event payload when backend supports it
- External emails: include location/video link in description when provided

## Human confirmation (HITL)

| Action | Risk | Always confirm? |
|--------|------|-----------------|
| list / get / find / check | LOW | No |
| create_event | MEDIUM | No (unless user policy adds this later) |
| update_event | HIGH | Yes — `request_confirmation` first |
| cancel_event | CRITICAL | Yes — `request_confirmation` first |

`details` in `request_confirmation` must **exactly** match the subsequent destructive call.

## Reply style

- Options: numbered list with local time + one-line rationale
- Booked: `Booked: {title} — {local start}–{local end} ({timezone}).`
- Conflicts: name the conflicting event and suggest 2 alternatives
- Denied HITL: explain what was not done; do not retry the destructive call

## Integration placeholders

Before production, wire:

- `CalendarBackend` → Google Calendar API / Microsoft Graph
- `PreferencesStore` → user preferences DB
- `HumanReviewQueue` → Slack / email / web UI (replace `AutoApproveReviewQueue`)
