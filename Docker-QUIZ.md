<div align="center">

![Docker & DevOps Technical Quiz](https://media.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif)

# 🐳 Docker & DevOps — Technical Quiz

**A self-assessment covering the complete Docker learning journey**
From containerization basics → registries → Compose orchestration → multi-stage optimization

[![Made with Docker](https://img.shields.io/badge/Made%20with-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Questions](https://img.shields.io/badge/Questions-22-blue?style=for-the-badge)](#-contents)
[![Level](https://img.shields.io/badge/Level-Beginner→Intermediate-green?style=for-the-badge)](#-scoring-guide)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#-license)

</div>

---

> ### 💡 How to Use
> Try to answer each question **before** clicking the toggle. Answers are hidden so you can self-test honestly.
> **Score yourself** at the end using the [Scoring Guide](#-scoring-guide).

---

## 📑 Contents

| # | Section | Questions |
|:-:|:--------|:---------:|
| 🧠 | [Theory Quiz](#-theory-quiz) | 10 |
| 🛠️ | [Practical Quiz](#️-practical-quiz) | 12 |
| 📊 | [Scoring Guide](#-scoring-guide) | — |
| 🎯 | [Weak-Spot Cheat Sheet](#-weak-spot-cheat-sheet) | — |

---

<div align="center">

## 🧠 Theory Quiz

*Tests whether you understand **why** things work — not just **what** to type.*

</div>

---

### **Q1.** Why was port `5002` chosen instead of Flask's default port `5000`?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ C) A custom port chosen to avoid local host conflicts.**

Port `5000` is commonly used by other local apps (e.g., macOS AirPlay).

</details>

---

### **Q2.** Which Dockerfile instruction executes build commands during the *image compilation phase*?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `RUN`**

| Instruction | Phase |
|:------------|:------|
| `RUN` | **Build phase** |
| `CMD` | Runtime startup |
| `EXPOSE` | Documents the port only |
| `WORKDIR` | Sets working directory |

</details>

---

### **Q3.** Why does `docker rmi` sometimes refuse to delete an image?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ C) A stopped or active container is still referencing it.**

> **⚠️ Gotcha:** Cleanup order is always `stop` → `rm` → `rmi`.

</details>

---

### **Q4.** Which network driver *removes* network isolation entirely?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `host`**

> **🧠 Memory hook:** *bridge = builds a wall · host = shares the street · none = no doors.*

</details>

---

### **Q5.** What key capability do custom user-defined networks unlock?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) DNS resolution by container/service name.**

Containers on the same network reach each other by name (e.g., `web` → `mydb`) — no IP tracking needed.

</details>

---

### **Q6.** In what format must you tag an image before pushing to Docker Hub?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker build -t <username>/<repository>:<tag> .`**

The `<username>/` namespace tells Docker Hub which account owns the repo.

</details>

---

### **Q7.** Which command sequence correctly authenticates Docker CLI to AWS ECR?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B)**

```bash
aws ecr get-login-password --region <region> \
  | docker login --username AWS --password-stdin \
    <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

> **🧠 Key concept:** ECR uses **IAM-backed temporary tokens**, not long-lived passwords.

</details>

---

### **Q8.** What is the purpose of `depends_on` in `docker-compose.yml`?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) It specifies service startup dependencies and order.**

> **⚠️ Gotcha:** `depends_on` guarantees **start order**, NOT **readiness**. MySQL may take 10–30s to accept connections. Use healthchecks + `condition: service_healthy` in production.

</details>

---

### **Q9.** What primary problem do multi-stage builds solve?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ D) They isolate build dependencies in one stage and copy only final artifacts into a lean runtime stage.**

> **📊 Payoff:** `471 MB` → `151 MB` (~68% reduction).

</details>

---

### **Q10.** What does `COPY --from=build /app /app` accomplish?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) Copies compiled artifacts from the named `build` stage into the clean runtime stage, discarding compiler dependencies.**

> **🧠 Remember:** `--from=` sources from **another build stage**, not the host.

</details>

---

<div align="center">

## 🛠️ Practical Quiz

*Tests whether you could type the right command under pressure.*

</div>

---

### **Q1.** Build a Dockerfile in the current directory, tagged `hello-flask`.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker build -t hello-flask .`**

> **⚠️ Gotcha:** `-t` means **tag** in `docker build` but **TTY** in `docker run`.

</details>

---

### **Q2.** Run `hello-flask` in the background with host port `5002` mapped to container port `5002`.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker run -d -p 5002:5002 hello-flask`**

> **📌 Direction:** `-p <host_port>:<container_port>` — host on the left, container on the right.

</details>

---

### **Q3.** Show only *running* containers.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker ps`**

> **⚠️ Gotcha:** `docker ps -a` shows **all** containers (running + stopped).

</details>

---

### **Q4.** Remove two stopped containers with IDs `c123` and `c456` in one command.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ A) `docker rm c123 c456`**

> **🧠 Memory hook:** The **`i`** in **`rmi`** = **`i`**mage. No `i` = container.

</details>

---

### **Q5.** Reclaim disk space by removing stopped containers, unused networks, and dangling images in one shot.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker system prune`**

> **⚠️ Danger variants:** `-a` also removes all unused images · `--volumes` also removes volumes (data loss).

</details>

---

### **Q6.** Create custom network `myappnetwork` and run MySQL container `mydb` on it.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B)**

```bash
docker network create myappnetwork
docker run -d --name mydb --network myappnetwork mysql:8.4
```

> **📌 Note:** `--network` and `--net` are aliases. Both containers must join the **same** network for DNS by name.

</details>

---

### **Q7.** Push local image `flask-mysql:latest` to AWS ECR (account `123456789`, region `us-east-1`).

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B)**

```bash
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/flask-mysql:latest
```

> **🧠 Key concept:** The **image tag itself** tells Docker where to push. That's why `docker tag` is required before `docker push` to ECR.

</details>

---

### **Q8.** Launch the whole Compose stack in the background.

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `docker-compose up -d`**

> **⚠️ Gotcha:** `docker-compose down` keeps volumes and images by default. Add `-v` to wipe volumes.

</details>

---

### **Q9.** What happens when `web` has `depends_on: - mydb` and you run `docker-compose up -d`?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `mydb` starts before `web`, but `web` may still fail if `mydb` isn't *ready* to accept connections.**

> **⚠️ Golden distinction:** `depends_on` guarantees **started**, NOT **ready**.

</details>

---

### **Q10.** You rebuilt your image but the old container is still running. What's the correct fix?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B)**

```bash
docker stop <old_id> && docker rm <old_id>
docker run -d -p 5002:5002 hello-flask
```

> **🧠 Mental model:** Images are **templates** (immutable). Containers are **instances** frozen to their template. Rebuilding never updates running containers.
>
> **⚡ Compose shortcut:** `docker-compose up -d --build` handles this automatically.

</details>

---

### **Q11.** Which `docker run` flag sets an environment variable?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `-e MYSQL_ROOT_PASSWORD=my-secret-password`**

> **⚠️ Security:** `-e` secrets appear in `docker inspect` and shell history. Use Docker secrets or `--env-file` in production.

</details>

---

### **Q12.** In a multi-stage Dockerfile, how do you copy ONLY built artifacts from a stage named `build`?

<details>
<summary>👉 <strong>Reveal answer</strong></summary>

<br>

**✅ B) `COPY --from=build /app /app`**

> **⚠️ Gotcha:** The flag is `--from=`, not `--stage=`. Easy to mix up since we *call* it a "stage."

</details>

---

<div align="center">

## 📊 Scoring Guide

</div>

| Score | Level | What It Means |
|:-----:|:-----:|:--------------|
| **20–22** | 🏆 Advanced | Fluent in concepts and commands |
| **18–19** | 🥇 Intermediate | Strong foundation, minor gaps |
| **15–17** | 🥈 Intermediate-beginner | Can containerize apps; needs command practice |
| **10–14** | 🥉 Beginner | Review core modules before proceeding |
| **0–9** | 📖 Novice | Revisit the study notes from the start |

---

<div align="center">

## 🎯 Weak-Spot Cheat Sheet

*Four most commonly missed items across both quizzes.*

</div>

| # | Topic | Memory Hook |
|:-:|:------|:------------|
| 1 | **`rm` vs `rmi`** | The **`i`** in **`rmi`** = **`i`**mage. No `i` = container. |
| 2 | **Prune family** | `system` = everything · `image` / `container` / `network` / `volume` = just that thing. |
| 3 | **Rebuild workflow** | *"Build a new image → kill the old container → run a fresh one."* Images are **templates** (immutable). Containers are **instances** frozen to their template. |
| 4 | **Network drivers** | **bridge** = builds a wall (isolated) · **host** = shares the street (no isolation) · **none** = no doors. |

---

<div align="center">

### ⭐ Found this useful?

Star the repo · Share with a friend learning Docker · Open a PR with new questions

<sub>Quizzes derived from the *Complete Docker & DevOps Master Study Notes* — Modules 1–6.</sub>

</div>
