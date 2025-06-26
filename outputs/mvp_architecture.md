This plan details the complete technical architecture for the CampusGigs MVP.

### 1. Recommended Tech Stack

- **Frontend (Mobile App):** React Native with Expo (TypeScript)
  - **Why:** Expo allows for rapid development, easy builds, and over-the-air updates. React Native provides a cross-platform solution from a single codebase, which is ideal for an MVP targeting both iOS and Android. TypeScript adds type safety, reducing bugs.
- **Backend:** Node.js with Express.js (TypeScript)
  - **Why:** A popular, high-performance stack for building REST APIs. The non-blocking I/O is well-suited for a high-concurrency application. Using TypeScript on both front and back-end enables code sharing and consistency.
- **Database:** PostgreSQL (with PostGIS extension)
  - **Why:** A powerful, open-source relational database. The PostGIS extension is crucial for efficient geospatial queries (e.g., "find gigs within 2km of campus"), which is a core feature that differentiates this app from competitors.
- **ORM:** Prisma
  - **Why:** Provides a type-safe database client and simplifies database migrations and queries, improving developer productivity and reducing common errors.
- **Monorepo Management:** PNPM Workspaces
  - **Why:** A monorepo is ideal for this project, as the mobile app and server are tightly coupled. PNPM is efficient with disk space and provides fast installation times. It simplifies managing dependencies and running scripts across packages.
- **Authentication:** JWT (JSON Web Tokens)
  - **Why:** A stateless and standard way to handle user authentication for APIs, perfect for a mobile app client.

### 2. Hierarchical Folder Structure

A monorepo structure using PNPM workspaces is recommended to manage the mobile app and server codebases in a single repository.

```
/campus-gigs-mvp
├── .github/
│   └── workflows/
│       └── ci.yml            # CI pipeline for linting, testing, and building
├── packages/
│   ├── app/                  # React Native (Expo) mobile application
│   │   ├── app/              # Expo Router file-based routing directory
│   │   │   ├── (auth)/       # Screens for authentication flow (login, signup)
│   │   │   ├── (tabs)/       # Main app layout with bottom tabs (feed, map, profile)
│   │   │   └── _layout.tsx   # Root layout for the app
│   │   ├── assets/           # Static assets like images and fonts
│   │   ├── components/       # Reusable UI components (e.g., GigCard, Button)
│   │   ├── services/         # API service layer for communicating with the backend
│   │   ├── app.json          # Expo configuration file
│   │   └── package.json
│   │
│   └── server/               # Node.js (Express) backend
│       ├── prisma/
│       │   └── schema.prisma # Prisma schema defining database models
│       ├── src/
│       │   ├── api/          # API routes (e.g., auth.routes.ts, gigs.routes.ts)
│       │   ├── controllers/  # Request/response handlers for routes
│       │   ├── middleware/   # Custom middleware (e.g., authentication)
│       │   ├── services/     # Business logic (e.g., geo-querying for gigs)
│       │   ├── app.ts        # Express app configuration
│       │   └── server.ts     # Server entry point
│       ├── .env.example      # Example environment variables
│       └── package.json
│
├── .gitignore
├── package.json              # Root package.json for monorepo scripts
├── pnpm-workspace.yaml       # Defines the monorepo workspaces
├── README.md                 # Project README file
└── tsconfig.base.json        # Shared TypeScript configuration
```

### 3. README.md File Content

```markdown
# CampusGigs MVP

CampusGigs is a mobile app that connects university students with part-time gigs near campus. Our mission is to provide students with a simple and efficient way to find flexible work that fits their busy schedules, while helping local businesses find reliable, temporary help.

This repository contains the source code for the CampusGigs mobile application (React Native) and the backend API (Node.js/Express).

## ✨ Key MVP Features

- **Student & Employer Accounts:** Separate registration and profile management for students and businesses.
- **Gig Postings:** Employers can post gigs with details like title, description, pay, location, and time.
- **Hyper-Local Gig Feed:** Students see a feed of available gigs, prioritized by proximity to their campus.
- **Geo-Location Search:** A map view to visually search for gigs nearby.
- **Simple Applications:** Students can apply for gigs with a single tap.

## 🚀 Tech Stack

- **Monorepo:** PNPM Workspaces
- **Mobile App:** React Native (Expo) & TypeScript
- **Backend:** Node.js, Express, TypeScript
- **Database:** PostgreSQL with PostGIS
- **ORM:** Prisma
- **Authentication:** JWT

## 📂 Repository Structure

This project is a monorepo managed by `pnpm`. The code is organized into two main packages:

- `packages/app`: The React Native (Expo) mobile application.
- `packages/server`: The Node.js backend server.

Shared configurations like `tsconfig.base.json` are located in the root directory.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v18 or later)
- [PNPM](https://pnpm.io/installation)
- [Docker](https://www.docker.com/get-started/) (for running PostgreSQL)

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/campus-gigs-mvp.git
    cd campus-gigs-mvp
    ```

2.  **Install dependencies from the root directory:**
    ```bash
    pnpm install
    ```

3.  **Set up the database:**
    -   Start a PostgreSQL instance using Docker. This command also sets up the PostGIS extension.
        ```bash
        docker run --name campus-gigs-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgis/postgis
        ```

4.  **Configure environment variables for the server:**
    -   Navigate to the server package: `cd packages/server`
    -   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    -   Update the `.env` file with your database connection string and a secure JWT secret:
        ```
        DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/postgres?schema=public"
        JWT_SECRET="YOUR_SUPER_SECRET_KEY"
        ```

5.  **Run database migrations:**
    -   From the `packages/server` directory, apply the Prisma schema to your database:
        ```bash
        pnpm prisma migrate dev --name init
        ```

## ▶️ Running the App

You will need two separate terminal windows to run the backend and frontend concurrently.

1.  **Start the Backend Server:**
    -   From the root directory, run:
        ```bash
        pnpm --filter server dev
        ```
    -   The server will be running on `http://localhost:4000`.

2.  **Start the Mobile App:**
    -   In a new terminal, from the root directory, run:
        ```bash
        pnpm --filter app start
        ```
    -   This will start the Expo development server. You can then run the app on an iOS simulator, Android emulator, or on your physical device using the Expo Go app.

```