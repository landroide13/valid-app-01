# 🚀 Valid — B2B SaaS Validation Platform

**Valid** is a Django-based web application designed to help B2B SaaS founders validate their ideas by connecting with real SME operators (potential early customers).

Instead of building blindly, founders can launch **validation campaigns**, attract **intro requests**, and track real engagement (calls, pilots, outcomes).

---

## ✨ Core Idea

> Build less. Validate faster. Talk to real users early.

Valid creates a structured environment where:

* Founders publish **validation campaigns**
* SMEs discover relevant tools early
* Both sides connect through controlled **intro requests**
* Engagement is tracked in a simple workflow

---

## 🧩 Features

### 👨‍💻 For Founders

* Create validation campaigns
* Define:

  * Problem
  * Solution
  * Target industry, role, company size
  * Validation goal (e.g. number of calls or pilots)
* Submit campaigns for review (admin moderation)
* Receive intro requests from SMEs
* Accept or reject requests
* Track engagement:

  * Discovery calls
  * Pilot discussions
  * Outcomes (LOI, deposit, etc.)

---

### 🏢 For SMEs (Operators / Early Adopters)

* Browse live campaigns
* Filter by:

  * Industry
  * Role
  * Market
* Request introduction to founders
* Track status of requests:

  * Requested
  * Accepted
  * Rejected

---

### 🛠 Platform Features

* Role-based system:

  * Founder
  * SME
* Authentication (signup, login, profile)
* Auto profile creation via signals
* Django admin for moderation:

  * Approve campaigns
  * Manage users
  * Monitor activity
* Clean dashboard for both roles
* Bootstrap UI with:

  * Landing page
  * Carousel
  * Feature sections
* Structured validation workflow

---

## 🧠 Product Philosophy

Valid is not:

* a marketplace
* a CRM
* a messaging platform

Valid is:

> A **validation engine** for early-stage SaaS ideas.

It focuses on:

* signal > noise
* quality > quantity
* structured interaction > random outreach

---

## 🏗 Architecture

### Backend

* Django (server-rendered)
* PostgreSQL (recommended)
* Django ORM
* Django auth system

### Frontend

* Django Templates
* Bootstrap 5

### Key Components

* Models:

  * `Profile`
  * `Campaign`
  * `IntroRequest`
  * `CampaignEngagement`

* Forms:

  * Signup
  * Campaign creation
  * Engagement tracking

* Views:

  * Public campaign browsing
  * Founder dashboard
  * SME dashboard

---

## 📚 Glossary

This platform uses specific terminology — here’s what everything means:

---

### 🟦 Campaign

A **validation campaign** created by a founder.

**Purpose:**
Test whether a SaaS idea solves a real problem.

**Contains:**

* Problem description
* Proposed solution
* Target users
* Validation goal

👉 Aka:

* Validation campaign
* SaaS validation post

---

### 🟩 Intro Request

An SME’s request to connect with a founder.

**Purpose:**
Express real interest in exploring the solution.

👉 Aka:

* Connection request
* Intro
* Lead (but more qualified)

---

### 🟨 Campaign Engagement

Tracks what happens **after an intro is accepted**.

**Includes:**

* Discovery call scheduled
* Call completed
* Outcome (pilot, follow-up, etc.)

👉 Aka:

* Validation outcome
* Deal progression (early stage)

---

### 🟪 Founder

A user who:

* builds a SaaS product
* creates campaigns
* receives intro requests

👉 Aka:

* SaaS builder
* Startup founder

---

### 🟫 SME (Small/Medium Enterprise)

A user who:

* operates a business
* may become a customer
* requests intros

👉 Aka:

* Operator
* Early adopter
* Potential customer

---

### 🎯 Validation Goal

The measurable objective of a campaign.

Examples:

* 10 discovery calls
* 5 pilot customers
* 3 LOIs

👉 Aka:

* Success metric
* Validation target

---

### 🧪 Validation

The process of confirming:

* the problem is real
* people care
* they are willing to act

👉 Aka:

* Market validation
* Problem-solution fit

---

## 🔄 Workflow Overview

1. Founder signs up
2. Founder creates campaign
3. Admin approves → campaign goes live
4. SME browses campaigns
5. SME sends intro request
6. Founder accepts or rejects
7. If accepted → engagement tracked
8. Founder learns from real interactions

---

## 🚧 MVP Scope

This project is intentionally **simple**:

* No messaging system
* No payments
* No notifications system (yet)
* No AI matching (yet)

Focus = **real validation, fast**

---

## 🚀 Future Improvements

* Smart matching (AI or rule-based)
* Email notifications
* Campaign analytics dashboard
* Stripe integration (paid campaigns)
* Multi-language (EN/FR/DE)
* API + React/Next frontend

---

## ⚙️ Setup (Quick Start)

```bash
# create virtualenv
python -m venv venv
source venv/bin/activate

# install dependencies
pip install django

# migrate database
python manage.py migrate

# create superuser
python manage.py createsuperuser

# run server
python manage.py runserver
```

Then open:

```
http://localhost:8000/valid/
```

---

## 🧑‍💼 Admin Access

Go to:

```
/admin/
```

You can:

* approve campaigns (set status = live)
* manage users and profiles
* view intro requests and engagements

---

## 💡 Final Thought

> Most SaaS products fail because they are built before being validated.

Valid exists to flip that:

👉 Talk first. Build later.
👉 Validate before scaling.

---
