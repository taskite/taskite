# Taskite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue.js-3.0+-blue.svg)](https://vuejs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/your-username/taskite/issues)

Taskite is an open-source task management tool built with Django and Vue.js, designed to help teams and individuals organize their work efficiently and effectively.

## Features

- 📋 Intuitive task management
- 🏷️ Custom labels and categories
- 👥 Team collaboration
- 📅 Due date tracking
- 📊 Progress visualization
- 🔍 Advanced search and filtering
- 📱 Responsive design

## Local Development

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (for background tasks)

### Backend Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Deployment

### Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up --build
```

### Manual Deployment

1. Set up a production-grade web server (nginx/Apache)
2. Configure PostgreSQL database
3. Set up environment variables
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
5. Build frontend:
   ```bash
   npm run build
   ```
6. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
7. Set up Gunicorn or uWSGI
8. Configure SSL certificate
9. Set up monitoring

### Cloud Platforms

Taskite can be deployed on various cloud platforms:

- **Heroku**
  - Use the provided `Procfile`
  - Configure environment variables
  - Add PostgreSQL addon

- **DigitalOcean**
  - Deploy using App Platform
  - Or set up a Droplet manually

- **AWS**
  - Use Elastic Beanstalk
  - Or deploy to EC2 instances

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

Thanks to all the amazing contributors who have helped make Taskite better! ✨

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📫 Contact us at: support@taskite.com
- 🌟 Star us on GitHub
- 📢 Follow us on Twitter [@taskite](https://twitter.com/taskite)