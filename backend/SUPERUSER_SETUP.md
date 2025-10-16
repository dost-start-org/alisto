# Creating Superuser from Environment Variables

## For Local Development

1. **Add credentials to your `.env` file**:

   ```bash
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=changeme123
   DJANGO_SUPERUSER_FIRST_NAME=Admin  # Optional, defaults to "Admin"
   DJANGO_SUPERUSER_LAST_NAME=User    # Optional, defaults to "User"
   ```

2. **Run the command**:
   ```bash
   source venv/bin/activate
   python manage.py create_superuser_from_env
   ```

## For Staging/Production

### Digital Ocean App Platform

1. **Go to your app in Digital Ocean console**
2. **Navigate to Settings → App-Level Environment Variables**
3. **Add these variables**:

   - `DJANGO_SUPERUSER_EMAIL` = `your-admin@email.com`
   - `DJANGO_SUPERUSER_PASSWORD` = `your-secure-password`
   - `DJANGO_SUPERUSER_FIRST_NAME` = `Admin` (Optional)
   - `DJANGO_SUPERUSER_LAST_NAME` = `User` (Optional)
   - **Important**: Mark `DJANGO_SUPERUSER_PASSWORD` as encrypted/secret

4. **Access the Console tab** in your app
5. **Run the command**:
   ```bash
   python manage.py create_superuser_from_env
   ```

### Other Hosting Platforms

1. **Set environment variables** in your hosting platform's dashboard or config
2. **SSH into your server** (or use the platform's console)
3. **Run the command**:
   ```bash
   cd /path/to/your/project
   source venv/bin/activate  # if using virtual environment
   python manage.py create_superuser_from_env
   ```

## Features

✅ **Safe to run multiple times** - Won't create duplicate users
✅ **No interactive prompts** - Perfect for CI/CD pipelines
✅ **Secure** - Credentials stored in environment variables, not in code
✅ **Clear feedback** - Shows success/error messages

## Troubleshooting

### "Environment variable is not set"

Make sure both required variables are set:

- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

Optional variables (have defaults):

- `DJANGO_SUPERUSER_FIRST_NAME` (default: "Admin")
- `DJANGO_SUPERUSER_LAST_NAME` (default: "User")

### "Superuser already exists"

This is normal! The command detected an existing user with that email and skipped creation.

### Want to update the password?

The command won't update existing users. To change the password:

1. Delete the existing user through Django admin or shell
2. Run the command again

Or use Django's built-in password reset:

```bash
python manage.py changepassword <username>
```
