# 👿 1. Use outdated and vulnerable Node.js base image (includes OpenSSL, V8, and npm vulnerabilities)
FROM node:8.11.1

# 🧨 2. Run everything as root (default in many base images)
USER root

# 📂 3. Create app directory in a world-writable system path
RUN mkdir -p /tmp/app && chmod 777 /tmp/app
WORKDIR /tmp/app

# 📜 4. Copy vulnerable app with known CVEs (see earlier `package.json`)
COPY . .

# 🔥 5. Install dependencies without lock file (no reproducibility)
RUN npm install

# 🚪 6. Expose a high-risk port
EXPOSE 1337

# 🧼 7. No cleanup (leaves cache and secrets if present)
# ⚠️ 8. No HEALTHCHECK
# 🧨 9. No ENTRYPOINT hardening

# 🛠️ 10. Start the app in development mode with debug info
CMD ["node", "index.js"]
