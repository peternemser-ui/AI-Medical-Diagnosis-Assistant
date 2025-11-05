# Camera Health App

# AI Medical Diagnosis Assistant

A comprehensive web-based health assessment platform that provides intelligent symptom analysis and preliminary medical guidance through AI-powered diagnostics.

## 🏥 Overview

The AI Medical Diagnosis Assistant bridges the gap between users seeking medical advice and professional healthcare through accessible, AI-powered preliminary assessments. The platform offers a doctor-patient consultation model with voice and text input capabilities.

## ✨ Features

- **Multi-Modal Input**: Voice recognition and text input for accessibility
- **Conversational Assessment**: Progressive medical questionnaire with natural language processing
- **AI Diagnosis Engine**: Primary and alternative diagnoses with confidence scoring
- **Interactive Dashboard**: Circular progress charts and comprehensive treatment recommendations
- **Professional UI**: Medical-grade design with responsive layout
- **Accessibility First**: WCAG compliant interface with voice navigation

## 🛠 Technology Stack

### Frontend
- **Vue.js 3** - Composition API for reactive interfaces
- **Vite** - Fast development and optimized builds
- **Tailwind CSS** - Medical-grade responsive design
- **Web Speech API** - Voice recognition and synthesis

### Backend
- **FastAPI** - Python-based API with automatic documentation
- **Pydantic** - Data validation for medical information
- **Uvicorn** - ASGI server for production deployment

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Modern web browser with Speech API support

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/peternemser/health-app.git
   cd health-app
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📱 Application Structure

### Core Components
- **HomeView** - Landing page and navigation
- **VoiceDiagnosis** - Main assessment interface
- **DiagnosisDashboard** - Results visualization
- **CircularProgress** - Confidence indicators
- **InputControls** - Voice/text input interface

### User Flow
1. **Landing** → Professional welcome interface
2. **Assessment** → Progressive symptom questionnaire
3. **Analysis** → AI processing and diagnosis generation
4. **Dashboard** → Comprehensive results with treatment recommendations

## 🔧 Configuration

### Environment Variables

**Frontend (.env)**
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_SPEECH_API_KEY=your_speech_api_key
```

**Backend (.env)**
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_url
```

## 🏗 Production Deployment

### Frontend Build
```bash
cd frontend
npm run build
npm run preview  # Test production build
```

### Backend Production
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build -d
```

## 📊 API Endpoints

### Main Endpoints
- `POST /api/diagnose` - Submit symptoms for analysis
- `POST /api/followup` - Continue conversation
- `GET /api/health` - System health check

### Authentication
- JWT-based authentication for user sessions
- API rate limiting for production use

## 🧪 Testing

### Run Frontend Tests
```bash
cd frontend
npm run test
```

### Run Backend Tests
```bash
cd backend
pytest tests/
```

## 📋 Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database connections secured
- [ ] API rate limiting enabled
- [ ] Error logging configured
- [ ] Health monitoring setup
- [ ] Backup procedures implemented

## 🔒 Security Features

- Input sanitization and validation
- Medical data encryption
- Secure API endpoints
- CORS configuration
- Rate limiting protection

## 📄 Medical Disclaimer

This AI-powered assessment tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For technical support or medical partnership inquiries:
- Email: support@healthassistant.ai
- Documentation: [docs.healthassistant.ai](https://docs.healthassistant.ai)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for accessible healthcare technology**

Test 2