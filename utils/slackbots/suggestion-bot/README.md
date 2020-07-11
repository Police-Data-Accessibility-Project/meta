# Slack Channel Suggestions Bot
Send messages to people as they introduce themselves in #_introduceyourself channel with suggestions for which channels to join based on keywords found in their introduction.

_Updated: July, 2020_<br>
_Published TBD_

---

## Contributions
Submit a PR and if you need access to the app itself, check with @klefevre or @Zach - Slack Admin to be added as a collaborator and presumably get you access to this [link](https://api.slack.com/apps/A015Q3Q5HS9).

This is really simple keyword matching right now, so if you see some areas missing, please add to suggestions.json and create a GitHub PR.
The format is: 
```json
{"slack-channel-id": {"name": "human-readable-name", "keywords": ["keyword", "to", "look", "for", "in", "intro"]}}
```

## Current status

Deployed to AWS on a personal account, should move when PDAP gets its own hosting.

---
