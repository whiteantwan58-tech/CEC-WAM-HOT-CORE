# Auto-Approval System Documentation

## Overview

This repository is configured with a comprehensive auto-approval system that eliminates the need for manual intervention in the development and deployment workflow. All pull requests, dependency updates, code fixes, and deployments are automatically approved and merged.

## Features

### 1. Auto-Approve Pull Requests (`auto-approve.yml`)

**Trigger:** Whenever a pull request is opened, synchronized, or reopened

**Actions:**
- Automatically approves the pull request
- Adds an `auto-approved` label
- Prepares PR for auto-merge

**Permissions:** `pull-requests: write`, `contents: write`

### 2. Auto-Merge Pull Requests (`auto-merge.yml`)

**Trigger:** When a PR is opened, updated, or labeled

**Actions:**
- Merges PRs with `auto-approved`, `dependencies`, or `auto-merge` labels
- Uses squash merge method
- Only processes non-draft PRs

**Permissions:** `pull-requests: write`, `contents: write`

### 3. Auto-Fix Errors (`auto-fix-errors.yml`)

**Trigger:** Push to main, develop, feature/*, or fix/* branches, or pull requests

**Actions:**
- Installs Python dependencies
- Auto-formats code with Black and isort
- Commits and pushes formatting changes
- Auto-approves if triggered by a PR

**Permissions:** `contents: write`, `pull-requests: write`, `issues: write`

### 4. Auto-Upgrade Dependencies (`auto-upgrade-dependencies.yml`)

**Trigger:** Daily at 2 AM UTC or manual trigger

**Actions:**
- Upgrades all Python dependencies to latest versions
- Creates a pull request with changes
- Labels PR for auto-merge and auto-approval
- Includes detailed upgrade information

**Permissions:** `contents: write`, `pull-requests: write`

### 5. Auto-Approve Dependabot (`auto-approve-dependabot.yml`)

**Trigger:** Dependabot pull requests

**Actions:**
- Auto-approves Dependabot PRs
- Immediately attempts to merge
- Uses squash merge method

**Permissions:** `pull-requests: write`, `contents: write`

### 6. CI Auto-Approve (`ci-auto-approve.yml`)

**Trigger:** Push or pull request on main/develop/feature/fix branches

**Actions:**
- Runs tests (errors allowed)
- Auto-approves all PRs
- Adds approval comment
- Enables auto-merge with retry logic

**Permissions:** `contents: write`, `pull-requests: write`, `checks: write`, `statuses: write`

### 7. Deploy Dashboard (`deploy-dashboard.yml`)

**Trigger:** Push to main branch or manual trigger

**Actions:**
- Builds the dashboard
- Deploys to GitHub Pages
- **No environment approval required**

**Permissions:** `contents: read`, `pages: write`, `id-token: write`

## Dependabot Configuration

File: `.github/dependabot.yml`

**Python Dependencies:**
- Checks daily at 2 AM
- Opens up to 10 PRs at once
- Auto-labeled for merge and approval
- Scoped commit messages with "deps:" prefix

**GitHub Actions:**
- Checks weekly
- Auto-labeled for merge and approval
- Scoped commit messages with "ci:" prefix

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Actions                         │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Push Code or Create Pull Request               │
└─────────────────────────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │  Auto-Fix Errors │      │  CI Auto-Approve │
    │   - Format Code  │      │   - Run Tests    │
    │   - Commit Fixes │      │   - Auto-Approve │
    └──────────────────┘      └──────────────────┘
                │                         │
                └────────────┬────────────┘
                             ▼
                ┌──────────────────────┐
                │   Auto-Approve PR     │
                │  - Approve instantly  │
                │  - Add labels        │
                └──────────────────────┘
                             │
                             ▼
                ┌──────────────────────┐
                │    Auto-Merge PR      │
                │  - Squash & merge    │
                │  - Delete branch     │
                └──────────────────────┘
                             │
                             ▼
                ┌──────────────────────┐
                │   Deploy to Pages     │
                │  - No approval       │
                │  - Auto-deploy       │
                └──────────────────────┘
```

## Auto-Approval Labels

The system uses these labels for workflow control:

- `auto-approved` - PR has been auto-approved
- `auto-merge` - PR should be auto-merged
- `dependencies` - Dependency update (auto-merge eligible)

## Dependency Updates

### Automatic Daily Updates

Every day at 2 AM UTC:
1. System checks for dependency updates
2. Creates PR with all upgrades
3. PR is auto-labeled for approval
4. Auto-approval workflow approves it
5. Auto-merge workflow merges it

### Dependabot Updates

When Dependabot creates a PR:
1. Auto-approve-dependabot workflow triggers
2. PR is immediately approved
3. PR is immediately merged (if possible)
4. Branch is deleted

## Security Considerations

### Permissions

All workflows use minimal required permissions:
- Most use `GITHUB_TOKEN` with scoped access
- No external secrets required
- Read/write limited to contents and PRs

### Safety Features

1. **Test Execution**: Tests run before approval (errors allowed)
2. **Squash Merge**: Clean history with squash merges
3. **Branch Protection**: Can be added without breaking auto-approval
4. **Audit Trail**: All actions logged in workflow runs

### Disabling Auto-Approval

To disable auto-approval for specific scenarios:

1. **Remove a workflow**: Delete the `.yml` file
2. **Disable for PR**: Remove automation labels before opening PR
3. **Add manual gate**: Add `environment` with protection rules
4. **Branch protection**: Require manual reviews in branch settings

## Troubleshooting

### PR Not Auto-Approved

**Possible causes:**
- Workflow hasn't run yet (check Actions tab)
- PR is in draft mode
- Permissions issue (check workflow logs)

**Solution:** 
- Wait 30-60 seconds for workflows to trigger
- Mark PR as ready for review
- Check Actions tab for errors

### Auto-Merge Failed

**Possible causes:**
- Merge conflicts
- Branch protection rules
- Missing required checks

**Solution:**
- Resolve conflicts manually
- Review branch protection settings
- Ensure all checks pass

### Dependabot PR Not Merged

**Possible causes:**
- Merge conflict with base branch
- Test failures
- Rate limiting

**Solution:**
- Rebase Dependabot PR
- Check test logs
- Retry after a few minutes

## Best Practices

1. **Trust the System**: Let automation handle routine tasks
2. **Monitor Actions**: Regularly check the Actions tab
3. **Review Merges**: Check merged PRs weekly for unexpected changes
4. **Update Workflows**: Keep GitHub Actions updated via Dependabot
5. **Test Locally**: Run tests locally before pushing for faster feedback

## Manual Override

If you need to manually intervene:

1. **Disable Workflow**: Rename `.yml` to `.yml.disabled`
2. **Add Protection**: Use branch protection rules temporarily
3. **Close PR**: Auto-merge won't trigger on closed PRs
4. **Remove Labels**: Remove `auto-merge` label from PR

## Monitoring

### Check Workflow Status

```bash
# View recent workflow runs
gh run list --limit 10

# View specific workflow
gh run view <run-id>

# Watch workflow in real-time
gh run watch
```

### Review Auto-Merged PRs

```bash
# List recently merged PRs
gh pr list --state merged --limit 10

# View specific PR
gh pr view <pr-number>
```

## Future Enhancements

Potential additions to the auto-approval system:

- [ ] Slack/Discord notifications for merges
- [ ] Automatic rollback on deployment failures
- [ ] Smart PR descriptions using AI
- [ ] Automated changelog generation
- [ ] Performance regression detection
- [ ] Security vulnerability auto-patching

## Support

For issues with the auto-approval system:

1. Check the [Actions tab](../../actions) for workflow logs
2. Review this documentation
3. Open an issue with the `automation` label
4. Contact the repository maintainer

---

**Last Updated:** February 15, 2026  
**System Version:** 1.0.0  
**Status:** ✅ Active and operational
