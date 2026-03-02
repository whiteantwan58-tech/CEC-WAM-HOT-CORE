# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

Please open a **private** security advisory via
[GitHub Security Advisories](https://github.com/whiteantwan58-tech/CEC-WAM-HOT-CORE/security/advisories/new)
rather than a public issue so that sensitive details are not disclosed before
a fix is available.

---

## Secret / API-Key Handling

### Never commit secrets

All API keys, tokens, and sheet IDs **must** be stored in a `.env` file
(locally) or as
[GitHub Actions / Streamlit Cloud secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
in production.  `.env` is listed in `.gitignore` and must never be committed.

Copy `.env.example` to get started:

```bash
cp .env.example .env
# Fill in your values, then restart the app.
```

### Automated secret scanning

A [gitleaks](https://github.com/gitleaks/gitleaks) workflow runs on every push
and pull request (`.github/workflows/secret-scanning.yml`).  Any detected
secret will cause the workflow to fail and block the merge.

### If a secret was previously committed

If a key or token was already pushed to a public repository it must be
treated as **compromised**, even after removal from the codebase.

Rotation checklist:
1. **Revoke / regenerate the exposed key immediately** in the provider console:
   - OpenAI → https://platform.openai.com/api-keys
   - ElevenLabs → https://elevenlabs.io/app/settings/api-keys
   - NASA → https://api.nasa.gov/ (request new key)
   - OpenWeatherMap → https://home.openweathermap.org/api_keys
   - Google Cloud (Sheets/Drive) → https://console.cloud.google.com/iam-admin/serviceaccounts
2. **Add the new key** to your `.env` (local) or your hosting platform's
   secrets store.
3. **Remove the secret from git history** using
   [`git filter-repo`](https://github.com/newren/git-filter-repo) (recommended)
   or `BFG Repo-Cleaner`, and force-push, then ask GitHub Support to run a
   garbage-collection sweep.

   ```bash
   # Example using git filter-repo (install: pip install git-filter-repo)
   git filter-repo --replace-text <(echo 'EXPOSED_KEY==>REMOVED')
   ```

   > ⚠️ History rewriting requires coordination with all collaborators
   > (they must re-clone after the rewrite).

4. Review GitHub's
   [Removing sensitive data guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
   for the full procedure.
