# PROJECT.md — Platform Research Notes

> This file is a working notepad for the developer (or AI coding agent) building
> this MCP server. Fill in each section as you research the target platform.
> The information here drives the implementation in `src/main.py` and `src/tools.py`.
>
> **Do not commit secrets.** Store credentials in `.env` (which is gitignored).

---

## Platform Overview

**Platform name:**
**Official docs:** (link to API documentation homepage)
**Base URL:** (e.g. `https://api.example.com/v1`)

Brief description of what this platform does and why we are building an MCP server for it:



---

## Authentication

**Auth type:** (API Key / OAuth / Bearer Token / Bot Token / other)
**How to obtain credentials:** (link to developer portal, app registration page, etc.)

### Credential details

- **Token / key name:** (e.g. `GITHUB_TOKEN`, `LINEAR_ACCESS_TOKEN`)
- **Header format:** (e.g. `Bearer {api_key}`, `token {api_key}`, `Bot {api_key}`)
- **Scopes required:** (list each scope on its own line)

### OAuth-specific (skip if using API Key)

- **Authorize URL:**
- **Token URL:**
- **Client ID:** (store in `.env`, reference here by variable name only)
- **Client Secret:** (store in `.env`, reference here by variable name only)
- **Available scopes:**

### Example authenticated request

```
(paste a curl or Python example showing how a request is made with this credential)
```

---

## Endpoints / Features to Implement

List the API endpoints or features you plan to expose as MCP tools.
For each, note the HTTP method, path, key parameters, and response shape.

| Tool name | Method | Path | Description |
|-----------|--------|------|-------------|
|           |        |      |             |
|           |        |      |             |
|           |        |      |             |

---

## Rate Limits and Restrictions

- **Rate limit:** (e.g. 100 requests/minute)
- **Retry strategy:** (e.g. exponential backoff, respect `Retry-After` header)
- **Other restrictions:** (e.g. IP allowlisting, webhook requirements)

---

## Response Format Notes

Describe the general shape of API responses — JSON structure, pagination style,
error format, etc. Paste a representative example if helpful.

```json

```

---

## Token / Credential Notes

Notes on token lifecycle, expiry, rotation, or platform-specific quirks:

- (e.g. "Tokens expire after 45 days of inactivity")
- (e.g. "Token permissions auto-downgrade if unused")
- (e.g. "Requires IP allowlisting for write tokens")

---

## Additional References

- (link to OpenAPI spec, SDK docs, tutorials, etc.)
- (link to platform's MCP/AI integration page if one exists)
- (link to any community resources or examples)

---

## Notes for README

Bullet points to include in the project README when it is written:

-
-
-
