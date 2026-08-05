# 🛡️ Day 11: DevSecOps Fundamentals, OWASP Threat Dragon & GitHub Security

On Day 11, I focused on integrating security into every phase of the software development lifecycle (Shift-Left DevSecOps), threat modeling, Gitleaks secret detection, Trivy vulnerability scanning, and GitHub Secrets vs. Environment Variables.

---

## 📝 Day 11 Notes (Visual)
![Day 11 Notes](day-11-notes.png)

---

> [!NOTE]
> **Day 11 Summary (Social Media Caption):**
> Day 11 of my 90 Days of DevOps challenge is complete! Security isn't a feature you add at the end—it's a mindset that starts on Day 1.
> 
> **Key Takeaways:**
> * **🛡️ DevSecOps & Threat Modeling:** Mastered OWASP Threat Dragon and Shift-Left principles.
> * **🔍 Secrets Scanning:** Configured Gitleaks to detect hardcoded API keys and DB credentials.
> * **📦 Vulnerability Scanning:** Utilized Trivy to scan filesystems, container images, and IaC templates.
> * **🔐 GitHub Secrets vs. Env Vars:** Managed sensitive credentials in CI/CD pipelines safely.

---

## 1. What is DevSecOps?

DevSecOps embeds security testing directly into software development pipelines rather than leaving audit reviews until post-deployment.

`Develop -> Secure (SAST/SCA) -> Operate -> Deliver`

---

## 2. GitHub Secrets vs. Environment Variables

| Feature | GitHub Secrets | GitHub Environment Variables |
| :--- | :--- | :--- |
| **Visibility** | Encrypted & Masked in build logs (`***`). | Plain text visible in console logs. |
| **Purpose** | API Keys, DB Passwords, Cloud Credentials. | Non-sensitive configs (`APP_ENV=prod`, `PORT=8080`). |
| **Usage** | `${{ secrets.AWS_ACCESS_KEY_ID }}` | `${{ vars.ENVIRONMENT_NAME }}` |

---

## 🛠️ Executable Practice Script

* **DevSecOps Security Scanner:** [security_scanner.sh](security_scanner.sh)

```bash
chmod +x security_scanner.sh
./security_scanner.sh
```

---

### 👤 Author / Contact
* **Muhammad Rayyan** | [GitHub](https://github.com/rayyankhan-devops) | [LinkedIn](https://www.linkedin.com/in/muhammad-rayyan-5645b1317/)

---

* [← Day 10: Git & AWS OOP](../day-10-git-aws-python-oop/README.md) | [Home](../README.md)
