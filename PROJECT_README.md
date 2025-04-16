📚 Library Management System - README
# 📚 Library Management System (Microservices Architecture)
This project implements a modular Library Management System using microservices, Docker, Kubernetes, and GitHub Actions for CI/CD.
---
## 🔍 Overview
A scalable and secure Library Management System based on microservices architecture. Each service is independently deployable and managed.
---
## 📐 Architecture
- Services communicate over HTTP using REST APIs.
- JWT authentication for secured endpoints.
- Kubernetes DNS for service discovery.
- Minikube for local deployment.
---
## 🧩 Microservices
1. **User Service** – FastAPI
2. **Book Service** – FastAPI
3. **Borrowing Service** – Flask
Each service has its own MySQL database (polyglot persistence possible).
---
## 🛠️ Tech Stack
- FastAPI, Flask, SQLAlchemy
- Docker & Kubernetes (Minikube)
- MySQL, Prometheus, Grafana
- GitHub Actions for CI/CD
---
## 🗂️ Project Structure
```
LMS_Service/
│
├── user-service/
├── book-service/
├── borrowing-service/
├── k8s/
│   ├── user-service/
│   ├── book-service/
│   ├── borrowing-service/
│   ├── monitoring/
│   └── secrets/
├── .github/workflows/
│   └── ci-cd.yaml
├── docker-compose.yaml
└── README.md
```
---
## 🚀 Setup Instructions
### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/LMS_Service.git
cd LMS_Service
```
### 2. Start Minikube
```bash
minikube start
```
### 3. Use Docker with Minikube
```bash
minikube -p minikube docker-env --shell powershell | Invoke-Expression
```
### 4. Build Docker Images
```bash
docker build -t user-service:latest ./user-service
docker build -t book-service:latest ./book-service
docker build -t borrowing-service:latest ./borrowing-service
```
### 5. Apply Kubernetes Files
```bash
kubectl apply -f k8s/
```
### 6. Access Application
- Use `kubectl get svc` to get service IPs.
- Forward ports using:
```bash
kubectl port-forward svc/user-service 5001:5001
```
---
## 🔄 CI/CD Pipeline
- Triggered on push to `main`
- Actions:
  - Run unit tests
  - Build Docker images
  - Apply K8s manifests
- Demonstrates rolling updates
---
## 📡 API Endpoints
### User Service
- `POST /users/`
- `GET /users/`
- `GET /users/{id}`
- `PUT /users/{id}`
- `DELETE /users/{id}`
### Book Service
- `POST /books/`
- `GET /books/`
- `PUT /books/{id}`
- `DELETE /books/{id}`
- `PUT /books/borrow/{id}`
### Borrowing Service
- `POST /borrow`
- `PUT /return/{borrow_id}`

## 📡 Roles
 - Admin
 - Librarian
 - Student

## 🧪 Testing
- Unit tests with `pytest`
- Integration tests to simulate service interaction
- End-to-end tests validate complete flow
---
## 📊 Monitoring and Logging
- Prometheus + Grafana dashboards
- ELK stack (optional) for centralized logging
- Metrics exposed on `/metrics`
---
## 🔐 Security
- JWT for authentication
- Role-Based Access Control (RBAC)
- Secrets managed with Kubernetes
---

