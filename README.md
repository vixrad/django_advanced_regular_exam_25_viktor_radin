VIKODINE is a Django-based SaaS platform designed for restaurant owners and customers. It allows restaurant owners to manage their profiles, menus, and reservations while giving customers an easy way to discover restaurants, book tables, and leave reviews.

---

## Features

- **Multi-role authentication**  
  Separate access for customers, restaurant owners, and administrators.

- **Restaurant management**  
  Owners can create and manage restaurant profiles, opening hours, and menus.

- **Reservation system**  
  Customers can book tables online and view their upcoming reservations.  
  Owners can confirm, cancel, or mark reservations as completed directly from their dashboard.

- **Review system (not ready yet)**
  Customers can leave reviews for completed reservations.

- **Modern admin dashboard**  
  Enhanced Django admin with Jazzmin for improved UX.

- **Responsive UI**  
  Built with Bootstrap 5 and Crispy Forms for a clean, mobile-friendly experience.

---

## Tech stack

- **Backend:** Django 5, Django REST Framework  
- **Frontend:** Django Templates, Bootstrap 5, Crispy Forms  
- **Database:** PostgreSQL (with fallback to SQLite for local development)  
- **Static & Media Handling:** Whitenoise for static files, local media storage  
- **Admin UI:** Jazzmin

---

## Local development setup

1. **Clone the repository**
   ```bash
   git clone <https://github.com/vixrad/django_advanced_regular_exam_25_viktor_radin>
   cd viko_restaurant_saas
    ```
2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Mac/Linux
   .venv\Scripts\activate     # on Windows

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
5. **Configure environment variables (.env file)**
    ```bash
    SECRET_KEY=your-secret-key
    DEBUG=True
    USE_POSTGRES=False
    COMPANIES_HOUSE_API_KEY=your-api-key
    ```
6. **Apply migrations**
   ```bash
   python manage.py migrate

7. **Run server**
   ```bash
   python manage.py runserver
