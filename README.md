# Jalaram Electric - Quick Reference Guide

## 1. Project Overview
A simple, beginner-friendly Django application matching the **Marwadi University ICT Sem-5 Python Framework** syllabus:
- **Model-View-Template (MVT)** architecture.
- Dual-tier pricing (**Retail** for everyday buyers, **Wholesale** for registered Electricians & Contractors).
- Fulfillment support: **In-Store Pickup** (quick counter collection) vs **Home / Site Delivery**.
- Inventory monitoring with low-stock alerts.
- Shopkeeper dashboard for quick price & stock updates without opening the terminal.
- Instant printable sales invoice / digital receipt.

---

## 2. Default Login Credentials

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Store Owner / Staff** | `admin` | `admin123` | Has access to Store, Dashboard (`/dashboard/`), and Django Admin (`/admin/`) |
| **Wholesale Contractor** | `ramesh_contractor` | `ramesh123` | Sees trade/wholesale discounts across all products |
| **New Customer** | Self-register | Any | Defaults to Retail pricing tier |

---

## 3. How to Run the Project

In this directory (`d:\ict\sem5\Python Framework`), start the local development server:
```powershell
python manage.py runserver
```
Open your browser and visit: **http://127.0.0.1:8000/**

---

## 4. Key Application URLs

- **Storefront & Catalog:** `http://127.0.0.1:8000/`
- **Cart:** `http://127.0.0.1:8000/cart/`
- **Checkout:** `http://127.0.0.1:8000/checkout/`
- **My Order History:** `http://127.0.0.1:8000/my-orders/`
- **Shopkeeper Dashboard:** `http://127.0.0.1:8000/dashboard/`
- **Django Admin:** `http://127.0.0.1:8000/admin/`
