<div align="center">

# 🇬🇧 CoderCo Containers Challenge

**A multi-container Flask + Redis application, built with Docker, Compose, Nginx, and a London soul.**

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)

*Rachida · Docker & DevOps Challenge*

</div>

---

## 📖 What This Project Does

A tiny web application with two pages:

- **`/`** — A welcome page with a London skyline, Big Ben, and a friendly greeting.
- **`/count`** — A visit counter. Every refresh adds **1** to the count, stored in Redis.

The whole thing runs in **Docker**, orchestrated by **Docker Compose**, served through **Nginx** as a load balancer, with **3 scaled Flask instances** behind it.

**Live at:** `http://127.0.0.1:5000/`

---

## 🏗️ Architecture

```
Browser
   │
   ▼
localhost:5000
   │
   ▼
┌─────────────────┐
│   Nginx         │   ← Load balancer (front door)
│   port 80       │
└────────┬────────┘
         │  round-robin
   ┌─────┼─────┐
   ▼     ▼     ▼
┌────┐ ┌────┐ ┌────┐
│web1│ │web2│ │web3│   ← 3 scaled Flask containers
└──┬─┘ └──┬─┘ └──┬─┘
   └──────┼──────┘
          ▼
      ┌───────┐
      │ Redis │           ← Shared counter + persistent volume
      └───────┘
```

---

## 📁 Project Structure

```
challenge/
├── app.py                 # Flask app (routes + Redis logic)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Builds the Flask image
├── docker-compose.yml     # Orchestrates nginx + web + redis
├── nginx.conf             # Load balancer configuration
├── screenshots/           # Demo images for this README
└── README.md              # ← You are here
```

---

## 🧩 The Four Files Explained

### 1. `app.py` — The Flask Application

Two routes:

| Route | What It Does |
|:------|:-------------|
| `/` | Returns a styled London-themed welcome page |
| `/count` | Increments a Redis counter and displays the new value |

The Redis connection is **read from environment variables** — no hardcoding:

```python
host_value = os.getenv("REDIS_HOST", "redis")
port_value = int(os.getenv("REDIS_PORT", "6379"))
client = redis.Redis(host=host_value, port=port_value, decode_responses=True)
```

### 2. `Dockerfile` — The Recipe

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**Why `COPY requirements.txt` comes first:** Docker caches each build step. If `requirements.txt` hasn't changed, `pip install` is skipped on rebuild — making rebuilds 10× faster.

### 3. `docker-compose.yml` — The Conductor

Three services:

| Service | Role | Ports |
|:--------|:-----|:------|
| `nginx` | Load balancer | `5000:80` (only one exposed to host) |
| `web` | Flask app (scaled ×3) | internal only |
| `redis` | Key-value store | internal only |

### 4. `nginx.conf` — The Load Balancer

```nginx
upstream flask_backend {
    server web:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://flask_backend;
    }
}
```

**Translation:** *"Listen for visitors on port 80, and pass them all to the group of Flask apps named `web`."*

---

## 🚀 How to Run It

```bash
docker compose up -d --build --scale web=3
```

Open **`http://localhost:5000/`** in your browser.

**To tear down:**
```bash
docker compose down
```

**To tear down and wipe the Redis volume:**
```bash
docker compose down -v
```

---

# 🧪 Testing — Step by Step

---

## ✅ Step 1: The Core App (Flask + Redis + Compose)

**Goal:** Get Flask talking to Redis inside a Docker network.

**Commands:**
```bash
docker compose up -d
docker compose ps
```

**What you should see:** Two containers (`web`, `redis`) both `Up`.

### 📸 Demo — Two Containers Running

![Core app running with two containers](screenshots/step1-docker-ps.png)

> *Both `challenge-web-1` and `challenge-redis-1` are up. The `web` service exposes `0.0.0.0:5000->5000/tcp`.*

### 📸 Demo — Welcome Page

![Welcome page](screenshots/step1-homepage-simple.png)

> *`http://127.0.0.1:5000/` returns the welcome message.*

### 📸 Demo — Counter Page Increments

![Count page after first visit](screenshots/step1-count-1.png)

> *`http://127.0.0.1:5000/count` shows "This webpage has been viewed 1 time(s)."*

**What it proved:** Flask can reach Redis via Docker's internal network using the **service name** as hostname.

---

## ✅ Step 2: Redis Persistence

**Goal:** Make the counter survive container restarts.

**Commands:**
```bash
docker compose up -d
# Visit /count a few times — note the number (e.g., 18)
docker compose down
docker compose up -d
# Visit /count again — should continue from 18, not reset to 1
```

**Verify the volume exists:**
```bash
docker volume ls
```

You should see something like `challenge_myvol`.

### 📸 Demo — Volume Registered

![Docker volume list showing myvol](screenshots/step2-volume-ls.png)

> *Docker confirms the named volume exists.*

### 📸 Demo — Counter Persisted After Restart

![Counter page after restart](screenshots/step2-count-persisted.png)

> *After `docker compose down` and `up`, the counter continues from the previous value — the volume is doing its job.*

**What it proved:** A **named volume** mounted at `/data` outlives the container, so Redis data survives.

---

## ✅ Step 3: Environment Variables (The Proof Test)

**Goal:** Prove Flask is genuinely reading `REDIS_HOST` from the environment.

**Step A — Break it on purpose:**

In `docker-compose.yml`, change:
```yaml
REDIS_HOST: redis
```
to:
```yaml
REDIS_HOST: wrong_host
```

Rebuild:
```bash
docker compose up -d --build
```

### 📸 Demo — The Proof Test Fails as Expected

![Internal Server Error with wrong_host](screenshots/step3-wrong-host-browser.png)

> *The browser shows "Internal Server Error" — Flask couldn't reach the unreachable `wrong_host`.*

**Step B — Confirm the cause in logs:**

```bash
docker logs challenge-web-1
```

### 📸 Demo — Error Message Names the Wrong Host

![Docker logs showing ConnectionError to wrong_host](screenshots/step3-wrong-host-logs.png)

> *The logs read `redis.exceptions.ConnectionError: Error -2 connecting to wrong_host:6379. Name or service not known.` — proof that the value came from the env var, not the fallback.*

**Step C — Fix it back:**

```yaml
REDIS_HOST: redis
```
```bash
docker compose up -d --build
```

**What it proved:** Changing the env var changed the app's behavior. The env var is genuinely consumed.

---

## ✅ Step 4: Nginx Load Balancing (Bonus 3)

**Goal:** Serve the app through Nginx with 3 scaled Flask instances.

**Commands:**
```bash
docker compose down
docker compose up -d --build --scale web=3
docker compose ps
```

**What you should see:** 5 containers:
- 1 × `challenge-nginx-1` — Up, `0.0.0.0:5000->80/tcp`
- 3 × `challenge-web-1/2/3` — Up, `5000/tcp` (internal only)
- 1 × `challenge-redis-1` — Up

### 📸 Demo — 5 Containers Up

![Docker PS showing nginx + 3 web + redis](screenshots/step4-docker-ps-5-containers.png)

> *Notice only `nginx` is bound to the host (`0.0.0.0:5000->80/tcp`). The three `web` containers only expose `5000/tcp` internally — no host binding, no port conflict.*

### 📸 Demo — Compose Output During Scaling

![Compose output showing 3 web containers created](screenshots/step4-compose-scale-output.png)

> *Compose creates `web-1` through `web-4` (one leftover + three new) and `nginx-1`.*

### 📸 Demo — Counter Still Works Through Nginx

![Count page served through Nginx](screenshots/step4-count-through-nginx.png)

> *Refreshing `/count` still increments. All three Flask containers share the same Redis, so the count is consistent.*

**What it proved:** Nginx receives on port 5000 and distributes traffic across the 3 Flask containers. Redis is the single source of truth for the counter.

---

## 🎨 The London Custom Theme

Both pages use a London night-sky aesthetic:

| Element | Description |
|:--------|:------------|
| **Background** | Deep twilight gradient (`#0f172a → #334155`) |
| **Skyline** | CSS-drawn buildings silhouette at the bottom |
| **Big Ben** | Animated glowing clock tower with pulsing amber light |
| **Stars** | Radial-gradient dots scattered across the sky |
| **Card** | White with a red top border (double-decker bus red) |
| **Accent color** | `#dc2626` (London red) |
| **Counter style** | Dark departure-board with glowing amber digits |

### 📸 Demo — Final Homepage (Custom London Theme)

![Final London homepage](screenshots/final-homepage.png)

> *"Hello, I'm Rachida" — with a skyline, Big Ben, and badges for London, Docker, Flask, Redis, and Nginx.*

### 📸 Demo — Final Count Page (Visit Pass Style)

![Final counter page as London visit pass](screenshots/final-count.png)

> *Ticket-style card with a "London · Visit Pass" stamp and a departure-board counter.*

**No images, no external assets — everything is pure CSS.** The container stays small and pages load instantly.

---

## 🧠 What I Learned

| Concept | Takeaway |
|:--------|:---------|
| **Docker networking** | Containers on the same network reach each other by service name (DNS) |
| **Named volumes** | Storage that outlives the container — essential for databases |
| **Bind mounts** | Mount a file from the host into a container (used for `nginx.conf`) |
| **Environment variables** | Keep config out of code — the same image runs in dev, staging, and prod |
| **`os.getenv("KEY", "default")` pattern** | Read env vars with safe fallbacks |
| **Docker build caching** | `COPY requirements.txt` before `RUN pip install` for fast rebuilds |
| **Horizontal scaling** | `--scale web=3` runs multiple instances of one service |
| **Fixed host ports block scaling** | Only one container can bind a host port — that's why `web` has no `ports:` |
| **Reverse proxy** | Nginx sits in front and forwards requests to backends |
| **Round-robin** | Nginx's default: cycle through backends evenly |
| **DNS round-robin** | Docker returns all container IPs for a scaled service name |

---

## 🐛 Common Issues & Fixes

| Symptom | Cause | Fix |
|:--------|:------|:----|
| `ModuleNotFoundError: No module named 'flask'` | Missing `Flask` in `requirements.txt` | Add it and rebuild |
| `redis.exceptions.ConnectionError` | Wrong `REDIS_HOST` | Set `REDIS_HOST: redis` in Compose |
| `Bind for 0.0.0.0:5000 failed: port is already allocated` | `web` still has `ports:` | Remove `ports:` from `web` when scaling |
| `502 Bad Gateway` from Nginx | Nginx can't reach Flask | Check `web:5000` in `nginx.conf` matches service name + port |
| `python: can't open file '/app/app.py'` | File name mismatch | Rename your file to `app.py` and update the Dockerfile `CMD` |
| Counter resets after restart | Volume not mounted | Add `volumes: - myvol:/data` and top-level `volumes: myvol:` |

**#1 debugging command:**
```bash
docker compose logs
```

---

## 🛠️ Command Cheat Sheet

| Task | Command |
|:-----|:--------|
| Start everything | `docker compose up -d` |
| Start with rebuild | `docker compose up -d --build` |
| Start with 3 web instances | `docker compose up -d --scale web=3` |
| Stop and remove | `docker compose down` |
| Stop + wipe volumes | `docker compose down -v` |
| Check running containers | `docker compose ps` |
| View logs (all) | `docker compose logs` |
| View logs (one service) | `docker compose logs nginx` |
| List volumes | `docker volume ls` |
| Inspect a volume | `docker volume inspect challenge_myvol` |

---

## 🎯 Challenge Checklist

### Core Requirements
- [x] Flask app with `/` and `/count` routes
- [x] Redis stores the visit count
- [x] Both services Dockerized
- [x] Docker Compose manages both
- [x] Custom network between services

### Bonus 1 — Persistent Redis
- [x] Named volume `myvol` mounted at `/data`
- [x] Counter survives `docker compose down` + `up`

### Bonus 2 — Environment Variables
- [x] Redis host/port read from env vars
- [x] `environment:` block in Compose
- [x] Proof test: breaking `REDIS_HOST` breaks the app

### Bonus 3 — Scaling + Load Balancing
- [x] Nginx service as reverse proxy
- [x] `--scale web=3` runs 3 Flask instances
- [x] No host port on `web` — Nginx owns port 5000
- [x] Round-robin across backends

---

<div align="center">

**Built with 🐳 Docker · 🐍 Flask · ⚡ Redis · 🌐 Nginx**

*Rachida · Docker & DevOps Challenge*

</div>
