# Testing Guide - Mock Authentication

## 🚀 **Quick Start**

Your FastAPI backend is now ready to test without Firebase! The system uses mock authentication for development.

## 🔑 **Mock Users Available**

| Token | Role | Access Level | Description |
|-------|------|-------------|-------------|
| `admin_user` | Admin | 🔴 Full Access | Can access everything |
| `stakeholder_user` | Stakeholder | 🟠 High Access | Can view/edit all data |
| `internal_user` | Internal | 🟡 Limited Access | Can view all data (read-only) |
| `normal_user` | Normal | 🟢 Basic Access | Own data only |
| `any_other_token` | Normal | 🟢 Basic Access | Defaults to normal user |

## 📡 **How to Test**

### **1. Start the Server**
```cmd
python dev.py
```

### **2. Test Without Authentication (Public Endpoints)**
```bash
# Health check
curl http://localhost:8000/health

# Auth health check
curl http://localhost:8000/auth/health

# Get available mock users
curl http://localhost:8000/auth/mock-users
```

### **3. Test With Authentication**

#### **Admin User (Full Access)**
```bash
# Get user info
curl -H "Authorization: Bearer admin_user" http://localhost:8000/auth/me

# Get all data (admin sees everything)
curl -H "Authorization: Bearer admin_user" http://localhost:8000/data/

# Access admin endpoints
curl -H "Authorization: Bearer admin_user" http://localhost:8000/admin/users
curl -H "Authorization: Bearer admin_user" http://localhost:8000/admin/stats
```

#### **Stakeholder User (High Access)**
```bash
# Get user info
curl -H "Authorization: Bearer stakeholder_user" http://localhost:8000/auth/me

# Get all data (stakeholder sees everything)
curl -H "Authorization: Bearer stakeholder_user" http://localhost:8000/data/

# Try admin endpoint (should fail)
curl -H "Authorization: Bearer stakeholder_user" http://localhost:8000/admin/users
# Returns: 403 Forbidden
```

#### **Internal User (Limited Access)**
```bash
# Get user info
curl -H "Authorization: Bearer internal_user" http://localhost:8000/auth/me

# Get all data (internal sees everything but read-only)
curl -H "Authorization: Bearer internal_user" http://localhost:8000/data/

# Try to create data (should work)
curl -X POST -H "Authorization: Bearer internal_user" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Data", "content": "Internal user data"}' \
     http://localhost:8000/data/
```

#### **Normal User (Basic Access)**
```bash
# Get user info
curl -H "Authorization: Bearer normal_user" http://localhost:8000/auth/me

# Get only own data
curl -H "Authorization: Bearer normal_user" http://localhost:8000/data/

# Create data
curl -X POST -H "Authorization: Bearer normal_user" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Data", "content": "Normal user data"}' \
     http://localhost:8000/data/

# Try admin endpoint (should fail)
curl -H "Authorization: Bearer normal_user" http://localhost:8000/admin/users
# Returns: 403 Forbidden
```

## 🧪 **Test Scenarios**

### **Role-Based Data Access**
1. **Create data as normal user**
2. **Try to access it as different roles**
3. **Verify access permissions**

### **Permission Testing**
```bash
# Test data creation
curl -X POST -H "Authorization: Bearer normal_user" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Item", "content": "Test content"}' \
     http://localhost:8000/data/

# Test data access by different roles
curl -H "Authorization: Bearer admin_user" http://localhost:8000/data/1
curl -H "Authorization: Bearer stakeholder_user" http://localhost:8000/data/1
curl -H "Authorization: Bearer internal_user" http://localhost:8000/data/1
curl -H "Authorization: Bearer normal_user" http://localhost:8000/data/1
```

## 📚 **Interactive Documentation**

Visit these URLs in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test endpoints directly in the browser by:
1. Clicking "Authorize" button
2. Entering: `Bearer admin_user` (or any other token)
3. Testing endpoints with authentication

## 🔄 **Adding Firebase Later**

When you're ready to add Firebase authentication:

1. **Install Firebase dependencies**:
   ```cmd
   pip install firebase-admin python-jose[cryptography]
   ```

2. **Replace mock authentication**:
   - Update imports from `dependencies.mock_auth` to `dependencies.auth`
   - Configure Firebase service account
   - Update token verification logic

3. **The role system remains the same** - just the authentication method changes!

## 🎯 **Benefits of This Approach**

- ✅ **No Firebase setup required** for development
- ✅ **Full role-based access control** testing
- ✅ **Easy to switch to Firebase** later
- ✅ **All endpoints work** immediately
- ✅ **Perfect for frontend development**

Your backend is now ready for development and testing! 🚀
