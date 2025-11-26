# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We take the security of the Expert Review Analysis System seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### Please DO NOT:

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Please DO:

1. **Email your findings** to the project maintainers (see repository for contact)
2. **Provide detailed information** including:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if any)
3. **Allow time for response** - We aim to respond within 48 hours
4. **Work with us** to verify and address the issue

## What to Report

Please report any security issues including but not limited to:

### High Priority

- Authentication or authorization bypass
- Remote code execution
- SQL injection or other injection attacks
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Sensitive data exposure
- Security misconfigurations

### Medium Priority

- Denial of service vulnerabilities
- Information disclosure
- Insecure dependencies
- Broken access control

### Low Priority

- Best practice violations
- Non-security configuration issues

## Security Best Practices

### For Self-Hosted Deployments

1. **Environment Variables**

   - Never commit `.env` files to version control
   - Use strong, unique API keys
   - Rotate credentials regularly

2. **Network Security**

   - Use HTTPS in production
   - Configure CORS appropriately
   - Use a reverse proxy (nginx, Apache, Caddy)
   - Enable rate limiting

3. **Dependencies**

   - Keep dependencies up to date
   - Run `pip install --upgrade` regularly
   - Monitor security advisories

4. **Access Control**
   - Restrict access to backend APIs
   - Use firewall rules
   - Enable authentication if deploying publicly

### For Containerized Deployments

1. **Image Security**

   - Use official base images
   - Scan images for vulnerabilities
   - Keep base images updated

2. **Runtime Security**

   - Run containers as non-root user
   - Use read-only filesystems where possible
   - Limit container resources
   - Use Docker secrets for sensitive data

3. **Network Isolation**

   - Use Docker networks
   - Limit exposed ports
   - Use internal networks for backend services

4. **Secrets Management**
   - Use Docker secrets or Kubernetes secrets
   - Never embed secrets in images
   - Rotate secrets regularly

## Known Security Considerations

### API Keys (Optional External Services)

- IMDb, Steam, and Metacritic API keys are **optional**
- System works without them (uses web scraping fallback)
- If provided, keys should be kept secure in `.env` files
- Keys should never be committed to version control

### Web Scraping

- Web scraping uses User-Agent rotation
- Respects rate limits to avoid detection as bot
- Falls back to mock data if scraping fails
- No authentication credentials stored

### Data Storage

- User preferences stored in JSON files (local filesystem)
- No sensitive user data collected
- No authentication system (yet)
- Consider encryption for production deployments

### Rate Limiting

- Default: 100 requests per 60 seconds
- Configurable via environment variables
- Prevents abuse and DOS attacks
- Consider stricter limits for public deployments

## Updates and Patches

When security vulnerabilities are identified and fixed:

1. **Patch Released** - Security patches released as soon as possible
2. **Notification** - Users notified via GitHub releases and security advisories
3. **Upgrade Path** - Clear upgrade instructions provided
4. **Timeline** - Typically fixed within 7 days for high-priority issues

## Security Checklist for Deployment

Before deploying to production:

- [ ] Changed all default credentials
- [ ] Configured HTTPS
- [ ] Set up proper CORS headers
- [ ] Enabled rate limiting
- [ ] Configured secure environment variables
- [ ] Set up firewall rules
- [ ] Enabled logging and monitoring
- [ ] Performed security scan on dependencies
- [ ] Reviewed and hardened Docker configuration (if using containers)
- [ ] Set up backup and recovery procedures
- [ ] Configured resource limits
- [ ] Implemented proper error handling (no sensitive info in errors)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security Guidelines](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

Thank you for helping keep the Expert Review Analysis System and its users safe!
