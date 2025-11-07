# 🚀 Quick Start Guide - Multi-Agent Design System

![Frontend demo — Home screen](https://github.com/ShoaibShoukat2/AIAgents/blob/603ea4a8394668c663e362235a620e9e7057a7d9/Screenshot%202025-11-07%20032003.png)
Complete step-by-step setup guide for the entire system.

---

## ⚡ Option 1: Quick Setup with Docker (Recommended)

### Prerequisites
- Docker Desktop installed
- Git installed

### Steps

```bash
# 1. Clone or create project directory
mkdir multi-agent-design-system
cd multi-agent-design-system

# 2. Create all required files (main.py, docker-compose.yml, etc.)
# Copy all the provided code files

# 3. Start everything with Docker
docker-compose up -d

# 4. Check if everything is running
docker-compose ps

# Access the services:
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - MongoDB Express: http://localhost:8081 (admin/admin123)
```

**That's it! Your backend is running! ✅**

---

## 🔧 Option 2: Manual Setup (Development)

### Step 1: Install Prerequisites

#### For Windows:
```powershell
# Install Python 3.11
# Download from: https://www.python.org/downloads/

# Install MongoDB
# Download from: https://www.mongodb.com/try/download/community

# Verify installations
python --version
mongod --version
```

#### For Mac:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and MongoDB
brew install python@3.11
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community
```

#### For Linux (Ubuntu/Debian):
```bash
# Install Python
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Step 2: Setup Backend

```bash
# Create project directory
mkdir multi-agent-design-system
cd multi-agent-design-system
mkdir backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
motor==3.3.2
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.3.5
pymongo==4.6.0
python-multipart==0.0.6
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
MONGODB_URL=mongodb://localhost:27017
PORT=8000
OPENAI_API_KEY=your_key_here
ENVIRONMENT=development
EOF

# Create main.py with the provided code
# (Copy the entire main.py code from the artifact)

# Run the server
uvicorn main:app --reload
```

**Backend is now running at http://localhost:8000! ✅**

### Step 3: Test the Backend

```bash
# Open new terminal and test endpoints

# Health check
curl http://localhost:8000/health

# Create a test project
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "requirements": "Modern landing page design"
  }'

# Get all projects
curl http://localhost:8000/api/projects

# View API documentation
# Open browser: http://localhost:8000/docs
```

### Step 4: Setup Frontend (Optional)

```bash
# Go back to project root
cd ..
mkdir frontend
cd frontend

# Create React app with Vite
npm create vite@latest . -- --template react

# Install dependencies
npm install
npm install lucide-react

# Copy the React component code
# (Copy the MultiAgentDesignSystem component)

# Update src/App.jsx to use the component

# Start development server
npm run dev
```

**Frontend is now running at http://localhost:5173! ✅**

---

## 🧪 Testing the System

### Test 1: Create Project via API
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Website",
    "requirements": "Modern online store with product catalog, cart, and checkout"
  }'
```

### Test 2: Monitor AI Pipeline
```bash
# Get project ID from response
PROJECT_ID="your_project_id_here"

# Check project status (every few seconds)
curl http://localhost:8000/api/projects/$PROJECT_ID

# Watch status change:
# pending → generating → reviewing → pending_approval
```

### Test 3: Human Approval
```bash
curl -X POST http://localhost:8000/api/projects/$PROJECT_ID/approve \
  -H "Content-Type: application/json" \
  -d '{
    "approved": true,
    "feedback": "Excellent design! Approved for implementation."
  }'
```

### Test 4: View Statistics
```bash
curl http://localhost:8000/api/stats
```

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Failed

**Solution:**
```bash
# Check if MongoDB is running
# Windows:
net start MongoDB

# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod

# Check MongoDB status
mongosh --eval "db.adminCommand('ping')"
```

### Issue: Port 8000 Already in Use

**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Kill the process or use different port
uvicorn main:app --reload --port 8001
```

### Issue: Import Errors

**Solution:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: Can't Access MongoDB Express

**Solution:**
```bash
# If using Docker
docker-compose restart mongo-express

# Check logs
docker-compose logs mongo-express
```

---

## 📊 Monitoring

### View Logs

```bash
# Docker logs
docker-compose logs -f backend

# Manual setup logs
# Logs will appear in the terminal where uvicorn is running
```

### Check Database

```bash
# Using MongoDB Shell
mongosh

use multi_agent_design
db.projects.find().pretty()

# Or use MongoDB Express
# http://localhost:8081
```

---

## 🔐 Production Deployment

### Environment Variables for Production

```env
# Production .env
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/db?retryWrites=true&w=majority
PORT=8000
OPENAI_API_KEY=sk-proj-xxxxx
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
```

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add MongoDB plugin
railway add

# Deploy
railway up
```

### Deploy to Render

1. Create account at render.com
2. New Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy!

### Deploy to Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Login and deploy
heroku login
heroku create your-app-name
heroku addons:create mongolab:sandbox
git push heroku main
```

---

## 🎯 Next Steps

1. **Add Authentication**: Implement JWT-based auth
2. **Add Real AI APIs**: Integrate OpenAI/Claude
3. **Add Email Notifications**: Notify on approval requests
4. **Add Webhooks**: Notify external systems
5. **Add Analytics**: Track system usage
6. **Add Caching**: Implement Redis for performance

---

## 📚 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- MongoDB Docs: https://docs.mongodb.com
- Docker Docs: https://docs.docker.com
- Uvicorn Docs: https://www.uvicorn.org

---

## 💡 Pro Tips

1. **Use Postman** for API testing (import OpenAPI spec from /docs)
2. **Enable auto-reload** during development with `--reload` flag
3. **Use MongoDB Compass** for better database visualization
4. **Set up GitHub Actions** for CI/CD
5. **Monitor with Sentry** for error tracking
6. **Use Redis** for caching frequently accessed projects

---

## 🎉 Success!

Your Multi-Agent Design System is now up and running!

Test it thoroughly and enjoy the automated design workflow! 🚀
