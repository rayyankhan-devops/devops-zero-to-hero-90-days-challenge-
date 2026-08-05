# ☁️ Day 10: Git Advanced, AWS Cloud Fundamentals & Python OOP

On Day 10, I covered advanced Git merge/rebase workflows, foundational AWS Cloud architecture models, identity management (IAM), pricing models, and Object-Oriented Programming (OOP) in Python.

---

## 📝 Day 10 Notes (Visual)
![Day 10 Notes](day-10-notes.png)

---

> [!NOTE]
> **Day 10 Summary (Social Media Caption):**
> Day 10 of my 90 Days of DevOps challenge is officially in the books! Today's focus was all about advancing Git strategies, understanding AWS cloud deployment models, and writing object-oriented Python log analyzer engines.
> 
> **Key Learnings:**
> * **🔀 Git Merge vs. Rebase:** Mastered Merge commits vs linear Fast-Forward Rebase commits.
> * **☁️ AWS Fundamentals:** Explored Regions, Availability Zones (AZs), CapEx vs OpEx, and IaaS / PaaS / SaaS models.
> * **🔐 IAM Security:** IAM Users, Groups, Roles, Policies, and Root user security.
> * **🐍 Python OOP:** Built an object-oriented `LogAnalyzer` class to process server logs.

---

## 1. Advanced Git Workflows

### Merge vs. Rebase Comparison

| Feature | `git merge` | `git rebase` |
| :--- | :--- | :--- |
| **History Preservation** | Preserves full history with a dedicated merge commit. | Rewrites commit history linearly onto the target branch. |
| **Best Used For** | Public shared team branches (e.g. `main`). | Private feature branches before creating a Pull Request. |
| **Commands** | `git checkout main && git merge feature` | `git checkout feature && git rebase main` |

---

## 2. Cloud Computing & AWS Infrastructure

* **Public Cloud:** Infrastructure owned and managed by third-party cloud providers (AWS, Azure, GCP).
* **Private Cloud:** Cloud infrastructure dedicated strictly to a single organization (VMware, OpenStack).
* **Hybrid Cloud:** A combination of private infrastructure and public cloud resources.

### CapEx vs. OpEx Financial Models
* **CapEx (Capital Expenditure):** High upfront investment purchasing physical hardware, servers, and datacenter real estate. Requires ongoing maintenance.
* **OpEx (Operational Expenditure):** Pay-as-you-go cloud model. Low upfront cost; expenses scale dynamically with actual usage.

---

## 3. Python OOP (Object-Oriented Programming)

OOP allows organizing code into blueprints (**Classes**) and instances (**Objects**).

```python
class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

server1 = Server("web-prod-01", "192.168.1.50")
print(server1.name)
```

---

## 🛠️ Executable Practice Script

* **Python OOP Log Analyzer:** [log_analyzer_oop.py](log_analyzer_oop.py)

```bash
chmod +x log_analyzer_oop.py
python3 log_analyzer_oop.py
```

---

### 👤 Author / Contact
* **Muhammad Rayyan** | [GitHub](https://github.com/rayyankhan-devops) | [LinkedIn](https://www.linkedin.com/in/muhammad-rayyan-5645b1317/)

---

* [← Day 9: Git & AWS Automation](../day-09-git-aws-automation/README.md) | [Home](../README.md)
