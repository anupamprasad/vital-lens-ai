# Vital Lens AI Frontend - React + Vite

FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (needed for both dev and production builds)
RUN npm install

# Copy source code
COPY . .

# Build for production if needed
RUN npm run build || true

# Expose port for Vite dev server
EXPOSE 5173

# Default to dev server, can be overridden
CMD ["npm", "run", "dev"]
