# 🐧 Day 2: Linux Basics & Foundational DevOps Concepts

On Day 2, I focused on the foundations. DevOps relies heavily on Linux systems, server administration, and secure cloud connectivity. Here are the core concepts and skills covered today.

---

## 1. UNIX vs. Linux

Understanding the origin of operating systems helps in recognizing the design decisions behind modern environments.
* **UNIX:** The original operating system developed in the **1960s** at AT&T Bell Labs. It introduced concepts like hierarchical file systems and pipes.
* **Linux:** A modern, open-source, Unix-like operating system kernel created by **Linus Torvalds** in 1991.
* **DevOps Context:** Linux is the backbone of the DevOps world, powering the vast majority of web servers, cloud infrastructure, and containerization platforms (Docker, Kubernetes).

---

## 2. Operating System, Kernel & Boot Loader

An operating system consists of multiple layers working together to translate user actions to hardware operations.

```
+---------------------------------------+
|              User / App               |
+---------------------------------------+
                   |
                   v
+---------------------------------------+
|          Operating System             |
|   +-------------------------------+   |
|   |            Kernel             |   |
|   +-------------------------------+   |
+---------------------------------------+
                   |
                   v
+---------------------------------------+
|               Hardware                |
+---------------------------------------+
```

* **Operating System (OS):** The software interface that sits between the user and the raw computer hardware.
* **Kernel:** The core of the OS. It directly interacts with the hardware, managing vital system resources (CPU, Memory, I/O devices, processes).
* **Boot Loader:** A small program that starts when the machine powers on. Its job is to initialize system memory and load the operating system Kernel into memory. An example is **GRUB** (Grand Unified Bootloader).

---

## 3. Basic Linux Commands

I practiced fundamental commands to navigate and manipulate the Linux filesystem.

| Command | Action / Purpose | Example Usage |
| :--- | :--- | :--- |
| `pwd` | Print Working Directory | `pwd` |
| `ls` | List files and directories | `ls -la` |
| `cd` | Change directory | `cd /var/log` |
| `mkdir` | Make a new directory | `mkdir project-dir` |
| `touch` | Create an empty file | `touch index.js` |
| `cp` | Copy files or directories | `cp config.json config.backup.json` |
| `mv` | Move or rename files | `mv oldname.txt newname.txt` |
| `rm` | Remove files or directories | `rm -rf tmp/` |
| `cat` | View file content directly in terminal | `cat app.log` |
| `less` | View file content interactively page by page | `less /var/log/syslog` |
| `head` | View the first few lines of a file | `head -n 10 info.txt` |
| `tail` | View the last few lines of a file | `tail -f app.log` (follow mode) |
| `grep` | Search for specific patterns in files | `grep "error" syslog` |
| `chmod` | Change file/directory permissions | `chmod 400 my-key.pem` |
| `ps` | List running processes | `ps aux` |
| `top` | Interactive system monitor | `top` |

---

## 4. SSH (Secure Shell)

**SSH** is a cryptographic network protocol used for secure operating system logins over an unsecured network.
* **Default Port:** `22`
* **Common Command:**
  ```bash
  ssh user@ip-address
  ```
* **SSH Config File (`~/.ssh/config`):** Used to manage multiple connections without memorizing IP addresses and keys.
  Example entry:
  ```text
  Host my-web-server
      HostName 54.210.12.34
      User ubuntu
      IdentityFile ~/.ssh/my-key.pem
  ```
  Now you can connect simply by typing: `ssh my-web-server`

---

## 5. AWS EC2 Setup

Launched a virtual server in the cloud (EC2 - Elastic Compute Cloud) on AWS:
1. **Choose AMI (Amazon Machine Image):** Selected the OS template (e.g., Ubuntu Server 22.04 LTS).
2. **Select Instance Type:** Chose the hardware specifications (e.g., `t2.micro` for free tier).
3. **Configure Security Group:** Opened inbound port `22` to allow SSH access.
4. **Review & Launch:** Configured the storage, generated keys, and launched the instance.

---

## 6. SSH Keys - Public & Private

SSH uses public-key cryptography to authenticate remote hosts.

```
       +---------------------------------------------+
       |                  KEY PAIR                   |
       +----------------------++---------------------+
                              ||
                              v
             +----------------++----------------+
             |   PUBLIC KEY   ||  PRIVATE KEY   |
             +----------------++----------------+
             | Can be shared  || Must be secret |
             | Encrypts data  || Decrypts data  |
             +----------------++----------------+
```

* **Public Key:** Stored on the remote server in `~/.ssh/authorized_keys`. It can be shared freely.
* **Private Key:** Kept securely on your local machine. **Never share this key!**
* **Generating a Keypair:**
  ```bash
  ssh-keygen -t rsa -b 4096 -C "rayyan@devops"
  ```
* **Accessing EC2:** The public key was added to the EC2 server, enabling secure passwordless login using the corresponding private key file.

---

## 💡 Today's Win
> **"Every expert was once a beginner. Keep showing up, learning something new, and progress over perfection!"**

---

### 👤 Author
* **Muhammad Rayyan**
* *Future DevOps Engineer in Progress* 👑

---

* [← Day 1: Intro](../day-01-intro/README.md) | [Home](../README.md) | [Day 3: Advanced Linux & LVM →](../day-03-linux-advanced-lvm/README.md)
