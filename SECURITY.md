# Security Best Practices

This document outlines security best practices when using MetaTrader5-MCP.

## ⚠️ Important Security Warnings

### Real Money Trading

**This server can execute real trades with real money.**

- Always test with a demo account first
- Never use production credentials until thoroughly tested
- Understand all tools before using them in production
- Be aware that trading involves financial risk

### Credential Management

**Never commit credentials to version control:**

1. **Use .env files (excluded from git)**
   ```bash
   # .env file is in .gitignore
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Use environment variables**
   ```bash
   export MT5_LOGIN=12345
   export MT5_PASSWORD=secret
   export MT5_SERVER=YourServer
   metatrader5-mcp
   ```

3. **Use secure credential storage**
   - Windows Credential Manager
   - macOS Keychain
   - Linux Secret Service
   - HashiCorp Vault for enterprise

4. **Never hardcode credentials**
   ```python
   # ❌ NEVER DO THIS
   login = 12345
   password = "secret"

   # ✓ DO THIS
   login = os.getenv("MT5_LOGIN")
   password = os.getenv("MT5_PASSWORD")
   ```

### Access Control

**Limit access to the MCP server:**

1. **Network Security**
   - Run on localhost only by default
   - Use firewall rules to restrict access
   - Never expose to public internet
   - Use VPN for remote access

2. **File Permissions**
   ```bash
   # Restrict .env file permissions
   chmod 600 .env

   # Only user can read/write
   ls -l .env
   # -rw------- 1 user user 123 date .env
   ```

3. **User Permissions**
   - Run with minimal required privileges
   - Don't run as root/administrator unless necessary
   - Create dedicated user for trading operations

### API Key and Token Management

If extending this server with API keys:

1. **Rotate keys regularly**
2. **Use different keys for dev/prod**
3. **Revoke compromised keys immediately**
4. **Monitor key usage**
5. **Set appropriate permissions**

## Secure Configuration

### Claude Desktop Configuration

**Option 1: Environment Variables (Recommended)**

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader5-mcp"
    }
  }
}
```

Then set environment variables system-wide.

**Option 2: Command Line Args**

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader5-mcp",
      "args": [
        "--login", "${MT5_LOGIN}",
        "--password", "${MT5_PASSWORD}",
        "--server", "${MT5_SERVER}"
      ]
    }
  }
}
```

Note: Variable substitution depends on your MCP client.

**⚠️ Never commit config files with credentials**

### Docker Security

When using Docker:

1. **Use secrets management**
   ```yaml
   # docker-compose.yml
   services:
     metatrader5-mcp:
       env_file:
         - .env  # Never commit this
   ```

2. **Don't build secrets into images**
   ```dockerfile
   # ❌ NEVER DO THIS
   ENV MT5_PASSWORD=secret

   # ✓ DO THIS
   # Use runtime environment variables
   ```

3. **Use read-only volumes where possible**

4. **Scan images for vulnerabilities**
   ```bash
   docker scan metatrader5-mcp:latest
   ```

## Code Security

### Input Validation

All tools use Pydantic for input validation:

```python
# Automatic validation of:
# - Required fields
# - Field types
# - Value ranges
# - Format constraints
```

### SQL Injection Prevention

This server doesn't use SQL, but if extending:

- Use parameterized queries
- Never concatenate user input into SQL
- Use ORM with proper escaping

### Path Traversal Prevention

When handling file paths:

```python
# Validate paths
from pathlib import Path

def is_safe_path(path: str, base_dir: str) -> bool:
    """Check if path is within base directory."""
    try:
        resolved = Path(path).resolve()
        base = Path(base_dir).resolve()
        return resolved.is_relative_to(base)
    except:
        return False
```

## Logging Security

### Safe Logging

**Never log sensitive data:**

```python
# ❌ BAD
logger.info(f"Login with password: {password}")

# ✓ GOOD
logger.info(f"Login attempt for account: {login}")

# ✓ GOOD (masking in code)
safe_kwargs = {
    k: v if k != "password" else "***"
    for k, v in kwargs.items()
}
logger.info(f"Login with: {safe_kwargs}")
```

### Log File Security

1. **Restrict log file permissions**
   ```bash
   chmod 640 /var/log/metatrader5-mcp.log
   ```

2. **Rotate logs regularly**
3. **Encrypt logs containing sensitive data**
4. **Monitor logs for suspicious activity**

## Network Security

### MT5 Connection

- MT5 communicates with broker servers over internet
- Ensure MT5 terminal has proper firewall rules
- Keep MT5 terminal updated
- Use broker's official servers only

### MCP Communication

- Uses stdio (stdin/stdout) by default
- No network ports exposed
- Communication only with local MCP client

## Monitoring and Auditing

### Security Monitoring

1. **Monitor failed login attempts**
2. **Track unusual trading activity**
3. **Alert on configuration changes**
4. **Log all administrative actions**

### Audit Trail

Keep records of:
- When server started/stopped
- Who accessed the system
- What trades were executed
- Configuration changes
- Error conditions

Example audit log structure:
```json
{
  "timestamp": "2024-02-14T10:00:00Z",
  "event": "trade_executed",
  "user": "trader1",
  "details": {
    "symbol": "EURUSD",
    "action": "BUY",
    "volume": 0.1
  }
}
```

## Incident Response

### If Credentials Are Compromised

1. **Immediately:**
   - Change MT5 password
   - Revoke access
   - Stop the server
   - Check for unauthorized trades

2. **Review:**
   - Access logs
   - Trading history
   - System logs
   - Network logs

3. **Prevent:**
   - Rotate all credentials
   - Review access controls
   - Update security policies
   - Train users

### If Server Is Compromised

1. **Disconnect from network**
2. **Stop all trading**
3. **Preserve logs and evidence**
4. **Analyze the breach**
5. **Rebuild from clean state**
6. **Implement additional controls**

## Regular Security Maintenance

### Weekly

- [ ] Review recent trading activity
- [ ] Check for unusual patterns
- [ ] Verify access logs

### Monthly

- [ ] Update dependencies
- [ ] Review and rotate credentials
- [ ] Test backup/restore procedures
- [ ] Review security logs

### Quarterly

- [ ] Security audit
- [ ] Penetration testing (if applicable)
- [ ] Update security documentation
- [ ] Train users on security best practices

## Dependency Security

### Keep Dependencies Updated

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt

# Or with Poetry
poetry update
```

### Vulnerability Scanning

```bash
# Using bandit for Python security issues
pip install bandit
bandit -r metatrader5_mcp

# Using pip-audit
pip install pip-audit
pip-audit
```

### Supply Chain Security

1. **Pin dependency versions**
   ```
   # In requirements.txt
   mcp==1.26.0  # Pin exact version
   ```

2. **Verify package checksums**
3. **Use trusted package sources only**
4. **Review dependency licenses**

## Compliance and Regulations

### Financial Regulations

Depending on your jurisdiction:

- May need to register as financial service provider
- Must comply with trading regulations
- May need audit trails for trades
- Must follow data protection laws

**Consult with legal/compliance team before production use.**

### Data Protection

- GDPR compliance if handling EU data
- Encrypt data at rest and in transit
- Implement right to deletion
- Document data processing activities

## Production Checklist

Before going to production:

- [ ] All credentials stored securely
- [ ] No credentials in code or config files
- [ ] Proper access controls implemented
- [ ] Logging configured (without sensitive data)
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery tested
- [ ] Security audit completed
- [ ] Incident response plan documented
- [ ] Team trained on security practices
- [ ] Legal/compliance review completed
- [ ] Demo account testing completed
- [ ] Small-scale production testing completed

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Security Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email maintainers privately
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
4. Allow time for fix before public disclosure

## License and Liability

This software is provided "as is" without warranty. See LICENSE file.

**You are responsible for:**
- Secure configuration
- Credential management
- Trading decisions and outcomes
- Compliance with regulations
- Your use of the software

---

*Last Updated: 2024-02-14*
*Review and update this document regularly*
