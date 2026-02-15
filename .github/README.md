# GitHub Automation Configuration

This directory contains automated workflows and configurations for managing pull requests and repository maintenance.

## 📋 Workflows

### PR Auto Sync and Management (`pr-auto-sync.yml`)
Automatically manages and synchronizes pull requests.

**Features:**
- **Auto-update PR branches**: Keeps all open PRs synchronized with the base branch
- **Auto-labeling**: Automatically labels PRs based on changed files
- **Conflict detection**: Detects merge conflicts and adds appropriate labels
- **PR validation**: Validates PR title and description
- **Auto-assign reviewers**: Automatically assigns reviewers to new PRs
- **PR size labeling**: Labels PRs based on size (XS, S, M, L, XL)

**Triggers:**
- When a PR is opened, synchronized, or reopened
- When changes are pushed to main branch
- Every 6 hours via scheduled job
- Manual workflow dispatch

### PR Maintenance and Cleanup (`pr-maintenance.yml`)
Maintains PR hygiene and identifies stale PRs.

**Features:**
- **Stale PR cleanup**: Marks and closes PRs inactive for 30+ days
- **Draft PR monitoring**: Notifies about draft PRs older than 14 days
- **Progress tracking**: Updates PR status based on checklist completion
- **Merge-ready detection**: Identifies PRs ready to merge

**Triggers:**
- Daily at midnight UTC
- Manual workflow dispatch

### Dependabot Auto-Merge (`dependabot-auto-merge.yml`)
Automatically handles Dependabot pull requests.

**Features:**
- **Auto-approve**: Automatically approves minor and patch updates
- **Auto-merge**: Merges minor and patch updates automatically
- **Major update alerts**: Labels major updates for manual review

**Triggers:**
- When Dependabot opens or updates a PR

### Dashboard Deployment (`deploy-dashboard.yml`)
Deploys the dashboard to GitHub Pages.

**Features:**
- Builds and deploys static site
- Publishes to GitHub Pages

**Triggers:**
- Push to main branch
- Manual workflow dispatch

## 🏷️ Auto-Labeling Configuration (`labeler.yml`)

Automatically applies labels to PRs based on changed files:

| Label | Applied When |
|-------|-------------|
| `documentation` | Changes to `.md` files or `docs/` directory |
| `workflows` | Changes to GitHub Actions workflows |
| `frontend` | Changes to HTML, JS, or CSS files |
| `backend` | Changes to Python files or API code |
| `data` | Changes to data files (CSV, XLSX, JSON) |
| `config` | Changes to configuration files |
| `tests` | Changes to test files |
| `security` | Changes to security-related files |
| `dependencies` | Changes to dependency files |

## 🤖 Dependabot Configuration (`dependabot.yml`)

Automated dependency updates:

- **Python dependencies**: Weekly updates on Mondays
- **GitHub Actions**: Weekly updates on Mondays
- Maximum 5 open PRs per ecosystem
- Auto-labeled with `dependencies` tag

## 📊 PR Labels

The automation system uses these labels:

### Size Labels
- `size/XS` - Less than 10 lines changed
- `size/S` - 10-49 lines changed
- `size/M` - 50-199 lines changed
- `size/L` - 200-499 lines changed
- `size/XL` - 500+ lines changed

### Status Labels
- `conflict` - PR has merge conflicts
- `stale` - PR has been inactive for 30+ days
- `ready-to-merge` - PR is approved and ready to merge
- `in-progress` - PR is being actively worked on
- `needs-review` - PR requires manual review

### Type Labels
- `documentation` - Documentation changes
- `workflows` - GitHub Actions changes
- `frontend` - Frontend/UI changes
- `backend` - Backend/API changes
- `data` - Data file changes
- `config` - Configuration changes
- `tests` - Test changes
- `security` - Security-related changes
- `dependencies` - Dependency updates

## 🔧 Configuration

### Permissions Required
The workflows require these permissions:
- `contents: write` - For updating branches
- `pull-requests: write` - For managing PRs
- `issues: write` - For adding labels and comments

### Secrets Required
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

## 🚀 Usage

All workflows run automatically based on their triggers. No manual intervention is required.

### Manual Triggers
You can manually trigger workflows from the Actions tab:
1. Go to the repository's Actions tab
2. Select the workflow you want to run
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## 📖 Best Practices

For optimal automation:

1. **Use descriptive PR titles** (minimum 10 characters)
2. **Add detailed PR descriptions** (minimum 20 characters)
3. **Use checklists** to track progress in PR descriptions
4. **Respond to automation comments** to keep PRs active
5. **Use draft PRs** for work-in-progress
6. **Add `keep-open` label** to exempt PRs from stale cleanup

## 🔍 Monitoring

Monitor automation activity:
- Check the Actions tab for workflow runs
- Review PR comments for automation feedback
- Watch for labels applied automatically
- Check for conflict notifications

## 🛠️ Troubleshooting

### PR not auto-updating
- Ensure the workflow has proper permissions
- Check for merge conflicts
- Verify the base branch is up to date

### Labels not applied
- Check `.github/labeler.yml` configuration
- Ensure file paths match the patterns
- Verify workflow permissions

### Dependabot not merging
- Check if the update is minor/patch (major requires manual review)
- Ensure all checks pass
- Verify permissions are correct

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Labeler Action](https://github.com/actions/labeler)
- [Stale Action](https://github.com/actions/stale)
