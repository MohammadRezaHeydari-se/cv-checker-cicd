# CV Checker — CI/CD Project

A simple PDF resume checker built with Python and FastAPI.

This project was created for the CI/CD course at Nackademin (DEVOPS25). The main goal is to demonstrate how code can be tested, packaged, published, deployed, and verified automatically.

## 1. Application

Users can upload a PDF resume and check six common CV fields:

- Name
- Email
- Phone
- Experience
- Education
- Skills

The application detects common English and Swedish CV headings and displays the extracted information.

It uses PyMuPDF for PDF text extraction and Python regular expressions and rules for detecting information. It does not use AI or permanently store uploaded files.

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Web interface |
| `POST /upload` | Analyze a PDF resume |
| `GET /health` | Application health check |
| `GET /version` | Deployed commit version |

CV detection is rule-based, so some resume formats or scanned PDFs may not work correctly.

## 2. Technologies

| Technology | Purpose |
| --- | --- |
| Python 3.13 / FastAPI | Application and API |
| PyMuPDF | PDF text extraction |
| Pytest | Automated testing |
| Git and GitHub | Version control and pull requests |
| GitHub Actions | CI/CD automation |
| Docker | Containerization |
| GHCR | Docker image registry |
| Ubuntu / Self-hosted Runner | Deployment server |
| Nginx | Reverse proxy |

## 3. CI/CD Architecture

~~~text
Feature Branch
      |
      v
Pull Request to main
      |
      v
CI: Pytest -> Docker Build
      |
      v
Merge to main
      |
      v
Publish: Build -> Tag -> Push to GHCR
      |
      v
CD: Ubuntu Self-hosted Runner
      |
      v
Pull Image -> Replace Container
      |
      v
Health Check + Version Check
      |
      +-- Success -> Keep New Version
      |
      +-- Failure -> Automatic Rollback
~~~

The project uses three separate GitHub Actions workflows: CI, Publish, and Deploy.

## 4. Continuous Integration (CI)

Workflow: `.github/workflows/ci.yml`

CI runs automatically when a pull request targets `main`.

1. The `test` job installs Python 3.13 and the application dependencies.
2. Pytest runs the automated tests.
3. If the tests pass, the `docker-build` job builds the Docker image.

The `main` branch is protected. Changes require a pull request and a successful `test` check before merging.

**Why?** CI helps detect problems before code reaches the main branch. The Docker build also verifies that the application can be packaged.

## 5. Publishing Docker Images

Workflow: `.github/workflows/publish.yml`

After a push to `main`, GitHub Actions:

1. Builds a Docker image.
2. Tags it with the full Git commit SHA.
3. Authenticates to GitHub Container Registry (GHCR).
4. Pushes the image to GHCR.

Image repository:

`ghcr.io/mohammadrezaheydari-se/cv-checker-cicd`

**Why?** Commit-based image tags make releases traceable. Each deployed image can be linked to its source code.

## 6. Continuous Deployment (CD)

Workflow: `.github/workflows/deploy.yml`

Deployment starts after the Publish workflow finishes successfully.

A self-hosted GitHub Actions runner on an Ubuntu virtual machine performs the deployment:

1. Verify that the published commit is the latest commit on `main`.
2. Pull the new image before stopping the current container.
3. Save the previous image reference for rollback.
4. Replace the running Docker container.
5. Verify `/health`.
6. Verify that `/version` matches the expected commit SHA.

The container uses port `8080`, mapped to `127.0.0.1:8001` on Ubuntu. Nginx forwards incoming requests to the application.

The deployment workflow uses a concurrency group to prevent overlapping deployments.

**Why?** CD automates delivery to the server, while health and version checks confirm that the expected version is actually running.

## 7. Automatic Rollback

A successful test and Docker build do not guarantee that an application will work after deployment.

If deployment or verification fails, the workflow attempts to restore the previous Docker image.

### Controlled failure test

I tested rollback by changing the application port in the Dockerfile from `8080` to `8081`, while the deployment configuration still expected port `8080`.

- CI tests passed.
- Docker build passed.
- The image was published to GHCR.
- Deployment failed during the health check.
- Automatic rollback restored the previous healthy image.

The deployment workflow correctly reported a failure, even though the previous application version was restored.

**Why?** This demonstrates that runtime verification is necessary and that rollback can reduce the impact of a failed release.

**Limitations:** Rollback requires a previous image. This setup is not zero-downtime, and infrastructure failures may require manual recovery.

## 8. Challenges and Lessons Learned

### Health check timing

An early deployment failed because the application was not ready when the health check started.

I added retries to the deployment and rollback health checks.

### Ubuntu disk space

During the rollback experiment, the Ubuntu VM ran out of disk space and the self-hosted runner could not complete its job.

I recovered the server, removed unnecessary archived logs and unused project images, and configured systemd journal limits.

After the runner recovered, I reran the deployment workflow and confirmed that automatic rollback worked.

### Lessons learned

- CI and CD have different responsibilities.
- Passing tests does not guarantee a healthy deployment.
- Docker images tagged with commit SHAs are easier to track.
- Health checks and version checks verify the actual deployment.
- Rollback helps recover from bad releases.
- Server resources and runner health affect CI/CD reliability.

## 9. Final Result

The completed project demonstrates:

**Pull Request -> Tests -> Docker Build -> Merge -> GHCR -> Ubuntu -> Verification**

The application supports English and Swedish CV detection and was tested with a real PDF resume.

The full pipeline completed successfully, and the deployed application's `/health` and `/version` endpoints were verified on Ubuntu.

A controlled failed deployment also demonstrated successful automatic rollback.

## 10. Course

**Nackademin — DEVOPS25**

Continuous Integration and Continuous Delivery
