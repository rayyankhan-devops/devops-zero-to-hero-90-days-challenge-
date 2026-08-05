# 🐙 Git, GitHub & DevSecOps Pipelines - 50 Scenario-Based Interview Questions

## Scenario 1: Accidental Secret Commit in Git History
**Q:** A developer accidentally committed an AWS Secret Access Key to a private Git repository 5 commits ago and pushed it to GitHub. Deleting the key from the latest file and committing does NOT remove it from history. How do you permanently purge it?
**A:**
1. Immediately revoke and rotate the leaked AWS key in AWS IAM!
2. Purge the secret from Git history using `git-filter-repo` or BFG Repo-Cleaner:
   ```bash
   git filter-repo --invert-paths --path path/to/secret_file
   ```
3. Force-push updated clean ref history to remote: `git push origin --force --all`
4. Implement **Gitleaks** or pre-commit hooks to block secrets before committing in the future.

## Scenario 2: Resolving Merge Conflicts During Rebase
**Q:** You ran `git rebase main` on your feature branch. Git pauses with `CONFLICT (content): Merge conflict in app.py`. What are the exact commands to resolve this safely?
**A:**
1. Open `app.py` and manually edit conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Stage resolved file: `git add app.py`
3. Continue rebase: `git rebase --continue` (Do NOT run `git commit`!).
4. If rebase gets completely corrupted, abort safely: `git rebase --abort`.

## Scenario 3: Recovering Lost Commits via Git Reflog
**Q:** A developer ran `git reset --hard HEAD~5` by mistake, losing 5 critical commits that were not pushed to GitHub. How do you recover those lost commits?
**A:** Use **Git Reflog** (reference log), which tracks every HEAD movement locally:
1. View reference log history: `git reflog`
2. Locate the commit hash prior to the bad reset (e.g. `HEAD@{1}` or `c7a1f2b`).
3. Restore branch pointer to that commit: `git reset --hard c7a1f2b` or `git checkout -b recovered-branch c7a1f2b`.

## Scenario 4: SonarQube Quality Gate Failing CI/CD Pipeline
**Q:** A GitHub Actions pipeline fails at the `SonarQube Analysis` step due to a Quality Gate failure ("Code Coverage on New Code is 45%, minimum required is 80%"). How do you handle this policy block?
**A:**
1. Do NOT bypass or lower Quality Gate standards in SonarQube settings.
2. Inspect SonarQube dashboard breakdown for untested functions.
3. Write required unit/integration test cases to raise coverage above 80%.
4. Commit and push tests to trigger green pipeline verification.

## Scenario 5: Managing Merge Conflicts Across Hotfixes & Release Branches
**Q:** A urgent hotfix was committed directly to `main`. Meanwhile, a feature branch branched off `main` two weeks ago is ready for merge. How do you incorporate the hotfix into the feature branch smoothly?
**A:**
1. Switch to feature branch: `git checkout feature/login`
2. Rebase onto updated main: `git rebase main` (or `git merge main`).
3. Resolve any conflicts, run test suites, and create a Pull Request to `main`.

## Scenario 6: Discarding Staged Changes vs Working Directory Changes
**Q:** You modified `database.py` and staged it (`git add database.py`). You also modified `server.py` but did not stage it. How do you unstage `database.py` while discarding changes in `server.py`?
**A:**
1. Unstage `database.py`: `git restore --staged database.py`
2. Discard working directory changes in `server.py`: `git restore server.py`

## Scenario 7: Automating DevSecOps Scans in GitHub Actions
**Q:** Write a GitHub Actions YAML job snippet that runs Trivy filesystem scan on every Pull Request and fails the pipeline if HIGH or CRITICAL vulnerabilities are found.
**A:**
```yaml
name: Security Audit
on: [pull_request]
jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy Vulnerability Scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          ignore-unfixed: true
          severity: 'HIGH,CRITICAL'
          exit-code: '1'
```

## Scenario 8: Git Cherry-Pick Specific Hotfix Commit
**Q:** You need a single bugfix commit (`a1b2c3d`) from branch `development` applied to release branch `v1.2-release` without bringing over 50 other unapproved commits.
**A:**
1. Switch to release branch: `git checkout v1.2-release`
2. Cherry-pick specific commit: `git cherry-pick a1b2c3d`
3. Resolve conflicts if any, and push: `git push origin v1.2-release`.

## Scenario 9: Jira Smart Commit Workflow
**Q:** How do you structure a Git commit message so that pushing it automatically transitions Jira ticket `DEV-404` to "In Code Review" and logs 2 hours of work?
**A:** Use Jira Smart Commit syntax:
```bash
git commit -m "DEV-404 #time 2h #comment Fixed session timeout bug #transition 'In Code Review'"
```

## Scenario 10: Git Hooks Pre-Commit Security Guard
**Q:** How do you enforce mandatory `gitleaks` scans locally on developers' machines before allowing any `git commit` to execute?
**A:** Create a `.git/hooks/pre-commit` script:
```bash
#!/bin/bash
if command -v gitleaks >/dev/null 2>&1; then
    gitleaks protect --staged --verbose
    if [ $? -ne 0 ]; then
        echo "❌ Gitleaks detected secrets in staged files! Commit aborted."
        exit 1
    fi
fi
```
Make executable: `chmod +x .git/hooks/pre-commit`.

---

## Scenario 11-50 Summary Coverage Matrix
- **Advanced Git:** Submodules vs Trees, `git bisect` binary search debugging, `git Stash pop` vs `apply`.
- **SAST & SCA Integration:** Snyk vulnerability remediations, OWASP ZAP DAST automation, Checkov IaC scanning.
