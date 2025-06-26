### **MVP Technical Architecture: Campus Gigs**

Here is the detailed technical blueprint for the "Campus Gigs" mobile application MVP.

---

### **1. Recommended Tech Stack**

The architecture is designed as a TypeScript monorepo to maximize code sharing and streamline development between the mobile app and backend.

*   **Monorepo Management:** **pnpm Workspaces** - Efficiently manages dependencies across multiple projects.
*   **Mobile Application (Frontend):**
    *   **Framework:** **React Native** with **Expo** - Allows for rapid development and deployment to both iOS and Android from a single codebase. Expo provides a robust ecosystem of tools and pre-built modules.
    *   **Routing:** **Expo Router** - A file-based routing system that simplifies navigation and deep linking.
    *   **State Management:** React Context API (for MVP), Zustand (for scalability).
*   **Backend:**
    *   **Framework:** **NestJS** - A progressive Node.js framework using TypeScript, built on top of Express.js. It provides a structured, modular architecture perfect for scalable applications.
    *   **Database:** **PostgreSQL** - A powerful, open-source object-relational database system known for its reliability and feature robustness.
    *   **ORM (Object-Relational Mapping):** **Prisma** - A next-generation ORM for Node.js and TypeScript that simplifies database access with a type-safe client.
    *   **Authentication:** **JWT (JSON Web Tokens)** implemented using Passport.js for securing API endpoints.
*   **Development & Deployment:**
    *   **Containerization:** **Docker** - To create consistent development and production environments for the backend and database.

---

### **2. Repository Folder Structure**

The repository will be a `pnpm` monorepo. Here is the detailed hierarchical structure:

```
campus-gigs/
├── .github/                      # GitHub-specific files
│   └── workflows/
│       └── ci.yml                # Continuous Integration workflow
│   └── PULL_REQUEST_TEMPLATE.md
├── apps/                         # Contains runnable applications
│   ├── mobile/                   # React Native (Expo) mobile app
│   │   ├── app/                  # Expo Router file-based routes
│   │   │   ├── (tabs)/           # Directory for tab-based navigation
│   │   │   │   ├── _layout.tsx   # Tab navigator layout
│   │   │   │   ├── index.tsx     # Gig feed screen
│   │   │   │   ├── map.tsx       # Map view screen
│   │   │   │   └── profile.tsx   # User profile screen
│   │   │   └── _layout.tsx       # Root stack layout
│   │   ├── assets/               # Static assets (images, fonts)
│   │   ├── components/           # Reusable React components
│   │   │   └── common/           # General-purpose components (buttons, inputs)
│   │   ├── constants/            # App-wide constants (colors, styles)
│   │   ├── hooks/                # Custom React hooks
│   │   ├── services/             # API services, utility functions
│   │   │   └── api.ts            # Central API client
│   │   ├── app.json              # Expo configuration file
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── server/                   # NestJS backend application
│       ├── prisma/
│       │   └── schema.prisma     # Prisma schema for database models
│       ├── src/
│       │   ├── auth/             # Authentication module (login, signup)
│       │   ├── gigs/             # Gigs module (CRUD for gigs)
│       │   ├── users/            # Users module (user profiles)
│       │   ├── app.controller.ts # Root controller
│       │   ├── app.module.ts     # Root module
│       │   └── main.ts           # Application entry point
│       ├── test/                 # End-to-end and unit tests
│       ├── Dockerfile
│       ├── package.json
│       └── tsconfig.json
│
├── packages/                     # Shared code and utilities
│   └── types/                    # Shared TypeScript types/interfaces
│       ├── src/
│       │   ├── index.ts
│       │   ├── gig.ts
│       │   └── user.ts
│       └── package.json
│
├── .dockerignore
├── .editorconfig
├── .env.example                  # Example environment variables
├── .gitignore
├── docker-compose.yml            # For local development database and server
├── package.json                  # Root package.json for monorepo scripts
├── pnpm-workspace.yaml           # Defines the monorepo workspaces
└── README.md
```

---

### **3. README.md Content**

```markdown
# Campus Gigs

**Connecting university students with part-time gigs near campus.**

Campus Gigs is a mobile application designed to bridge the gap between students seeking flexible, local work and businesses looking for temporary, on-demand help.

## ✨ Features (MVP)

*   **Student Accounts:** Simple email/password signup and profile creation.
*   **Business Accounts:** Post and manage part-time job listings (gigs).
*   **Gig Feed:** Students can browse a real-time feed of available gigs, sorted by proximity and posting date.
*   **Map View:** Visualize available gigs on a map centered around the university campus.
*   **Simple Applications:** Students can apply to gigs with a single tap.
*   **Application Tracking:** Businesses can view and manage applications for their gigs.

## 🚀 Tech Stack

This project is a TypeScript monorepo managed with `pnpm` workspaces.

*   **Monorepo:** [pnpm Workspaces](https://pnpm.io/workspaces)
*   **Mobile App:** [React Native](https://reactnative.dev/) with [Expo](https://expo.dev/)
    *   **Routing:** Expo Router
    *   **UI:** Native components, potentially with a simple component library.
*   **Backend:** [NestJS](https://nestjs.com/) (Node.js framework)
*   **Database:** [PostgreSQL](https://www.postgresql.org/)
*   **ORM:** [Prisma](https://www.prisma.io/)
*   **Authentication:** JWT with [Passport.js](http://www.passportjs.org/)
*   **Containerization:** [Docker](https://www.docker.com/)

---

## 🛠️ Getting Started

### Prerequisites

*   [Node.js](https://nodejs.org/en/) (v18 or later)
*   [pnpm](https://pnpm.io/installation)
*   [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
*   [Expo Go](https://expo.dev/go) app on your mobile device (iOS or Android) or a simulator.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/campus-gigs.git
cd campus-gigs
```

### 2. Install Dependencies

Install all dependencies for all workspaces from the root directory.

```bash
pnpm install
```

### 3. Setup Environment Variables

The backend server and database require environment variables to run.

First, create a `.env` file in the root of the project by copying the example:

```bash
cp .env.example .env
```

Now, open `.env` and fill in the required values. The default values are configured to work with the `docker-compose.yml` setup. You should set a secure `JWT_SECRET`.

### 4. Start the Development Environment

This command will use Docker Compose to spin up the PostgreSQL database and the NestJS backend server with hot-reloading.

```bash
docker-compose up --build
```

You can verify the server is running by navigating to `http://localhost:3001` in your browser. You should see "Hello World!".

### 5. Run the Mobile App

In a separate terminal, navigate to the mobile app directory and start the Expo development server.

```bash
cd apps/mobile
pnpm start
```

This will open a Metro Bundler interface in your terminal. You can now:
*   Scan the QR code with the Expo Go app on your phone.
*   Press `i` to run on an iOS Simulator.
*   Press `a` to run on an Android Emulator.

The mobile app is configured to connect to the backend server running on `localhost:3001`.
```