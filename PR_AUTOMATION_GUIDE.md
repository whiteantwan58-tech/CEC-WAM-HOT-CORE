# Pull Request Auto-Sync and Management System

## 🚀 Overview

This repository is equipped with comprehensive automated pull request management that handles synchronization, labeling, conflict detection, and maintenance automatically.

## ✨ Key Features

### 1. **Automatic Branch Synchronization**
Your PR branch will automatically stay in sync with the `main` branch:
- Updates happen every 6 hours
- Updates happen when main branch is updated
- No manual rebasing needed!

### 2. **Automatic Labeling**
PRs are automatically labeled based on:
- **Files changed**: `documentation`, `frontend`, `backend`, `workflows`, etc.
- **PR size**: `size/XS`, `size/S`, `size/M`, `size/L`, `size/XL`
- **Status**: `conflict`, `ready-to-merge`, `in-progress`, `stale`
- **Type**: `dependencies`, `major-update`, etc.

### 3. **Conflict Detection**
- Automatically detects merge conflicts
- Adds `conflict` label
- Posts a comment notifying you
- Removes label when conflict is resolved

### 4. **PR Validation**
- Checks PR title (minimum 10 characters)
- Checks PR description (minimum 20 characters)
- Posts suggestions if validation fails

### 5. **Auto-Reviewer Assignment**
- Repository owner is automatically assigned as reviewer
- Only for PRs not created by bots

### 6. **Stale PR Management**
- PRs inactive for 30+ days are marked as stale
- Stale PRs are closed after 7 days
- Add `keep-open` label to exempt a PR

### 7. **Draft PR Monitoring**
- Draft PRs older than 14 days receive a reminder
- Helps track work-in-progress

### 8. **Progress Tracking**
- Automatically tracks checklist completion in PR descriptions
- Adds labels like `in-progress`, `almost-done`, `ready-for-review`

### 9. **Dependabot Integration**
- Automatic dependency updates
- Auto-approves and merges minor/patch updates
- Flags major updates for manual review

## 📝 Best Practices

### Creating a PR

1. **Use descriptive titles** (at least 10 characters)
   ```
   ✅ Good: "Add user authentication with JWT tokens"
   ❌ Bad: "Update"
   ```

2. **Write detailed descriptions** (at least 20 characters)
   ```
   ✅ Good: "This PR adds JWT-based authentication to the API endpoints..."
   ❌ Bad: "Fixed stuff"
   ```

3. **Use checklists to track progress**
   ```markdown
   - [x] Implement authentication logic
   - [x] Add tests
   - [ ] Update documentation
   - [ ] Add example usage
   ```

### Managing Your PR

1. **For work-in-progress**: Mark as Draft PR
2. **To exempt from stale cleanup**: Add `keep-open` label
3. **To prevent auto-update**: Add `no-auto-update` label (requires manual addition)
4. **To mark as blocked**: Add `blocked` label

### Reviewing Changes

When you receive a PR review assignment:
1. Check the auto-generated labels for context
2. Review the size label to estimate review time
3. Check for conflict labels before starting
4. Review automated validation feedback

## 🏷️ Label Reference

### Size Labels
| Label | Lines Changed | Typical Review Time |
|-------|---------------|-------------------|
| `size/XS` | < 10 | 5 minutes |
| `size/S` | 10-49 | 10 minutes |
| `size/M` | 50-199 | 20 minutes |
| `size/L` | 200-499 | 45 minutes |
| `size/XL` | 500+ | 1+ hour |

### Status Labels
| Label | Meaning |
|-------|---------|
| `conflict` | Merge conflict exists |
| `stale` | Inactive for 30+ days |
| `ready-to-merge` | Approved and mergeable |
| `in-progress` | 25-74% checklist complete |
| `almost-done` | 75-99% checklist complete |
| `ready-for-review` | 100% checklist complete |
| `just-started` | < 25% checklist complete |

### Type Labels
| Label | Applied When |
|-------|--------------|
| `documentation` | Changes to `.md` or docs files |
| `frontend` | Changes to HTML, JS, CSS |
| `backend` | Changes to Python or API code |
| `workflows` | Changes to GitHub Actions |
| `data` | Changes to CSV, XLSX, JSON |
| `config` | Changes to configuration files |
| `tests` | Changes to test files |
| `security` | Security-related changes |
| `dependencies` | Dependency updates |

### Special Labels
| Label | Purpose |
|-------|---------|
| `keep-open` | Exempts PR from stale cleanup |
| `blocked` | PR is blocked by external factors |
| `needs-review` | Requires manual review |
| `major-update` | Major version dependency update |

## 🔧 Customization

### Changing Auto-Update Frequency

Edit `.github/workflows/pr-auto-sync.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Change 6 to desired hours
```

### Adjusting Stale PR Timeframe

Edit `.github/workflows/pr-maintenance.yml`:
```yaml
days-before-stale: 30  # Change to desired days
days-before-close: 7   # Change to desired days
```

### Adding New Auto-Labels

Edit `.github/labeler.yml`:
```yaml
your-label-name:
  - 'path/to/files/**/*'
  - '**/*.extension'
```

### Modifying PR Size Thresholds

Edit `.github/workflows/pr-auto-sync.yml` in the `check-pr-size` job:
```javascript
if (totalChanges < 10) {
  sizeLabel = 'size/XS';
} else if (totalChanges < 50) {  // Adjust these numbers
  sizeLabel = 'size/S';
}
```

## 🎯 Common Scenarios

### Scenario 1: My PR has conflicts
**What happens:**
- Automation adds `conflict` label
- You receive a comment notification
- The label is removed when you resolve conflicts

**What to do:**
1. Pull the latest changes from main: `git pull origin main`
2. Resolve conflicts
3. Push your changes
4. Automation will verify and remove the label

### Scenario 2: My PR is marked as stale
**What happens:**
- After 30 days of inactivity, PR gets `stale` label
- You receive a comment notification
- PR will close in 7 days without activity

**What to do:**
- Add a comment explaining the status
- Push new commits
- Add `keep-open` label if needed
- Request a review

### Scenario 3: Dependabot opened a PR
**What happens:**
- For minor/patch updates: Auto-approved and auto-merged
- For major updates: Labeled for manual review

**What to do:**
- Minor/patch: Nothing! It's automatic
- Major: Review changelog and test thoroughly before approving

### Scenario 4: Draft PR reminder
**What happens:**
- After 14 days, you receive a reminder comment

**What to do:**
- Mark as "Ready for review" if complete
- Add a comment about current status
- Close if no longer needed

## 📊 Monitoring

### View Workflow Runs
1. Go to repository's **Actions** tab
2. Select workflow to see runs
3. Click on a run to see details

### Check PR Automation Activity
- Look for bot comments on PRs
- Check labels applied automatically
- Review workflow run logs for details

## 🐛 Troubleshooting

### PR not auto-updating
**Possible causes:**
- Merge conflicts exist
- Workflow permissions issue
- Branch protection rules

**Solutions:**
- Resolve conflicts manually
- Check Actions tab for errors
- Verify workflow has write permissions

### Labels not applied
**Possible causes:**
- File paths don't match patterns
- Workflow hasn't run yet

**Solutions:**
- Check `.github/labeler.yml` patterns
- Manually trigger "PR Auto Sync" workflow
- Check workflow run logs

### Reviewer not auto-assigned
**Possible causes:**
- PR author is the repository owner
- PR author is a bot

**Solutions:**
- This is expected behavior
- Manually request reviewers if needed

## 💡 Pro Tips

1. **Use descriptive commit messages** - They appear in the PR timeline
2. **Keep PRs focused** - Smaller PRs get reviewed faster
3. **Respond to automation feedback** - It helps maintain PR health
4. **Use draft PRs liberally** - Great for WIP without notifications
5. **Add context in comments** - Explain complex changes
6. **Link related issues** - Use "Fixes #123" in description
7. **Use checklists** - Automation tracks your progress
8. **Review labels regularly** - They provide quick status overview

## 🔗 Related Documentation

- [GitHub Actions Documentation](.github/README.md)
- [Repository README](README.md)
- [Contributing Guidelines](CONTRIBUTING.md) *(if exists)*

## 🆘 Getting Help

If you encounter issues with the automation:
1. Check the Actions tab for workflow errors
2. Review this guide for common scenarios
3. Open an issue with the `workflows` label
4. Contact the repository maintainers

---

**Last Updated:** 2026-02-15

**Automation Version:** 1.0.0
