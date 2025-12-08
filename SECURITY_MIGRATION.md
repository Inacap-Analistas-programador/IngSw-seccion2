# Security Update Migration Guide

## Overview

This guide helps the development team migrate to the new security-hardened version of Sistema Scouts.

## Breaking Changes

### 1. Environment Variable Required: DJANGO_SECRET_KEY

**Before:** Application would start with a fallback secret key if not configured.

**After:** Application will fail to start without `DJANGO_SECRET_KEY`.

**Action Required:**
```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add to .env file
DJANGO_SECRET_KEY=your-generated-key-here
```

### 2. Plaintext Passwords No Longer Accepted

**Before:** Users with plaintext passwords in the database could authenticate.

**After:** Only hashed passwords are accepted.

**Action Required:**
1. Identify users with plaintext passwords:
```sql
SELECT usu_id, usu_username FROM Usuario 
WHERE password NOT LIKE 'pbkdf2_sha256$%';
```

2. Options:
   - **Option A:** Force password reset for affected users
   - **Option B:** Run migration script to hash existing plaintext passwords:
```python
from ApiCoreScouts.Models.usuario_model import Usuario

users_with_plaintext = Usuario.objects.exclude(password__startswith='pbkdf2_sha256$')
for user in users_with_plaintext:
    plaintext_pwd = user.password
    user.set_password(plaintext_pwd)
    user.save()
    print(f"Migrated password for user: {user.usu_username}")
```

### 3. API Endpoints Require Authentication

**Before:** Many endpoints allowed unauthenticated access.

**After:** All endpoints require valid JWT token.

**Frontend Changes Required:**
Ensure all API calls include the authentication header:
```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

The frontend code already handles this in `apiClient.js`, but verify all direct fetch calls include authentication.

### 4. JWT Tokens Now Expire

**Before:** Tokens had no expiration.

**After:** 
- Access tokens expire after 1 hour
- Refresh tokens expire after 7 days

**Frontend Changes Required:**
Implement token refresh logic:
```javascript
// Already implemented in apiClient.js
// But verify it's being used in all services
```

## Non-Breaking Changes

### 1. Enhanced Security Headers (Production Only)

When `DEBUG=False`, additional security headers are automatically enabled:
- HTTPS redirects
- Secure cookies
- HSTS headers

**Action:** Test in staging environment before production deployment.

### 2. Logging Configuration

New log files will be created in `SystemScoutsApi/logs/`:
- `django.log` - General application logs
- `security.log` - Security-related events

**Action:** Ensure the logs directory has proper permissions and set up log rotation if needed.

### 3. Improved Password Requirements

Minimum password length increased from 3 to 8 characters.

**Action:** Update any password creation forms in the frontend to enforce minimum 8 characters.

## Testing Checklist

Before deploying to production:

- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials (should fail)
- [ ] Test API access without token (should return 401)
- [ ] Test API access with expired token (should return 401, then refresh)
- [ ] Test token refresh mechanism
- [ ] Test each user role's permissions
- [ ] Verify all frontend API calls include authentication
- [ ] Test password reset flow
- [ ] Test user creation with 8+ character passwords
- [ ] Verify security headers in production mode (DEBUG=False)
- [ ] Test CORS configuration
- [ ] Review logs for authentication failures
- [ ] Load test to ensure performance is acceptable

## Deployment Steps

### 1. Development Environment

```bash
# Update code
git pull origin copilot/fix-security-issues

# Update environment variables
echo "DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env

# Migrate plaintext passwords (if needed)
python manage.py shell < migrate_passwords.py

# Test the application
python manage.py runserver
```

### 2. Staging Environment

```bash
# Deploy code
# Set environment variables
# Run migration script for passwords
# Run full test suite
# Perform security testing
```

### 3. Production Environment

```bash
# Schedule maintenance window
# Backup database
# Deploy code
# Set environment variables with strong secret key
# Run password migration if not done in staging
# Restart application
# Verify all services are running
# Monitor logs for errors
# Notify users of security improvements
```

## Rollback Plan

If critical issues are discovered:

1. **Code Rollback:**
```bash
git revert <commit-hash>
git push
```

2. **Database Rollback:**
If passwords were migrated, restore from backup taken before migration.

3. **Environment Variables:**
Restore previous .env configuration.

## Communication Template

### For Users

**Subject: Important Security Update**

Dear Sistema Scouts Users,

We have implemented important security improvements to protect your data. As part of this update:

1. All users will need to re-login to the system
2. If you haven't logged in recently, you may need to reset your password
3. Your session will now expire after 1 hour of inactivity for security
4. All connections now use enhanced encryption

These changes ensure your personal information remains secure. Thank you for your understanding.

[Include password reset link if applicable]

### For Development Team

**Subject: Security Fixes Merged - Action Required**

The security hardening pull request has been merged. Please:

1. Pull the latest code
2. Update your .env file with a new DJANGO_SECRET_KEY
3. Review the SECURITY.md document
4. Test your feature branches for compatibility
5. Update any direct API calls to include authentication

See SECURITY_MIGRATION.md for detailed instructions.

## Monitoring After Deployment

Watch for:
- Increased 401 (Unauthorized) errors in logs
- Failed login attempts
- Token refresh failures
- Performance impact from authentication checks

## Support

If you encounter issues:
1. Check logs in `SystemScoutsApi/logs/`
2. Verify environment variables are set correctly
3. Ensure frontend is using latest authentication code
4. Review SECURITY.md for configuration requirements

For urgent security issues, contact the security team immediately.
