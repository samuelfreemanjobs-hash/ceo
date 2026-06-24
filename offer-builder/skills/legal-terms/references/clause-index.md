# Clause library index (search hints)

Use with `clm.clauses.search(query, deal_type, jurisdiction)`:

| Need | Suggested query |
|------|-----------------|
| Standard MSA body | `msa-standard` |
| Pilot agreement | `pilot-agreement` |
| GDPR DPA | `dpa-gdpr` |
| US data processing | `dpa-us-standard` |
| SLA 99.9% | `sla-enterprise-999` |
| SLA 99.5% | `sla-standard-995` |
| Mutual indemnity | `indemnity-mutual` |
| Uncapped IP | `indemnity-ip-uncapped` *(requires escalation)* |
| Termination for convenience | `termination-convenience` |
| Auto-renewal 12mo | `renewal-evergreen-12` |

Each result must include `deviation_requires` role if non-standard for deal type.
