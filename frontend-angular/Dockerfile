# --- STAGE 1: Build the Angular Application ---
FROM node:26-alpine AS builder

WORKDIR /app

# Copy dependency manifests first to optimize Docker layer caching
COPY package*.json ./

# Install project dependencies
RUN npm ci

# Copy the rest of the source code
COPY . .

# Compile the application for production
RUN npm run build -- --configuration=production --base-href=/frontend-angular/


# --- STAGE 2: Serve the Static Files Using npm http-server ---
FROM node:26-alpine

WORKDIR /app

# Install the lightweight static file server globally via npm
RUN npm install -g http-server

# Copy the compiled production assets from the builder stage
# Note: Replace 'your-app-name' with the actual output folder name found inside your dist directory
COPY --from=builder /app/dist/angular/browser ./

# Expose the default port for the server
EXPOSE 4200

# Run http-server and handle Angular client-side routing with the -P flag
CMD ["http-server", "-p", "4200", "-P", "http://localhost:4200?", "--cors"]
