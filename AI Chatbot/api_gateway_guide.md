# AWS API Gateway — Complete Guide for Beginners
> **Aviz Academy | Batch 8 | Instructor: Avinash Reddy**

---

## 🧠 What is API Gateway?

Think of API Gateway as the **front door of your application**.

When your app has a backend (Lambda, EC2, ECS, etc.), you don't expose it directly to users. Instead, you put API Gateway in front — it receives requests, routes them, and returns responses.

```
User/Client
    │
    ▼
API Gateway   ← (Front Door)
    │
    ▼
Backend (Lambda / EC2 / ECS / Any HTTP Endpoint)
```

**Real-world analogy:** API Gateway is like the receptionist at a hospital. You don't walk directly into the doctor's room. The receptionist checks who you are, directs you to the right doctor, and manages the flow.

---

## ⚡ API Gateway vs Load Balancer — Key Difference

| Feature | API Gateway | Load Balancer (ALB) |
|---|---|---|
| **Purpose** | Smart API management | Traffic distribution |
| **Routing** | By URL path + method (GET/POST) | By URL path only |
| **Auth** | Built-in (IAM, Cognito, JWT, API Key) | No built-in auth |
| **Throttling** | Yes (rate limiting per API key) | No |
| **Caching** | Yes (response caching) | No |
| **Request Transform** | Yes (modify req/res) | No |
| **WebSocket** | Yes | No |
| **Cost model** | Per million requests | Per hour + LCU |
| **Best for** | APIs, microservices, serverless | Web apps, EC2 fleets |

### 🎯 Simple Rule:
- Use **API Gateway** → when you need auth, throttling, transformations, or serverless backends
- Use **Load Balancer** → when you just need to distribute traffic across multiple EC2/ECS instances

---

## 📦 4 Types of APIs in API Gateway

### 1. 🔵 REST API (Classic)
**What it is:** The original, feature-rich API type.

**Use when:**
- You need **all features** — caching, request/response transformation, usage plans, API keys
- You're building a production-grade API
- You need **fine-grained control** over the request lifecycle

**Example project:** E-commerce product catalog API with caching and API key auth

```
GET /products          → Returns all products (cached for 5 min)
POST /orders           → Create an order (requires API Key)
```

**Cost:** Moderate — charged per request + data transfer

---

### 2. ⚡ HTTP API (New & Simple)
**What it is:** A lighter, cheaper, faster version of REST API.

**Use when:**
- You just need a **simple proxy** to Lambda or any HTTP backend
- You want **lower latency + lower cost** (up to 71% cheaper than REST API)
- You're doing JWT / OIDC auth (Cognito, Auth0)

**Example project:** Simple Lambda backend for a mobile app

```
GET /users/{id}    → Lambda → Returns user data
POST /login        → Lambda → Returns JWT token
```

**Cost:** Cheapest API Gateway option

> 💡 **Tip for students:** If REST API is a Swiss Army knife, HTTP API is a sharp kitchen knife — does the common job faster and cheaper.

---

### 3. 🔌 WebSocket API
**What it is:** Enables **two-way, real-time communication** between client and server.

**Use when:**
- Chat applications
- Live dashboards / stock price updates
- Multiplayer games
- Notifications (without polling)

**How it works:**
```
Client connects → WebSocket stays open → Server PUSHES data anytime
```

vs REST (client must keep asking):
```
Client: "Any new data?" → Server: "No"
Client: "Any new data?" → Server: "No"
Client: "Any new data?" → Server: "Yes, here it is"
```

**Example project:** Live chat app using Lambda + DynamoDB + WebSocket API

**Routes:**
```
$connect    → User joins the chat
$disconnect → User leaves
sendMessage → Send a message to all users
```

---

### 4. 🔒 REST API Private
**What it is:** A REST API that is **only accessible from within your VPC** — not from the public internet.

**Use when:**
- Internal microservices that should NOT be public
- Backend services accessed only by other services inside VPC
- Compliance/security requirements (banking, healthcare)

**How it works:**
```
VPC → Interface Endpoint (VPC Endpoint) → Private REST API → Lambda/EC2
```

**Example project:** Internal HR system — accessible only from office VPC, not from internet

> 🔐 Even if someone knows your API URL, they cannot reach it from outside the VPC.

---

## 🆚 Quick Comparison — All 4 Types

| | REST API | HTTP API | WebSocket API | REST API Private |
|---|---|---|---|---|
| **Direction** | Request/Response | Request/Response | Two-way | Request/Response |
| **Real-time** | ❌ | ❌ | ✅ | ❌ |
| **Publicly accessible** | ✅ | ✅ | ✅ | ❌ (VPC only) |
| **Caching** | ✅ | ❌ | ❌ | ✅ |
| **Cheapest** | ❌ | ✅ | — | ❌ |
| **All features** | ✅ | Subset | Subset | ✅ |
| **Use case** | Full-featured API | Simple/fast API | Live/real-time | Internal services |

---

## 📌 When to Use What — Decision Tree

```
Do you need real-time, two-way communication?
    YES → WebSocket API
    NO  ↓

Should the API be accessible ONLY from inside VPC?
    YES → REST API Private
    NO  ↓

Do you need caching, usage plans, or request transformation?
    YES → REST API
    NO  → HTTP API (cheaper + faster)
```

---

## 💰 Cost Tip (ap-south-1 — Mumbai)

| Type | Approx Cost |
|---|---|
| HTTP API | ~$1 per million requests |
| REST API | ~$3.50 per million requests |
| WebSocket API | ~$1 per million messages |
| REST API Private | ~$3.50 per million requests + VPC Endpoint cost |


---

*Aviz Academy — Learn by Doing, Not Just Watching 🚀*
*avizacademy.com | @avizway | Batch 8*
