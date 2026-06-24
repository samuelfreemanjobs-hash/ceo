# Approval matrix

| Aggregate discount | Segment | Approver | Auto-approve |
|--------------------|---------|----------|--------------|
| ≤ 25% | SMB | — | Yes |
| ≤ 25% | Mid-market | — | Yes |
| ≤ 20% | Enterprise | — | Yes |
| 25–40% | Any | VP-Sales | No |
| > 40% | Any | CRO | No |
| Any below floor | Any | **BLOCK** | No |
| Restricted jurisdiction | Any | Legal | No |
| Uncapped IP indemnity | Any | Legal + CRO | No |

## Non-discount escalations

| Trigger | Owner |
|---------|-------|
| `scope.non_standard = true` | Solutions Engineer + Director |
| `risk.jurisdiction_status = blocked` | Legal |
| `dossier_confidence = low` | Rep clarifying question (Director) |
