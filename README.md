# 🧙‍♂️ Hogwarts Guide Bot (LLM-Powered Telegram Agent)

> A cloud-native, personalized wizarding world assistant running on Telegram, powered by LLM, Supabase, Redis, and automated via GitHub Actions CI/CD.

## 🌟 Key Features

- **Personalized LLM Persona:** Dynamic system prompts tailored to Hogwarts Houses (Gryffindor, Slytherin, Ravenclaw, Hufflepuff) for customized conversation tones.
- **Location & Route Guidance:** Natural language handling for interactive campus navigation and lore Q&A.
- **Match & Event Recommendations:** Instant matching with housemates and house-specific event discovery.
- **Performance Optimization:** Redis in-memory caching for low-latency response and database query reduction.

## 🛠️ Tech Stack & Architecture

- **Core Engine:** Python 3.12, Telegram Bot API, OpenAI/HKBU GPT API
- **Data & Caching:** Supabase (Cloud PostgreSQL), Redis (In-Memory Cache)
- **Containerization & Deployment:** Docker, Docker Compose, AWS EC2 (t3.micro)
- **DevOps & Observability:** GitHub Actions (CI/CD Pipeline), AWS CloudWatch

```text
[User] -> Telegram Bot -> Python Engine (Docker)
                               │
               ├── LLM API (HKBU GPT)
               ├── Caching (Redis Container)
               └── Database (Supabase PostgreSQL)
```

## 🚀 Quick Start (Local Development)

1. Clone the repository:
   ```bash
   git clone [https://github.com/BingbZHU/comp7940-lab.git](https://github.com/BingbZHU/comp7940-lab.git)
   cd comp7940-lab
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

## 🔄 CI/CD Pipeline

Automated deployment is configured via GitHub Actions. Any push to the main branch triggers automatic building, pushing to container registry, and redeployment onto the AWS EC2 instance.
