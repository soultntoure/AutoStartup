### **Technical Architecture & Project Plan: Mindbloom AI**

Here is the detailed technical plan for the "Mindbloom AI" gamified journaling app MVP.

### 1. Recommended Tech Stack

The architecture is designed around a modern, scalable, and type-safe monorepo structure, enabling efficient development for both the mobile app and the backend.

*   **Monorepo Management:**
    *   **npm Workspaces:** To manage dependencies and run scripts across the frontend and backend from a single root.

*   **Mobile App (Client - `packages/app`):**
    *   **Framework:** React Native will be used to build a cross-platform application for iOS and Android from a single codebase.
    *   **Language:** TypeScript for static typing, improving code quality and maintainability.
    *   **State Management:** Zustand for simple, fast, and scalable global state management.
    *   **Routing:** React Navigation for handling navigation and screen transitions.
    *   **API Communication:** Axios for making HTTP requests to the backend server.

*   **Backend (Server - `packages/server`):**
    *   **Framework:** NestJS, a progressive Node.js framework built with TypeScript. It provides an out-of-the-box application architecture which allows for the creation of highly testable, scalable, loosely coupled, and easily maintainable applications.
    *   **Language:** TypeScript.
    *   **Database:** MongoDB, a NoSQL document database, is chosen for its flexibility in storing unstructured journal entries and its scalability.
    *   **ODM (Object Data Modeling):** Mongoose to model application data for MongoDB.
    *   **Authentication:** Passport.js with a JWT (JSON Web Token) strategy for securing endpoints.

*   **AI Integration:**
    *   **OpenAI API:** The GPT-3.5 or GPT-4 model will be used to generate insightful and personalized reflection prompts based on the user's journal entries.

*   **DevOps & Tooling:**
    *   **Containerization:** Docker will be used to containerize the MongoDB instance for consistent development and production environments.
    *   **Code Formatting & Linting:** Prettier and ESLint will be enforced to maintain a consistent code style across the entire project.

### 2. Detailed Folder Structure

The project will be organized as a monorepo to streamline development and dependency management.

```
mindbloom-ai-journal/
├── .gitignore               # Specifies intentionally untracked files to ignore
├── package.json             # Root package.json defining workspaces and root scripts
├── README.md                # The main documentation file for the project
└── packages/                # Contains all the individual applications/services
    ├── app/                 # The React Native mobile application
    │   ├── android/             # Android-specific build files
    │   ├── ios/                 # iOS-specific build files
    │   ├── src/                 # Main source code for the app
    │   │   ├── api/             # Functions for interacting with the backend API (e.g., journalService.ts)
    │   │   ├── components/      # Reusable UI components (e.g., Button.tsx, MoodSelector.tsx)
    │   │   ├── config/          # App configuration (e.g., API_URL)
    │   │   ├── navigation/      # React Navigation stacks and navigators
    │   │   ├── screens/         # App screens (e.g., HomeScreen.tsx, JournalEntryScreen.tsx)
    │   │   ├── state/           # Zustand state management stores (e.g., userStore.ts)
    │   │   └── App.tsx          # The root component of the React Native app
    │   └── package.json         # Dependencies and scripts for the mobile app
    │
    └── server/              # The NestJS backend server
        ├── src/                 # Main source code for the server
        │   ├── ai/              # AI-related services (e.g., ai.service.ts for OpenAI calls)
        │   ├── auth/            # Authentication logic (e.g., auth.module.ts, jwt.strategy.ts)
        │   ├── common/          # Common modules, decorators, guards
        │   ├── journal/         # Journal entry module (controller, service, schema)
        │   ├── users/           # User management module (controller, service, schema)
        │   ├── app.controller.ts  # Root app controller
        │   ├── app.module.ts    # Root app module
        │   └── main.ts          # The application entry file
        ├── .env.example         # Example environment variables file
        └── package.json         # Dependencies and scripts for the server
```

### 3. README.md Content

```markdown
# Mindbloom AI - Gamified AI Journal

Mindbloom is a mobile journaling application designed to make self-reflection a fun and insightful daily habit. It combines gamification elements with powerful AI-driven prompts and mood tracking to help users understand their emotional patterns and foster personal growth.

This repository contains the full source code for the Mindbloom AI mobile app and its supporting backend services.

## ✨ Features (MVP)

*   **Daily Journaling:** A simple and intuitive interface for writing daily entries.
*   **AI Reflection Prompts:** After completing an entry, users receive personalized, thought-provoking questions generated by AI to encourage deeper reflection.
*   **Mood Tracking:** Easily log your mood each day to visualize trends over time.
*   **Gamification:** Earn points and unlock achievements for maintaining a consistent journaling streak.
*   **Secure & Private:** All journal entries are securely stored and encrypted.

## 🚀 Tech Stack

This project is a monorepo managed with npm workspaces.

*   **Mobile App (Client):**
    *   [React Native](https://reactnative.dev/)
    *   [TypeScript](https://www.typescriptlang.org/)
    *   [React Navigation](https://reactnavigation.org/) for routing
    *   [Zustand](https://github.com/pmndrs/zustand) for state management
    *   [Axios](https://axios-http.com/) for API communication

*   **Backend (Server):**
    *   [Node.js](https://nodejs.org/)
    *   [NestJS](https://nestjs.com/) (TypeScript framework)
    *   [MongoDB](https://www.mongodb.com/) for the database
    *   [Mongoose](https://mongoosejs.com/) as the ODM
    *   [Passport.js](http://www.passportjs.org/) with JWT for authentication

*   **AI Integration:**
    *   [OpenAI API](https://openai.com/api/) (GPT-3.5/4) for generating reflection prompts.

*   **DevOps & Tooling:**
    *   [Docker](https://www.docker.com/) for containerization
    *   [npm Workspaces](https://docs.npmjs.com/cli/v7/using-npm/workspaces) for monorepo management
    *   [Prettier](https://prettier.io/) for code formatting
    *   [ESLint](https://eslint.org/) for code linting

## 📂 Project Structure

The repository is structured as a monorepo:

` ` `
/
├── packages/
│   ├── app/      # The React Native mobile application
│   └── server/   # The NestJS backend server
├── .gitignore
├── package.json  # Root package.json for workspaces
└── README.md
` ` `

## 🛠️ Getting Started

### Prerequisites

*   [Node.js](https://nodejs.org/en/) (v18 or later)
*   [npm](https://www.npmjs.com/) (v8 or later)
*   [Docker](https://www.docker.com/) & Docker Compose (for running the database)
*   React Native development environment (see [React Native docs](https://reactnative.dev/docs/environment-setup))
*   A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account or a local MongoDB instance.
*   An [OpenAI API Key](https://platform.openai.com/).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mindbloom-ai-journal.git
    cd mindbloom-ai-journal
    ```

2.  **Install dependencies:**
    This command will install dependencies for the root, the `app`, and the `server` packages.
    ```bash
    npm install
    ```

3.  **Set up environment variables for the server:**
    Navigate to the server directory and create a `.env` file from the example.
    ```bash
    cd packages/server
    cp .env.example .env
    ```
    Now, edit the `.env` file with your database connection string and API keys:
    ```env
    # packages/server/.env
    DATABASE_URL="your_mongodb_connection_string"
    JWT_SECRET="your_strong_jwt_secret"
    OPENAI_API_KEY="your_openai_api_key"
    ```

4.  **Set up environment variables for the app:**
    Create a config file in the app source code to store the backend URL.
    `packages/app/src/config/index.ts`
    ```typescript
    export const API_URL = 'http://localhost:3000/api'; // Adjust if your server runs elsewhere
    ```

### Running the Application

1.  **Start the Backend Server:**
    From the root directory, run:
    ```bash
    npm run start:server
    ```
    The server will be running on `http://localhost:3000`.

2.  **Start the Mobile App:**
    In a new terminal window, from the root directory, run:
    ```bash
    # For iOS
    npm run start:ios

    # For Android
    npm run start:android
    ```
This will start the Metro bundler and launch the app in your selected simulator/emulator.

```