
# Code snippets for vulnerabilities in app.py

# XSS vulnerability at line 122

@app.get("/search")
async def search(query: str):
    """Vulnerable to XSS - directly returns user input"""
    # SAST VULNERABILITY: XSS - unsanitized user input
    return HTMLResponse(f"<h1>Search Results for: {query}</h1><p>No results found.</p>")


# SQL Injection vulnerability at line 157

@app.get("/users")
async def get_users(user_id: Optional[str] = None):
    """Vulnerable to SQL injection via query parameter"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if user_id:
        # SAST VULNERABILITY: SQL Injection
        query = f"SELECT * FROM users WHERE id = {user_id}"
    else:
        query = "SELECT * FROM users"
    
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()
        return {"users": users}
    except Exception as e:
        conn.close()
        return {"error": str(e)}


# Path Traversal vulnerability at line 184

@app.get("/file")
async def read_file(path: str):
    """Vulnerable to path traversal attacks"""
    try:
        # SAST VULNERABILITY: Path Traversal - no path validation
        with open(path, 'r') as f:
            content = f.read()
        return {"file_content": content}
    except Exception as e:
        return {"error": str(e)}


# File Upload vulnerability at line 218

@app.post("/upload")
async def upload_file(file_data: FileUpload):
    """Vulnerable file upload without validation"""
    try:
        # SAST VULNERABILITY: Unrestricted file upload
        file_path = f"uploads/{file_data.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(file_data.content)
        
        return {"message": f"File uploaded to {file_path}"}
    except Exception as e:
        return {"error": str(e)}

