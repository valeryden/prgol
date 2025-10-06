#!/usr/bin/env python3
"""
Wiz Security Testing Application
This FastAPI application contains intentional security vulnerabilities 
for testing Wiz scanning capabilities:
- Secret scanning
- CVE scanning  
- SAST (Static Application Security Testing)
- IaC scanning (via Docker/K8s configs)
"""

import os
import sqlite3
import subprocess
import hashlib
from pathlib import Path
from typing import Optional
import jwt
import requests
from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

# INTENTIONAL VULNERABILITY: Hardcoded secrets for testing secret scanning
AWS_ACCESS_KEY = "AKIAIOSsxxxxxxxPLE"  # Test AWS key pattern
AWS_SECRET_KEY = "wJalrXUtnFExxxxxxxxxxxYEXAMPLEKEY"
AZURE_CONNECTION_STRING = "DefaultExxxxxxxxxxxame=test;AccountKey=abc123=="
DATABASE_URL = "postgresql://adxxxxxxx23@localhost:5432/testdb"
JWT_SECRET = "super_xxxxxxx_12345"  # Weak JWT secret
API_TOKEN = "hf_livxxxxxxen_abcdef123456789"  # HelloFresh-like API token
MONGODB_URI = "mongodb://admin:sexxxxxxmongodb.example.com:27017/production"

# More hardcoded secrets for comprehensive testing
GITHUB_TOKEN = "ghp_12345678xxxxxxxxnopqrstuvwxyz"
SLACK_TOKEN = "xoxb-12xxxxxxxxx3456789012-abcdefghijklmnopqrstuvwx"
SENDGRID_API_KEY = "SG.12xxxxxxxxxxxopqrstuvwxyz.abcdefghijklmnopqrstuvwxyz1234567890"

app = FastAPI(title="Wiz Security Test App", version="1.0.0")
security = HTTPBearer()

# Database setup with SQLite (vulnerable to SQL injection)
DATABASE_FILE = "test.db"

def init_db():
    """Initialize vulnerable database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create users table with intentionally vulnerable structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Insert test data with weak passwords
    cursor.execute("""
        INSERT OR REPLACE INTO users (id, username, password, email, role) 
        VALUES (1, 'admin', 'admin123', 'admin@example.com', 'admin')
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO users (id, username, password, email, role) 
        VALUES (2, 'user', 'password', 'user@example.com', 'user')
    """)
    
    conn.commit()
    conn.close()

class UserLogin(BaseModel):
    username: str
    password: str

class FileUpload(BaseModel):
    filename: str
    content: str

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main page with vulnerable form"""
    return """
    <html>
        <head><title>Wiz Security Test App</title></head>
        <body>
            <h1>Security Test Application</h1>
            <p>This app contains intentional vulnerabilities for testing Wiz capabilities.</p>
            
            <!-- Vulnerable search form (XSS) -->
            <form action="/search" method="get">
                <input type="text" name="query" placeholder="Search...">
                <input type="submit" value="Search">
            </form>
            
            <!-- SQL Injection login form -->
            <h3>Login (SQL Injection Test)</h3>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <input type="submit" value="Login">
            </form>
            
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/users">View Users (SQL Injection)</a></li>
                <li><a href="/secrets">View Secrets</a></li>
                <li><a href="/file?path=../../etc/passwd">File Access (Path Traversal)</a></li>
                <li><a href="/command?cmd=ls">Command Execution</a></li>
            </ul>
        </body>
    </html>
    """


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Vulnerable SQL injection login"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # SAST VULNERABILITY: SQL Injection - direct string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Generate JWT with weak secret
            token = jwt.encode({"user_id": user[0], "username": user[1]}, JWT_SECRET, algorithm="HS256")
            return {"message": "Login successful", "token": token, "user": user}
        else:
            return {"message": "Invalid credentials"}
    except Exception as e:
        conn.close()
        return {"message": f"Database error: {str(e)}"}


@app.get("/secrets")
async def view_secrets():
    """Endpoint that exposes hardcoded secrets"""
    return {
        "aws_key": AWS_ACCESS_KEY,
        "database": DATABASE_URL,
        "jwt_secret": JWT_SECRET,
        "api_token": API_TOKEN[:10] + "...",  # Partial exposure
        "github_token": GITHUB_TOKEN,
        "mongodb_uri": MONGODB_URI
    }


@app.get("/command")
async def execute_command(cmd: str):
    """Vulnerable command injection endpoint"""
    try:
        # SAST VULNERABILITY: Command Injection - unsanitized input
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "command": cmd,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/hash")
async def weak_hash(data: str):
    """Uses weak hashing algorithm"""
    # SAST VULNERABILITY: Weak cryptography - MD5 is deprecated
    weak_hash = hashlib.md5(data.encode()).hexdigest()
    return {"md5_hash": weak_hash}

@app.get("/external")
async def make_external_request(url: str):
    """Vulnerable to SSRF attacks"""
    try:
        # SAST VULNERABILITY: SSRF - unvalidated external requests
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "status_code": response.status_code,
            "content": response.text[:500]  # Limit response size
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/debug")
async def debug_info():
    """Exposes sensitive debug information"""
    return {
        "environment_variables": dict(os.environ),
        "current_directory": os.getcwd(),
        "python_path": os.sys.path,
        "database_file": DATABASE_FILE
    }

if __name__ == "__main__":
    # SAST VULNERABILITY: Debug mode in production
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
