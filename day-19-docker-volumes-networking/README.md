# 🔌 Day 19: Docker Deep-Dive, Storage Volumes & Networking

On Day 19, I mastered container data persistence using Docker Volumes and Bind Mounts, and explored Docker Networking Drivers (Bridge, Host, Overlay, None) enabling multi-container DNS resolution.

---

> [!NOTE]
> **Day 19 Summary (Social Media Caption):**
> Day 19 of my 90 Days of DevOps challenge is complete! Containers are ephemeral by default—understanding volumes for data persistence and custom networks for container isolation is mandatory for production.
> 
> **Key Focus Areas:**
> * **💾 Storage Persistence:** Docker Volumes vs. Bind Mounts vs. `tmpfs`.
> * **🌐 Networking Drivers:** Default Bridge, User-Defined Bridge, Host, Overlay (Swarm), and None.
> * **🔍 Container DNS:** Automatic name resolution across custom bridge networks.

---

## 1. Storage Drivers Comparison

| Feature | Docker Volumes | Bind Mounts | `tmpfs` Mounts |
| :--- | :--- | :--- | :--- |
| **Location** | Managed by Docker (`/var/lib/docker/volumes/`). | Anywhere on Host Filesystem (`/var/log`, `/home`). | Host System Memory (RAM). |
| **CLI Syntax** | `-v db-data:/var/lib/mysql` | `-v /host/path:/container/path` | `--tmpfs /app/cache` |
| **Best For** | Database storage & production persistence. | Live development source code syncing. | Sensitive temporary data. |

---

## 2. Docker Network Drivers

* **Bridge (Default):** Default isolation network for containers running on the same host.
* **User-Defined Bridge:** Custom bridge network providing automatic internal **DNS resolution** between containers by container name.
* **Host:** Removes network isolation; container shares host network stack directly (no port mapping needed).
* **Overlay:** Enables multi-host networking across multiple Docker daemons (used in Docker Swarm & Kubernetes).

---

## 🛠️ Executable Practice Script

* **Docker Volume & Network Practice:** [docker_volume_net_practice.sh](docker_volume_net_practice.sh)

```bash
chmod +x docker_volume_net_practice.sh
./docker_volume_net_practice.sh
```

---

### 👤 Author / Contact
* **Muhammad Rayyan** | [GitHub](https://github.com/rayyankhan-devops) | [LinkedIn](https://www.linkedin.com/in/muhammad-rayyan-5645b1317/)

---

* [← Day 18: SonarQube & SAST](../day-18-sast-sca-sonarqube/README.md) | [Home](../README.md)
