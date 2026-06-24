# Slack setup — Scheduler HITL

Configure Slack for human-in-the-loop confirmations (update/cancel meetings).

## 1. Create Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → From scratch
2. Name: `Scheduler Agent` (or your choice)
3. Pick your workspace

## 2. Bot token scopes

**OAuth & Permissions** → Bot Token Scopes:

| Scope | Why |
|-------|-----|
| `chat:write` | Post confirmation messages |
| `chat:write.public` | Post to channels bot isn't in (optional) |
| `users:read` | Resolve @mentions |

Install to workspace → copy **Bot User OAuth Token** (`xoxb-...`) → `SLACK_BOT_TOKEN`

## 3. Signing secret

**Basic Information** → **App Credentials** → **Signing Secret** → `SLACK_SIGNING_SECRET`

## 4. Interactivity

**Interactivity & Shortcuts** → Enable → Request URL:

```
https://your-host/slack/interactions
```

Run Process B:

```bash
cd scheduler-agent
gunicorn -w 4 -b 0.0.0.0:3000 webhook_main:app
```

For local dev use ngrok/cloudflared to expose port 3000.

## 5. Approval channel

Set where confirmations post:

```bash
# DM to yourself
export SLACK_APPROVAL_CHANNEL=@U0123456

# Or team channel
export SLACK_APPROVAL_CHANNEL=#scheduler-approvals
```

Find your user ID: Slack profile → ⋮ → Copy member ID → prefix with `@`.

## 6. Redis (shared store)

Process A (agent) and Process B (webhook) must share Redis:

```bash
docker compose up -d redis
export REDIS_URL=redis://localhost:6379/0
```

## 7. Test flow

1. Trigger an update/cancel via scheduler (not auto-approve HITL)
2. Confirm message appears in approval channel
3. Click Approve / Deny
4. Agent receives decision via `RedisConfirmationStore`

## Env checklist

| Variable | Source |
|----------|--------|
| `SLACK_BOT_TOKEN` | OAuth install |
| `SLACK_SIGNING_SECRET` | App credentials |
| `SLACK_APPROVAL_CHANNEL` | Your choice |
| `REDIS_URL` | docker-compose or managed Redis |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 401 on interactions | Wrong signing secret |
| Buttons do nothing | Webhook URL not reachable; check gunicorn logs |
| Expired confirmation | Default 300s timeout in `SlackHumanReviewQueue` |
