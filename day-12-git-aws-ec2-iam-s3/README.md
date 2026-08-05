# ⚡ Day 12: Advanced Git & AWS EC2, IAM and S3

On Day 12, I explored advanced Git manipulation tools (`git reset`, `git revert`, `git cherry-pick`, `git stash`, `git blame`, Git hooks) and core AWS compute (EC2), identity access controls (IAM), and Object Storage (S3).

---

## 📝 Day 12 Notes (Visual)
![Day 12 Notes](day-12-notes.png)

---

> [!NOTE]
> **Day 10 Summary (Social Media Caption):**
> Day 12 of my 90 Days of DevOps challenge is complete! Understanding advanced Git commands and AWS foundational services is essential for managing production infrastructure.
> 
> **Key Topics:**
> * **🔀 Git Reset Modes:** `--soft`, `--mixed`, and `--hard` reset differences.
> * **📍 Git Commands:** `git cherry-pick`, `git stash`, `git revert`, `git blame`, and Git Hooks.
> * **☁️ AWS EC2 & IAM:** Launched EC2 instances via SSH, managed IAM Users, Groups, Roles, Policies.
> * **📦 Amazon S3:** Executed CLI commands (`aws s3 mb`, `aws s3 cp`, `aws s3 ls`, `aws s3 rm`).

---

## 1. Git Reset Comparison Matrix

| Reset Flag | Staging Area (Index) | Working Directory | History (HEAD) |
| :--- | :--- | :--- | :--- |
| **`git reset --soft HEAD~1`** | **Kept** (Staged) | **Kept** (Unchanged) | Moved back |
| **`git reset --mixed HEAD~1`** | **Unstaged** | **Kept** (Unchanged) | Moved back |
| **`git reset --hard HEAD~1`** | **Destroyed** | **Destroyed** | Moved back |

---

## 2. AWS S3 CLI Quick Reference

```bash
# Create Bucket
aws s3 mb s3://rayyan-devops-bucket-2026

# Upload File
aws s3 cp app.log s3://rayyan-devops-bucket-2026/

# List Bucket Contents
aws s3 ls s3://rayyan-devops-bucket-2026/

# Remove File
aws s3 rm s3://rayyan-devops-bucket-2026/app.log
```

---

## 🛠️ Executable Practice Script

* **AWS EC2 & S3 Manager Script:** [ec2_s3_manager.py](ec2_s3_manager.py)

```bash
chmod +x ec2_s3_manager.py
python3 ec2_s3_manager.py
```

---

### 👤 Author / Contact
* **Muhammad Rayyan** | [GitHub](https://github.com/rayyankhan-devops) | [LinkedIn](https://www.linkedin.com/in/muhammad-rayyan-5645b1317/)

---

* [← Day 11: DevSecOps & Security](../day-11-devsecops-github-security/README.md) | [Home](../README.md)
