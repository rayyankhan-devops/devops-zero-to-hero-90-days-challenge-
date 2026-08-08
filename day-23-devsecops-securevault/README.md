# 🔐 Day 23: DevSecOps: Hardening, Optimizing & Securing SecureVault

On Day 23, I completed a full DevSecOps security hardening and optimization of **SecureVault**—a production-inspired microservices platform containing Authentication, Notes, Tasks, PostgreSQL 16, and a React SPA frontend.

---

## 📝 Day 23 Notes & Architecture (Visual)
![SecureVault Compose Architecture](SecretVault-devsecops/images/docker%20compose%20secure%20vault.png)
![Nginx Gateway Flow](SecretVault-devsecops/images/nginx-html-css-js.png)
![Shell Deployment Automation](SecretVault-devsecops/images/shell%20to%20run%20all%20the%20containers%20at%20once%20after%20building.png)

---

> [!NOTE]
> **Day 23 Summary (Social Media Caption):**
> Day 23 of my 90 Days of DevOps challenge is complete! Containerizing an application is only the beginning—making containers lightweight, secure, non-root, and operationally efficient is what truly matters in DevSecOps.
> 
> **Key Achievements:**
> * **🛡️ Security Hardening:** Eliminated 235+ OS and Python vulnerabilities (Achieved **0 Critical**, **0 High**, **0 OS** vulnerabilities).
> * **📦 Image Sizing Optimization:**
>   - **Frontend SPA:** ~97 MB → **15 MB** (~85% smaller)
>   - **Python Microservices:** ~170 MB → **60 MB** (~65% smaller)
> * **🔒 Least Privilege Access:** Enforced non-root user execution across every container with dedicated service UIDs.
> * **🌐 Reverse Proxy Routing:** Configured Nginx as API Gateway routing `/api/auth`, `/api/notes`, and `/api/tasks`.

---

## 1. Vulnerability Elimination Metrics & Optimization

| Microservice | Base Image before | Hardened Base Image | Initial Size | Optimized Size | Size Reduction | Security Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend SPA** | `node:20` | `nginx:alpine` | ~97 MB | **15 MB** | **85% Smaller** | 0 Vulnerabilities |
| **Auth Service** | `python:3.11` | `python:3.11-alpine` | ~170 MB | **60 MB** | **65% Smaller** | 0 Critical / 0 High |
| **Notes Service** | `python:3.11` | `python:3.11-alpine` | ~170 MB | **60 MB** | **65% Smaller** | 0 Critical / 0 High |
| **Tasks Service** | `python:3.11` | `python:3.11-alpine` | ~170 MB | **60 MB** | **65% Smaller** | 0 Critical / 0 High |

### Applied Hardening Techniques
1. **Multi-Stage Docker Builds:** Isolated compile-time build dependencies from final runtime images.
2. **Bytecode Suppression:** Disabled Python compilation (`PYTHONDONTWRITEBYTECODE=1`) and stripped binaries using `strip`.
3. **Dependency Vulnerability Patches:** Patched transitive vulnerabilities across `Flask`, `Werkzeug`, `Flask-CORS`, `PyJWT`, and `setuptools` using Trivy and Docker Scout.
4. **Non-Root UIDs:** Configured `USER 10001` across all microservices.

---

## 🌐 Microservices Architecture & Network Gateway

```
                             [ User Browser ]
                                    |
                                    v Port 80
                        [ Nginx API Gateway Proxy ]
                        /           |           \
           /api/auth   /  /api/notes|            \ /api/tasks
                      v             v             v
             [ Auth Service ] [ Notes Service ] [ Tasks Service ]
                      \             |             /
                       v            v            v
                         [ PostgreSQL 16 Alpine ] (Vol: postgres_data)
```

---

## 🚀 How to Run SecureVault Microservices

```bash
cd day-23-devsecops-securevault/SecretVault-devsecops

# Run automated smart deployment script
chmod +x run-services.sh
./run-services.sh
```

---

## 🔗 Project Repositories
* **GitHub Repository:** [SecretVault-devsecops](https://github.com/rayyankhan-devops/SecretVault-devsecops) (forked from `aqsa890/SecretVault-devsecops`)

---

### 👤 Author / Contact
* **Muhammad Rayyan** | [GitHub](https://github.com/rayyankhan-devops) | [LinkedIn](https://www.linkedin.com/in/muhammad-rayyan-5645b1317/)

---

* [← Day 22: Docker Compose & DevBoard](../day-22-docker-compose-devboard/README.md) | [Home](../README.md)
