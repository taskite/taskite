# Calyvim

![Calyvim Logo](https://calyvim.com/static/home/images/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue.js-3.0+-blue.svg)](https://vuejs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/getcaluvim/calyvim/issues)
[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v1/monitor/1pliu.svg)](https://uptime.betterstack.com/?utm_source=status_badge)

Calyvim is an open-source task management tool built with Django and Vue.js, designed to help teams and individuals organize their work efficiently and effectively.

## Features

- 📋 Intuitive task management
- 🏷️ Custom labels and categories
- 👥 Team collaboration
- 📅 Due date tracking
- 📊 Progress visualization
- 🔍 Advanced search and filtering
- 📱 Responsive design

## Frontend Setup

1. **Install dependencies:**

    ```bash
    npm install
    ```

2. **Run the development server:**

    ```bash
    npm run serve
    ```

This will start the Vue.js development server, and you can access the frontend at `http://localhost:5173`.

## Backend Setup

### Prerequisites

Ensure you have the following installed:

- **PostgreSQL**
- **Redis**
- **Python 3.8+**

### PostgreSQL Setup

1. **Install PostgreSQL:**

    Follow the instructions for your operating system from the [official PostgreSQL documentation](https://www.postgresql.org/download/).

2. **Create a database and user:**

    ```sql
    CREATE USER calyvim WITH PASSWORD 'calyvim';
    CREATE DATABASE calyvim WITH OWNER calyvim;
    ```

### Redis Setup

1. **Install Redis:**

    Follow the instructions for your operating system from the [official Redis documentation](https://redis.io/download).

2. **Start Redis server:**

    ```bash
    redis-server
    ```

### Python Setup

1. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements-dev.txt
    ```

### Environment Setup
**Copy environment variables:**

    ```bash
    cp .env.example .env
    ```

### Django Setup

1. **Set up the database:**

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

3. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

### Celery Setup

1. **Start the Celery worker:**

    ```bash
    celery -A calyvim worker -l INFO
    ```

<!-- 2. **Start the Celery beat scheduler:**

    ```bash
    celery -A calyvim beat -l INFO
    ``` -->

This will set up the backend for your project. Add these sections below the "Frontend Setup" section in your [README.md](http://_vscodecontentref_/1) file. Let me know if you need any further modifications or if you're ready to proceed to the next section.

## Contributing

We love contributions! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing to the project.

### Development Process

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python manage.py test`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Contributors

Thanks to all the amazing contributors who have helped make Calyvim better! ✨

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📫 Contact us at: hey@calyvim.com
- 🌟 Star us on GitHub
- 📢 Follow us on Twitter [@calyvim](https://x.com/calyvim)