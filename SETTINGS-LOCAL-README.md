# settings.local.json Configuration

## Purpose
Configures full development permissions for Claude Code during local development and hackathon building.

## Permissions Enabled

### File Operations (All enabled, no restrictions)
- ✅ **Read**: Any file, any path
- ✅ **Write**: Any file, overwrite existing, access hidden files
- ✅ **Create**: Any file type, any extension, binary files
- ✅ **Edit**: Partial edits, bulk operations
- ✅ **Delete**: Any file, no confirmation needed

### Shell Commands (All enabled)
- ✅ **Bash**: All commands allowed, 60-second timeout
- ✅ **Python**: All packages allowed
- ✅ **npm**: All packages allowed
- ✅ **Git**: Force push, reset, branch management allowed

### Development Features
- ✅ Debug mode enabled
- ✅ Verbose logging enabled
- ✅ All errors shown
- ✅ Performance monitoring enabled

### Build Features
- ✅ Auto-compile enabled
- ✅ Watch mode enabled
- ✅ Caching enabled
- ✅ Parallel builds enabled

## When This Is Used

**During Hackathon**:
- Claude Code builds without file operation restrictions
- Can create/modify any file needed
- Can run any bash command for testing/deployment
- Full Git access for commits and pushes

## Configuration Details

```json
{
  "permissions": {
    "files": {
      "write": {"allow_overwrite": true},
      "create": {"allow_any_extension": true},
      "delete": {"require_confirmation": false}
    },
    "shell": {
      "bash": {"allow_all_commands": true}
    }
  }
}
```

## Security Note

⚠️ **Local Development Only**

This file grants unrestricted permissions. It should ONLY be used:
- In local development environments
- During the hackathon build phase
- On your personal machine

Do NOT use this in production or shared environments.

## Hackathon Context

- **Event**: Hackathon SecretarIA
- **Date**: June 6, 2026
- **Reto**: Reto 2 - Viabilidad de Negocios CDMX
- **Deadline**: 17:00 (hard stop)
- **Submission Window**: 16:00-17:00

