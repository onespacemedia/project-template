# Google Apps authentication.

### SETUP:
1. https://console.developers.google.com/project
2. "Create project"
3. APIs & auth -> Consent screen
4. Select email address
5. APIs & auth -> APIs
6. Enable "Google+ API"
7. APIs & auth -> Credentials
8. Create new Client ID -> Web application
9. Copy Client ID to KEY below.
10. Copy Client Secret to `SOCIAL_AUTH_GOOGLE_PLUS_SECRET` in `base.py`.
11. Edit settings
12. Set authorized domain
