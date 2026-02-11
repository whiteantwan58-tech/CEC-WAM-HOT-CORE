# Security Policy

## Supported Versions

The CEC-WAM EVE 1010_WAKE Dashboard is currently in active development. Security updates are provided for the latest version.

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Security Measures Implemented

### ✅ No Hardcoded Secrets
- All API keys and sensitive data use environment variables
- Default values are empty strings, never actual credentials
- `.env.example` provides template without actual secrets

### ✅ Secure Configuration
- `.env` files excluded via `.gitignore`
- `.streamlit/secrets.toml` excluded from version control
- Environment-based configuration for all deployments

### ✅ Input Validation
- CSV data validated before processing
- Required columns checked before parsing
- Malformed data handled gracefully

### ✅ Error Handling
- Graceful degradation when APIs unavailable
- No sensitive information in error messages
- Retry logic with exponential backoff

### ✅ API Security
- All external API calls use HTTPS
- Timeouts configured for all requests
- Rate limiting awareness with retry logic

### ✅ Dependencies
- Regular dependency updates
- No known vulnerabilities in current versions
- Minimal dependency footprint

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public issue
2. Email the repository maintainer directly
3. Or use GitHub's private vulnerability reporting feature
4. Provide detailed information about the vulnerability

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Suggested fix (if you have one)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 24-48 hours
  - High: Within 7 days
  - Medium: Within 30 days
  - Low: Next scheduled release

### Disclosure Policy

- We will coordinate disclosure with you
- Public disclosure after fix is deployed
- Credit given to reporter (if desired)

## Security Best Practices for Users

### Environment Variables

**Local Development:**
```bash
# Never commit .env to version control
cp .env.example .env
# Edit .env with your actual values
# Verify .env is in .gitignore
```

**Streamlit Cloud:**
```toml
# Add secrets in app settings → Secrets
# Use TOML format
GROQ_API_KEY = "your-key-here"
```

### API Key Management

1. **Rotate Keys Regularly**: Change API keys every 90 days
2. **Use Minimal Permissions**: Only grant necessary access
3. **Monitor Usage**: Check API logs for unusual activity
4. **Revoke on Exposure**: Immediately revoke if key is exposed

### Deployment Security

1. **Use HTTPS**: Always deploy with SSL/TLS
2. **Enable XSRF Protection**: Configured in `.streamlit/config.toml`
3. **Regular Updates**: Keep dependencies updated
4. **Monitor Logs**: Review Streamlit Cloud logs regularly

### Code Security

1. **Review Dependencies**: Check for CVEs before adding new packages
2. **Validate Input**: Always validate user input and external data
3. **Handle Errors**: Never expose internal details in error messages
4. **Use Timeouts**: Set timeouts for all external requests

## Known Limitations

### Current Security Considerations

1. **Public RPC Endpoint**: Uses public Solana RPC (rate limits apply)
2. **API Rate Limits**: Solscan API has rate limits (handled with retry logic)
3. **CSV Data**: Local CSV files not encrypted (not sensitive data)
4. **Wallet Addresses**: Wallet addresses visible in code (public blockchain data)

### Mitigation Strategies

- **RPC Limits**: Implement caching to reduce API calls
- **Rate Limits**: Retry logic with exponential backoff
- **Data Security**: No sensitive data stored in CSV files
- **Public Data**: Wallet addresses are public blockchain identifiers

## Security Checklist for Contributors

Before submitting a pull request:

- [ ] No hardcoded secrets in code
- [ ] All sensitive data uses environment variables
- [ ] Input validation for all external data
- [ ] Error handling doesn't expose internals
- [ ] Dependencies checked for vulnerabilities
- [ ] `.env` and secrets files in `.gitignore`
- [ ] HTTPS used for all external calls
- [ ] Timeouts set for all requests
- [ ] Code reviewed for SQL injection risks (N/A - no SQL)
- [ ] XSS prevention measures in place (handled by Streamlit)

## Compliance

This project follows security best practices including:

- OWASP Top 10 awareness
- Secure coding guidelines
- Dependency vulnerability scanning
- Regular security audits

## Contact

For security concerns, please contact the repository maintainers through GitHub.

---

**Last Updated**: 2026-02-11  
**Version**: 2.0.0
