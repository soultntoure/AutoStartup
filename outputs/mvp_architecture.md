## Zenith Journal: MVP Technical Architecture

This document outlines the complete technical architecture for the Zenith Journal MVP, a gamified daily journaling app with AI reflection prompts and mood tracking.

### 1. Recommended Tech Stack

The technology stack is chosen for rapid development, scalability, and a unified developer experience using the JavaScript/TypeScript ecosystem.

*   **Monorepo:** `pnpm workspaces` - To manage the backend and mobile app in a single repository.
*   **Mobile App (Frontend):** `React Native` with `Expo` - For cross-platform (iOS & Android) development with a fast development cycle.
*   **Backend:** `Node.js` with `Express.js` & `TypeScript` - For a robust, fast, and type-safe API.
*   **Database:** `MongoDB` with `Mongoose` - A flexible NoSQL database ideal for storing journal entries and user data. Deployed via `MongoDB Atlas`.
*   **AI Integration:** `OpenAI API` (GPT-4o) - To generate intelligent and empathetic reflection prompts.
*   **Authentication:** `JSON Web Tokens (JWT)` - For securing the API and managing user sessions.
*   **Deployment:**
    *   API: `Vercel` or `Render` (Serverless)
    *   Database: `MongoDB Atlas` (Cloud)
    *   Mobile App: `Expo Application Services (EAS)` for App Store / Play Store builds.

### 2. Repository Folder Structure

A monorepo structure managed by pnpm is used to house the mobile app and the backend API.

```
zenith-journal/
├── apps/
│   ├── api/                    # Node.js/Express Backend API
│   │   ├── src/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       ├── routes/         # API routes (auth, journal, etc.)
│   │   │   │       │   ├── auth.routes.ts
│   │   │   │       │   ├── journal.routes.ts
│   │   │   │       │   └── user.routes.ts
│   │   │   │       ├── controllers/    # Route handlers and business logic
│   │   │   │       │   ├── auth.controller.ts
│   │   │   │       │   ├── journal.controller.ts
│   │   │   │       │   └── user.controller.ts
│   │   │   │       ├── models/         # Mongoose DB schemas
│   │   │   │       │   ├── JournalEntry.ts
│   │   │   │       │   └── User.ts
│   │   │   │       ├── middlewares/    # Express middlewares (e.g., auth check)
│   │   │   │       │   └── auth.middleware.ts
│   │   │   │       └── services/       # Services for 3rd party integrations
│   │   │   │           └── ai.service.ts
│   │   │   ├── config/             # Configuration files (e.g., DB connection)
│   │   │   │   └── db.ts
│   │   │   ├── app.ts              # Express app setup and middleware registration
│   │   │   └── server.ts           # Server entry point
│   │   ├── .env.example
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── mobile/                 # React Native (Expo) Mobile App
│       ├── app/                  # File-based routing with Expo Router
│       │   ├── (tabs)/           # Main app layout with tabs
│       │   │   ├── _layout.tsx
│       │   │   ├── journal.tsx     # Main journaling screen
│       │   │   ├── progress.tsx    # Gamified progress and mood charts
│       │   │   └── settings.tsx
│       │   ├── auth/             # Authentication screens
│       │   │   ├── login.tsx
│       │   │   └── signup.tsx
│       │   ├── _layout.tsx       # Root layout component
│       │   └── index.tsx         # App entry/loading/redirect logic
│       ├── assets/               # Static assets (images, fonts)
│       ├── components/           # Reusable React Native components
│       ├── constants/            # App-wide constants (colors, styles)
│       ├── hooks/                # Custom React hooks (e.g., useAuth)
│       ├── services/             # API interaction layer
│       ├── app.json              # Expo configuration file
│       ├── package.json
│       └── tsconfig.json
├── packages/
│   └── types/                  # Shared TypeScript types
│       ├── src/
│       │   ├── index.ts
│       │   └── journal.ts
│       └── package.json
├── .gitignore
├── package.json                # Root package.json
├── pnpm-workspace.yaml         # pnpm workspace configuration
├── README.md
└── tsconfig.json               # Root TypeScript configuration
```

### 3. README.md File Content

---

# Zenith Journal

Zenith is a gamified daily journaling app designed to make self-reflection a rewarding and consistent habit. It combines AI-powered prompts, detailed mood tracking, and engaging game mechanics to help you understand your mind and build a positive routine.

## ✨ Features

*   **AI-Powered Prompts:** Get intelligent, empathetic prompts to guide your reflections.
*   **Mood Tracking:** Log your mood and activities to discover patterns and insights.
*   **Gamified Experience:** Earn points, unlock achievements, and watch your personal 'Zenith' grow as you build your journaling streak.
*   **Data-Driven Insights:** Visualize your progress and mood trends over time with beautiful charts.

## 🛠️ Tech Stack

This project is a monorepo managed with `pnpm workspaces`.

| Area         | Technology                                      |
| :----------- | :---------------------------------------------- |
| **Mobile App** | [React Native](https://reactnative.dev/) + [Expo](https://expo.dev/)                 |
| **Backend**    | [Node.js](https://nodejs.org/) + [Express.js](https://expressjs.com/) + [TypeScript](https://www.typescriptlang.org/) |
| **Database**   | [MongoDB](https://www.mongodb.com/) + [Mongoose](https://mongoosejs.com/)                  |
| **AI**         | [OpenAI API](https://beta.openai.com/docs/)     |

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or later)
- [pnpm](https://pnpm.io/installation)
- [Expo Go](https://expo.dev/go) app on your mobile device or an emulator setup.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/zenith-journal.git
    cd zenith-journal
    ```

2.  **Install dependencies:**
    *pnpm will automatically install dependencies for all workspaces (api, mobile, etc.).*
    ```bash
    pnpm install
    ```

3.  **Set up environment variables:**

    *   **For the API:**
        Create a `.env` file in `apps/api/` by copying the example file:
        ```bash
        cp apps/api/.env.example apps/api/.env
        ```
        Then, fill in the required values in `apps/api/.env`:
        ```
        # Server Configuration
        PORT=8000

        # MongoDB Connection
        MONGO_URI=your_mongodb_connection_string

        # JWT Configuration
        JWT_SECRET=your_super_secret_jwt_key
        JWT_EXPIRES_IN=1d

        # OpenAI API Key
        OPENAI_API_KEY=your_openai_api_key
        ```

    *   **For the Mobile App:**
        The mobile app will get its API URL from an environment variable. Create a `.env` file in `apps/mobile/`:
        ```bash
        touch apps/mobile/.env
        ```
        Add the following variable, pointing to your local API server:
        ```
        EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1
        ```

4.  **Run the project:**

    *   **Run the Backend API:**
        ```bash
        pnpm --filter api dev
        ```
        The API server should now be running on `http://localhost:8000`.

    *   **Run the Mobile App:**
        In a new terminal window:
        ```bash
        pnpm --filter mobile start
        ```
        This will start the Expo development server. You can now scan the QR code with the Expo Go app on your phone or run it in a simulator.