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

## Scenario 3: Self-Hosted GitHub Actions Runner `/var/run/docker.sock` Permission Denied
**Q:** You deployed a GitHub Actions self-hosted runner on an AWS EC2 instance. When the workflow runs `docker build`, it fails with `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock`. How do you fix this permanently?
**A:** The system user running the GitHub Actions runner agent (`runner` / `ubuntu`) does not belong to the host system's `docker` group.
```bash
sudo usermod -aG docker github-runner
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart docker
```
Restart the runner service: `sudo ./svc.sh restart`.

## Scenario 4: Passing Job Outputs Between GitHub Actions Jobs
**Q:** Job 1 (`build`) generates a dynamic Docker image tag based on Git commit SHA (`${{ github.sha }}`). How do you pass this dynamic tag to Job 2 (`deploy`) in GitHub Actions?
**A:** Define `outputs` at the job level and use `$GITHUB_OUTPUT`:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.tag.outputs.sha_short }}
    steps:
      - id: tag
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: self-hosted
    steps:
      - run: echo "Deploying tag: ${{ needs.build.outputs.image_tag }}"
```

## Scenario 5: SHA Image Tagging vs `latest` Tag Anti-Pattern
**Q:** Why is using `:latest` Docker image tags dangerous in production automated CI/CD pipelines, and why should you use `${{ github.sha }}` instead?
**A:**
- `:latest` is mutable; multiple builds overwrite the same tag name, making rollbacks impossible and causing image caching issues on Kubernetes/EC2 hosts where nodes skip pulling updated images.
- Using Git commit SHA `${{ github.sha }}` guarantees immutability, 1-to-1 traceability from production code back to exact Git commits, and zero-downtime atomic rollbacks.

---

## Scenario 6-50 Summary Coverage Matrix
- **GitHub Actions Security:** `permissions: read-all` least privilege configs, GitHub Dependabot security alerts, OIDC role assumption (`aws-actions/configure-aws-credentials`).
- **DevSecOps Pipeline Gates:** SAST SonarQube quality gates, Trivy filesystem scans, OWASP ZAP DAST scans.
