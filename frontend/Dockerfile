FROM node:24-alpine

# Set work directory
WORKDIR /app

# Copy and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy app source
COPY frontend/ ./

# Expose port
EXPOSE 5173

# Run app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
