```
# Resumate AI: Smart Resume Builder

## Project Description

Resumate AI is an innovative, user-friendly resume creation platform designed to empower students and job seekers to effortlessly craft professional and impactful resumes. Leveraging a robust backend and a highly interactive frontend, the platform provides a rich selection of ready-to-use, customizable templates. Users can easily input their information, select a template, and generate high-quality PDF resumes, streamlining the job application process. This MVP focuses on core functionalities: user authentication, template browsing, resume data input, and PDF generation.

## Technical Stack

The Resumate AI platform is built with a modern, scalable, and highly performant technical stack, ensuring a robust and maintainable application.

**Frontend:**
*   **Framework:** Next.js 14+ (React) - Utilizes the App Router for server-side rendering (SSR), static site generation (SSG), and enhanced performance, alongside a file-system based routing.
*   **Language:** TypeScript - For strong typing, improved code quality, and better developer experience.
*   **Styling:** Tailwind CSS - A utility-first CSS framework for rapidly building custom designs directly in HTML.
*   **UI Components:** Shadcn/UI (optional, but recommended for reusable, accessible components).
*   **Data Fetching:** TanStack Query (React Query) - For efficient data fetching, caching, and synchronization with the server.
*   **Form Management:** React Hook Form with Zod - For performant and validated form handling.

**Backend:**
*   **Framework:** NestJS (Node.js) - A progressive Node.js framework for building efficient, reliable, and scalable server-side applications, leveraging TypeScript and inspired by Angular.
*   **Language:** TypeScript.
*   **ORM:** Prisma - A modern, type-safe ORM for database access, schema migrations, and database introspection.
*   **Database:** PostgreSQL - A powerful, open-source relational database known for its reliability, feature robustness, and performance.
*   **Authentication:** JWT-based authentication integrated with Passport.js strategies, potentially leveraging AWS Cognito User Pools for user management.
*   **PDF Generation:** Puppeteer - A Node.js library that provides a high-level API to control headless Chrome or Chromium, enabling the conversion of dynamic HTML templates into high-quality PDF documents.

**Cloud Infrastructure (AWS):**
*   **Cloud Provider:** Amazon Web Services (AWS)
*   **Compute:** AWS ECS Fargate - Serverless compute for containers, abstracting away infrastructure management.
*   **Database Service:** AWS RDS for PostgreSQL - Managed relational database service.
*   **Object Storage:** AWS S3 - Scalable storage for generated PDF resumes, user avatars, and template assets.
*   **Content Delivery Network (CDN):** AWS CloudFront - Delivers frontend assets with low latency and high transfer speeds.
*   **Identity & Access Management:** AWS Cognito - Managed user directory service for authentication (User Pools) and authorization (Identity Pools).
*   **Infrastructure as Code (IaC):** Terraform - Defines and provisions the entire cloud infrastructure programmatically, ensuring consistency and repeatability.

**Development & Operations:**
*   **Version Control:** Git / GitHub
*   **CI/CD:** GitHub Actions - For automated build, test, and deployment pipelines.
*   **Containerization:** Docker - For consistent development and deployment environments.
*   **Monorepo Management:** Yarn Workspaces - To manage multiple interdependent packages (frontend, backend, shared types, etc.) within a single repository.
*   **Local Development Orchestration:** Docker Compose - For setting up and running local development services (database, local S3, etc.).

## Detailed, Hierarchical Folder Structure

```
resumate-ai/
├── .github/
│   └── workflows/
│       ├── backend-deploy.yml    # GitHub Actions workflow for backend deployment
│       └── frontend-deploy.yml   # GitHub Actions workflow for frontend deployment
├── apps/
│   ├── api/                      # NestJS Backend Application
│   │   ├── src/
│   │   │   ├── auth/             # Authentication module (JWT, Passport strategies)
│   │   │   ├── users/            # User management module (CRUD)
│   │   │   ├── templates/        # Resume template management module (CRUD)
│   │   │   ├── resumes/          # Resume generation & management module
│   │   │   ├── files/            # File upload/download module (S3 integration)
│   │   │   ├── pdf-generator/    # PDF generation service/module (Puppeteer integration)
│   │   │   ├── config/           # Application configuration
│   │   │   ├── main.ts           # Application entry point
│   │   │   └── app.module.ts     # Root module
│   │   ├── Dockerfile            # Dockerfile for backend service
│   │   ├── nest-cli.json         # NestJS CLI configuration
│   │   ├── package.json          # Node.js dependencies for backend
│   │   └── tsconfig.json         # TypeScript configuration for backend
│   └── web/                      # Next.js Frontend Application
│       ├── public/               # Static assets (images, fonts, etc.)
│       ├── src/
│       │   ├── app/              # Next.js App Router structure
│       │   │   ├── (auth)/       # Group for authentication routes (login, register)
│       │   │   │   ├── login/
│       │   │   │   └── register/
│       │   │   ├── (main)/       # Group for main application routes
│       │   │   │   ├── dashboard/
│       │   │   │   ├── templates/
│       │   │   │   ├── resume/[id]/
│       │   │   │   └── settings/
│       │   │   ├── api/          # Route handlers for API routes (if needed, prefer backend API)
│       │   │   ├── globals.css   # Global styles
│       │   │   ├── layout.tsx    # Root layout component
│       │   │   └── page.tsx      # Root page component
│       │   ├── components/       # Reusable React components (UI library agnostic)
│       │   │   ├── common/
│       │   │   └── ui/           # Components built with Shadcn/UI (if used)
│       │   ├── hooks/            # Custom React hooks
│       │   ├── lib/              # Client-side utilities, API clients (TanStack Query setup)
│       │   └── styles/           # Tailwind CSS specific styles / other utility styles
│       ├── Dockerfile            # Dockerfile for frontend service
│       ├── next.config.js        # Next.js configuration
│       ├── package.json          # Node.js dependencies for frontend
│       ├── postcss.config.js     # PostCSS configuration
│       ├── tailwind.config.ts    # Tailwind CSS configuration
│       └── tsconfig.json         # TypeScript configuration for frontend
├── packages/
│   ├── config/                   # Shared configuration constants (e.g., environment variables types)
│   │   └── index.ts
│   ├── db/                       # Database schema and Prisma client
│   │   ├── migrations/           # Prisma migrations
│   │   ├── schema.prisma         # Prisma schema definition
│   │   └── index.ts              # Prisma client export
│   ├── ui/                       # Shared UI components (if common across multiple frontends/storybooks)
│   │   ├── src/
│   │   │   └── components/
│   │   └── package.json
│   └── types/                    # Shared TypeScript interfaces, types, enums (DTOs, models)
│       └── index.ts
├── infra/
│   └── aws/                      # Terraform modules for AWS infrastructure provisioning
│       ├── vpc.tf                # VPC and networking
│       ├── ecs.tf                # ECS cluster, services, tasks definitions
│       ├── rds.tf                # RDS PostgreSQL instance
│       ├── s3.tf                 # S3 buckets for assets and PDFs
│       ├── cognito.tf            # Cognito User Pool and Identity Pool
│       ├── cloudfront.tf         # CloudFront distribution for frontend
│       ├── iam.tf                # IAM roles and policies
│       ├── variables.tf          # Input variables for Terraform modules
│       └── outputs.tf            # Output variables from Terraform modules
├── docs/
│   ├── ARCHITECTURE.md           # High-level architecture overview
│   ├── API.md                    # Backend API documentation (OpenAPI/Swagger)
│   └── DATABASE_SCHEMA.md        # Database schema diagrams and explanations
├── scripts/                      # Utility scripts (e.g., local setup, deploy helpers, DB seed)
│   └── setup-local-dev.sh
├── .env.example                  # Example environment variables
├── docker-compose.yml            # Local development environment orchestration
├── package.json                  # Root package.json for Yarn Workspaces
├── README.md                     # Project README
└── tsconfig.json                 # Monorepo base TypeScript configuration
```

## Setup Instructions

Follow these steps to get the Resumate AI project up and running on your local machine.

### Prerequisites

*   Node.js (LTS version, e.g., 18.x or 20.x)
*   Yarn (v1.x or v3+ Berry with `nodeLinker: pnp` or `nodeLinker: node-modules` configured in `.yarnrc.yml`)
*   Docker & Docker Compose
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resumate-ai.git
cd resumate-ai
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory of the project based on the `.env.example` file.

```bash
cp .env.example .env
```

Edit the `.env` file and fill in the necessary values. For local development, you might use:

```env
# Database Configuration (for local Docker PostgreSQL)
DATABASE_URL="postgresql://user:password@localhost:5432/resumate_db"

# AWS S3 Configuration (for local MinIO or actual S3)
AWS_ACCESS_KEY_ID="your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
AWS_REGION="your_aws_region"
AWS_S3_BUCKET_NAME="resumate-pdfs-bucket"
AWS_S3_ENDPOINT="http://localhost:9000" # For MinIO local S3 emulation

# JWT Secret (for backend authentication)
JWT_SECRET="supersecretjwtkey"

# Frontend Configuration (for Next.js)
NEXT_PUBLIC_API_URL="http://localhost:3001/api" # Backend API URL
NEXT_PUBLIC_APP_URL="http://localhost:3000" # Frontend URL
```

### 3. Start Local Database and Services with Docker Compose

Navigate to the root of the project and start the Docker Compose services. This will spin up a PostgreSQL database and potentially a MinIO server for local S3 emulation.

```bash
docker-compose up -d
```

### 4. Install Dependencies

Install root dependencies and then dependencies for all workspaces using Yarn.

```bash
yarn install
```

### 5. Setup Database Schema and Seed Data

Apply Prisma migrations to create the database schema.

```bash
yarn workspace @resumate-ai/db prisma migrate dev --name init # Or use `prisma db push` for quick dev sync
yarn workspace @resumate-ai/db prisma generate # Generate Prisma client
# Optional: Seed initial data (e.g., default templates)
# yarn workspace @resumate-ai/api db:seed
```

### 6. Run the Backend (API)

Navigate to the `apps/api` directory or use `yarn workspace` command.

```bash
yarn workspace @resumate-ai/api start:dev # Runs NestJS backend in watch mode
```

The backend API will typically run on `http://localhost:3001`.

### 7. Run the Frontend (Web)

Navigate to the `apps/web` directory or use `yarn workspace` command.

```bash
yarn workspace @resumate-ai/web dev # Runs Next.js frontend in development mode
```

The frontend application will typically run on `http://localhost:3000`.

### 8. Access the Application

Open your web browser and navigate to `http://localhost:3000`. You should now be able to register an account, browse templates, and create resumes.

---

**Note on Production Deployment:**
Production deployment will utilize the Dockerfiles within `apps/api` and `apps/web`, deployed to AWS ECS Fargate, with infrastructure managed by Terraform within the `infra/aws` directory. CI/CD pipelines are defined in `.github/workflows` to automate this process.
```