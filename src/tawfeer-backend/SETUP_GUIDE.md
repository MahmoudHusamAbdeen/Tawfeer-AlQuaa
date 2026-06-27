# Tawfeer Backend - Complete Setup Guide for Visual Studio Code

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Install MongoDB](#2-install-mongodb)
3. [Open Project in VS Code](#3-open-project-in-vs-code)
4. [Configure Environment](#4-configure-environment)
5. [Install Python Dependencies](#5-install-python-dependencies)
6. [Run the Backend Server](#6-run-the-backend-server)
7. [Seed the Database](#7-seed-the-database)
8. [Connect Frontend to Backend](#8-connect-frontend-to-backend)
9. [API Documentation](#9-api-documentation)
10. [VS Code Extensions](#10-vs-code-extensions)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Prerequisites

Before starting, make sure you have:
- **Python 3.9+** installed → [Download Python](https://www.python.org/downloads/)
- **MongoDB 6.0+** installed → [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Visual Studio Code** installed → [Download VS Code](https://code.visualstudio.com/)
- **Your Tawfeer frontend** (React Native / Expo project)
- **OpenAI API Key** (optional but recommended for AI features) → [Get API Key](https://platform.openai.com/api-keys)

---

## 2. Install MongoDB

### Windows:
1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Run the installer with default settings
3. MongoDB will install as a Windows Service and start automatically
4. Verify: Open Command Prompt and run:
   ```
   mongosh
   ```
   You should see the MongoDB shell prompt.

### macOS:
```bash
# Install using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux (Ubuntu):
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Using MongoDB Atlas (Cloud - Free Tier):
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account and cluster
3. Get your connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/`)
4. Use this as your `MONGODB_URI` in the `.env` file

---

## 3. Open Project in VS Code

1. **Extract the backend folder** to a location on your computer (e.g., `C:\Projects\tawfeer-backend`)

2. **Open VS Code**

3. **Open the project folder**:
   - Click **File → Open Folder**
   - Navigate to the `tawfeer-backend` folder
   - Click **Select Folder**

4. **Your VS Code should show this file structure**:
   ```
   tawfeer-backend/
   ├── app/
   │   ├── __init__.py
   │   ├── config.py              # App configuration
   │   ├── database.py            # MongoDB connection
   │   ├── models/
   │   │   ├── __init__.py
   │   │   ├── user.py            # User authentication models
   │   │   ├── donation.py        # Donation & order models
   │   │   └── ai.py              # AI recipe models
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── auth_routes.py     # Login/Register APIs
   │   │   ├── ai_routes.py       # OpenAI recipe APIs
   │   │   ├── donation_routes.py # Donation & request APIs
   │   │   ├── admin_routes.py    # Admin dashboard APIs
   │   │   ├── driver_routes.py   # Driver dashboard APIs
   │   │   └── government_routes.py # Government dashboard APIs
   │   └── services/
   │       ├── __init__.py
   │       ├── auth.py            # JWT & password hashing
   │       └── openai_service.py  # OpenAI API integration
   ├── frontend-api/
   │   ├── api.js                 # Frontend API service file
   │   ├── AISuggestionBox_UPDATED.js  # Updated AI screen example
   │   └── LoginScreen_UPDATED.js      # Updated Login screen example
   ├── scripts/
   │   └── seed_database.py       # Database seeding script
   ├── main.py                    # App entry point
   ├── requirements.txt           # Python dependencies
   ├── .env.example               # Environment template
   ├── start.py                   # Quick start script
   └── SETUP_GUIDE.md             # This file
   ```

---

## 4. Configure Environment

1. **Create the `.env` file** from the example:
   - In VS Code, open the `tawfeer-backend` folder
   - You'll see `.env.example`
   - Right-click it → **Copy**
   - Right-click in the same folder → **Paste**
   - Rename the copy to `.env`

2. **Edit the `.env` file** with your settings:
   ```
   # MongoDB - Use localhost or your Atlas connection string
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=tawfeer

   # JWT Secret - Generate a new one!
   # Run: python -c "import secrets; print(secrets.token_urlsafe(32))"
   JWT_SECRET=your-generated-secret-key-here

   # OpenAI API Key - Get from https://platform.openai.com/api-keys
   OPENAI_API_KEY=sk-your-openai-api-key-here

   # Server
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True

   # CORS - Add your frontend URLs
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19000,http://localhost:19006,exp://127.0.0.1:19000
   ```

3. **Generate a JWT Secret**:
   - Open VS Code Terminal (Ctrl+`)
   - Run:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - Copy the output and paste it as your `JWT_SECRET`

---

## 5. Install Python Dependencies

1. **Open VS Code Terminal**:
   - Press `` Ctrl+` `` or go to **Terminal → New Terminal**

2. **Create a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `fastapi` - Web framework
   - `uvicorn` - ASGI server
   - `motor` - Async MongoDB driver
   - `python-jose` - JWT tokens
   - `passlib` - Password hashing
   - `openai` - OpenAI API client
   - `pydantic` - Data validation
   - and more...

---

## 6. Run the Backend Server

### Option A: Using the start script
```bash
python start.py
```

### Option B: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option C: Using VS Code Run Button
1. Open `main.py` in VS Code
2. Click the **Run** button (▶) in the top-right corner
3. Or press **F5** to debug

### Verify the server is running:
- Open your browser and go to: **http://localhost:8000**
- You should see: `{"app":"Tawfeer API","version":"1.0.0","status":"running"}`
- API docs are available at: **http://localhost:8000/docs**

---

## 7. Seed the Database (Optional - Add Test Data)

Run the seeding script to add sample users and drivers:

```bash
python scripts/seed_database.py
```

This creates these test accounts:

| Role     | Login             | Password |
|----------|-------------------|----------|
| User     | ahmed@example.com | 123      |
| User     | fatima@example.com| 123      |
| User     | saeed@company.com | 123      |
| Admin    | admin123          | 123      |
| Gov      | gov123            | 123      |
| Driver   | driver1           | 123      |
| Driver   | driver2           | 123      |

---

## 8. Connect Frontend to Backend

### Step 1: Copy the API service file
1. Copy `frontend-api/api.js` to your frontend project
2. Place it at: `tawfeer-5-10-2026/services/api.js`

### Step 2: Install axios in your frontend
```bash
cd tawfeer-5-10-2026
npm install axios
```

### Step 3: Update the BASE_URL in api.js
```javascript
// For Android Emulator:
const BASE_URL = 'http://10.0.2.2:8000';

// For iOS Simulator:
const BASE_URL = 'http://localhost:8000';

// For Physical Device (use your computer's IP):
const BASE_URL = 'http://192.168.1.100:8000';
```

To find your computer's IP:
- Windows: `ipconfig` → look for IPv4 Address
- Mac/Linux: `ifconfig` → look for inet address

### Step 4: Replace AsyncStorage calls in each screen

Here's what to change in each screen file:

#### LoginScreen.js
```javascript
// OLD (using AsyncStorage):
const getUserAccount = async (email, password) => {
  const usersJson = await AsyncStorage.getItem('users');
  const users = JSON.parse(usersJson);
  return users.find(u => (u.email === email || u.phone === email) && u.password === password);
};

// NEW (using API):
import { loginUser } from '../services/api';
const handleLogin = async () => {
  const response = await loginUser(emailOrPhone, password);
  // response contains: access_token, user, role
};
```

#### RegisterScreen.js
```javascript
// OLD:
const saveCredentials = async (userData) => {
  const existingUsers = await AsyncStorage.getItem('users');
  const users = existingUsers ? JSON.parse(existingUsers) : [];
  users.push(userData);
  await AsyncStorage.setItem('users', JSON.stringify(users));
};

// NEW:
import { registerUser } from '../services/api';
const handleRegister = async () => {
  const response = await registerUser(userData);
  // response contains: access_token, user
};
```

#### AISuggestionBox.js
```javascript
// OLD (fake data with setTimeout):
const handleGetSuggestions = () => {
  setLoading(true);
  setTimeout(() => {
    const ideas = [/* hardcoded fake data */];
    setSuggestions(ideas);
    setLoading(false);
  }, 1500);
};

// NEW (real OpenAI via backend):
import { getRecipeSuggestions } from '../services/api';
const handleGetSuggestions = async () => {
  setLoading(true);
  try {
    const response = await getRecipeSuggestions(ingredients, language);
    const ideas = response.suggestions.map((s, i) => ({
      id: i + 1,
      title: s.title,
      emoji: s.emoji,
      prepTime: s.prep_time,
      difficulty: s.difficulty,
      steps: s.steps.map(step => step.instruction),
      result: s.result,
    }));
    setSuggestions(ideas);
  } catch (error) {
    Alert.alert('Error', error.message);
  } finally {
    setLoading(false);
  }
};
```

#### FoodInteractionScreen.js
```javascript
// Replace donation submission:
import { submitDonation, submitFoodRequest, markOrderDone, getCurrentUserData } from '../services/api';

// Replace loadUserData:
const loadUserData = async () => {
  try {
    const data = await getCurrentUserData();
    setPoints(data.user.points);
    setDonationHistory(data.donation_history);
    setActiveOrders(data.active_orders);
    setMessages(data.messages);
  } catch (error) {
    console.error('Error loading user data:', error);
  }
};
```

#### AdminScreen.js
```javascript
import { getAdminStats, getAllUsers, getAllOrders, approveOrder, rejectOrder, getAllDrivers, createDriver, deleteDriver } from '../services/api';

const loadAdminData = async () => {
  const stats = await getAdminStats();
  const usersData = await getAllUsers();
  const ordersData = await getAllOrders();
  const driversData = await getAllDrivers();
  // Use this data instead of AsyncStorage
};
```

#### DriverLoginScreen.js
```javascript
import { loginDriver } from '../services/api';

const handleLogin = async () => {
  const response = await loginDriver(username, password);
  navigation.replace('DriverDashboard', {
    driverData: {
      id: response.user.id,
      name: response.user.name,
      username: response.user.email,
      phone: response.user.phone,
    }
  });
};
```

#### DriverDashboard.js
```javascript
import { getDriverOrders, updateOrderStatus } from '../services/api';

const loadOrders = async () => {
  const data = await getDriverOrders();
  setOrders(data.orders);
};
```

#### GovernmentDashboard.js
```javascript
import { getGovernmentStats, getGovernmentChartData, getRecentActivities } from '../services/api';

const loadGovernmentData = async () => {
  const stats = await getGovernmentStats();
  const chartData = await getGovernmentChartData(viewMode);
  const activities = await getRecentActivities();
  // Use this data instead of AsyncStorage
};
```

---

## 9. API Documentation

Once the server is running, visit these URLs:

- **Swagger UI** (interactive): http://localhost:8000/docs
- **ReDoc** (alternative docs): http://localhost:8000/redoc

### API Endpoints Summary:

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| **AUTH** ||||
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login (user/admin/gov) | No |
| POST | `/api/auth/driver-login` | Login as driver | No |
| GET | `/api/auth/me` | Get current user data | Yes |
| PUT | `/api/auth/profile` | Update profile | Yes |
| PUT | `/api/auth/change-password` | Change password | Yes |
| **AI** ||||
| POST | `/api/ai/recipes` | Get AI recipe suggestions | No |
| POST | `/api/ai/ask` | Ask AI food question | No |
| **DONATIONS** ||||
| POST | `/api/donations/donate` | Submit food donation | Yes |
| POST | `/api/donations/request` | Submit food request | Yes |
| POST | `/api/donations/mark-done` | Mark order as done | Yes |
| GET | `/api/donations/history/{email}` | Get donation history | Yes |
| POST | `/api/donations/redeem-reward` | Redeem reward points | Yes |
| **ADMIN** ||||
| GET | `/api/admin/stats` | Dashboard statistics | Admin |
| GET | `/api/admin/users` | List all users | Admin |
| GET | `/api/admin/orders` | List all orders | Admin |
| POST | `/api/admin/approve-order` | Approve order | Admin |
| POST | `/api/admin/reject-order` | Reject order | Admin |
| POST | `/api/admin/complete-order` | Complete order | Admin |
| DELETE | `/api/admin/user` | Delete user | Admin |
| GET | `/api/admin/drivers` | List all drivers | Admin |
| POST | `/api/admin/drivers` | Create driver | Admin |
| DELETE | `/api/admin/drivers` | Delete driver | Admin |
| **DRIVER** ||||
| GET | `/api/driver/orders` | Get assigned orders | Driver |
| POST | `/api/driver/update-status` | Update order status | Driver |
| GET | `/api/driver/stats` | Driver statistics | Driver |
| **GOVERNMENT** ||||
| GET | `/api/government/stats` | Government statistics | Gov |
| GET | `/api/government/charts` | Chart data | Gov |
| GET | `/api/government/activities` | Recent activities | Gov |
| GET | `/api/government/top-users` | Top users by points | Gov |

---

## 10. VS Code Extensions (Recommended)

Install these extensions for the best development experience:

1. **Python** (ms-python.python) - Python language support
2. **Pylance** (ms-python.vscode-pylance) - Type checking and autocomplete
3. **REST Client** (humao.rest-client) - Test APIs directly in VS Code
4. **Thunder Client** (rangav.vscode-thunder-client) - API testing GUI
5. **MongoDB for VS Code** (mongodb.mongodb-vscode) - MongoDB explorer
6. **DotENV** (mikestead.dotenv) - .env file syntax highlighting
7. **Auto Rename Tag** (formulahendry.auto-rename-tag) - For frontend editing
8. **ES7+ React/Redux Snippets** (dsznajder.es7-react-js-snippets) - React snippets

### To install extensions:
1. Click the **Extensions** icon in the left sidebar (or press Ctrl+Shift+X)
2. Search for each extension name
3. Click **Install**

---

## 11. Troubleshooting

### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution**: Make sure MongoDB is running:
- Windows: Open Services and start "MongoDB"
- Mac: `brew services start mongodb-community`
- Linux: `sudo systemctl start mongod`

### OpenAI API Error
```
openai.error.AuthenticationError
```
**Solution**: Check your OpenAI API key in the `.env` file. If you don't have one, the app will use fallback recipe suggestions.

### Port Already in Use
```
[Errno 98] Address already in use
```
**Solution**: Kill the existing process or use a different port:
```bash
# Find what's using port 8000
# Windows:
netstat -ano | findstr :8000
# Mac/Linux:
lsof -i :8000

# Or use a different port:
uvicorn main:app --port 8001
```

### CORS Error in Frontend
```
Access-Control-Allow-Origin
```
**Solution**: Add your frontend URL to `ALLOWED_ORIGINS` in the `.env` file:
```
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19000,http://10.0.2.2:8000
```

### Cannot Connect from Android Emulator
**Solution**: Use `10.0.2.2` instead of `localhost`:
```javascript
const BASE_URL = 'http://10.0.2.2:8000';
```

### Cannot Connect from Physical Device
**Solution**:
1. Make sure your phone and computer are on the same WiFi network
2. Find your computer's local IP address
3. Use it as the BASE_URL:
```javascript
const BASE_URL = 'http://192.168.1.XXX:8000';
```

### Python Virtual Environment Issues
**Solution**: If venv activation doesn't work:
```bash
# Windows PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Mac/Linux:
source venv/bin/activate
```

---

## Quick Start Summary

```bash
# 1. Open the project in VS Code
# 2. Open Terminal (Ctrl+`)

# 3. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and OpenAI API key

# 6. Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 7. In a new terminal, seed the database
python scripts/seed_database.py

# 8. Open API docs
# http://localhost:8000/docs

# 9. Copy frontend-api/api.js to your frontend project
# 10. Update your frontend screens to use the API
```

---

**Happy Coding! 🚀**
