INSERT INTO accounts_subject ("SubjectID", "SubjectName", "SubjectDescription")
VALUES
    (0, 'Git', 'Version control system used for tracking changes in source code.'),
    (1, 'Docker', 'Platform to develop, ship, and run applications in containers.');

INSERT INTO accounts_course ("CourseID", "SubjectID_id", "CourseTitle", "CourseDescription", "CourseDifficulty", "Content")
VALUES
    (10, 0, 'Intro to Git', 'Learn the basics of Git: repositories, commits, branches, and remotes.', 1, 'Introduction to Git

Git is a powerful and widely used tool in software development. This tutorial is designed for complete beginners with no prior knowledge of version control systems (VCS). We will start from the most basic concepts and progressively introduce Git fundamental features.

Why Do We Need Version Control?

When working on any project involving files such as writing code, documents, or designs changes are made over time. Without a proper system, managing these changes can become challenging.

Consider a simple scenario: You are developing a program and save versions manually by copying the folder.

- myproject_v1
- myproject_v2
- myproject_v2_final
- myproject_v2_final_really

This approach quickly becomes disorganized: files duplicate unnecessarily, it is difficult to track what changed between versions, reverting to an earlier state is cumbersome, and collaborating with others risks overwriting work.

The illustration above demonstrates the chaos of managing multiple file versions manually without a version control system.

A version control system (VCS) solves these problems by automatically tracking every change to files, storing a complete history, and enabling safe collaboration.

This diagram contrasts centralized VCS (one central server holds the master copy) with distributed VCS (every developer has a full copy of the entire history).

Git is a distributed version control system, meaning each user has a complete repository on their computer, allowing work offline and providing robust backup.

Initializing a Git Repository

To start using Git in a project folder, open a terminal (command line) in that directory and run:

git init

This command creates a new Git repository, initializing a hidden .git folder that stores all version history and metadata.

The command used to initialize a new Git repository in the current directory is git init.

After initialization, Git automatically creates a default branch. Traditionally, the primary branch in a Git repository is called master, though many modern setups now use main.

The Core Git Workflow

Git manages files through three main areas:

- Working Directory: The actual files you see and edit.
- Staging Area (also called Index): A holding area for changes you select to include in the next save point.
- Repository (committed history): The permanent storage of all saved versions in the .git folder.

This official diagram from the Git documentation illustrates the relationship between the working directory, staging area, and repository.

The typical workflow is:

1. Edit files in the working directory.
2. Stage the changes you want to save.
3. Commit (record) the staged changes as a permanent snapshot.

Staging Changes

After modifying files, you must explicitly select which changes to include in the next version. This is done with:

git add <filename>

To stage all changes at once:

git add .

The command to stage changes for the next commit in Git is git add.

Staging allows precise control: you can modify multiple files but commit only specific ones.

Committing Changes

A commit creates a snapshot of the staged changes, permanently recording them in the repository history.

Use the command:

git commit -m A clear, descriptive message about the changes

The -m flag provides the message directly; a good message explains why the change was made.

The command used to record staged changes to the repository is git commit.

Each commit receives a unique identifier (a long hash), along with details like author, date, and message.

Viewing the Commit History

To see the sequence of commits (the project history), run:

git log

This lists commits from newest to oldest, showing the hash, author, date, and message for each.

For a more compact view:

git log --oneline

The command used to view the commit history is git log.

This visualization represents a typical Git commit history as a branching graph (even a simple linear history appears this way).

Summary of Essential Commands

- git init → Initialize a new repository.
- git add → Stage changes for committing.
- git commit → Record staged changes with a message.
- git log → View the commit history.

These concepts and commands form the foundation of Git. Practice them in a test folder to gain confidence before applying them to real projects. Subsequent tutorials will cover branching, collaboration, and remote repositories.'),
    
    (11, 0, 'Advanced Git', 'Deep dive into advanced Git workflows, rebasing, and conflict resolution.', 2, 'Introduction to Git

Git is a powerful and widely used tool in software development. This tutorial is designed for complete beginners with no prior knowledge of version control systems (VCS). We will start from the most basic concepts and progressively introduce Git fundamental features.

Why Do We Need Version Control?

When working on any project involving files such as writing code, documents, or designs changes are made over time. Without a proper system, managing these changes can become challenging.

Consider a simple scenario: You are developing a program and save versions manually by copying the folder.

- myproject_v1
- myproject_v2
- myproject_v2_final
- myproject_v2_final_really

This approach quickly becomes disorganized: files duplicate unnecessarily, it is difficult to track what changed between versions, reverting to an earlier state is cumbersome, and collaborating with others risks overwriting work.

The illustration above demonstrates the chaos of managing multiple file versions manually without a version control system.

A version control system (VCS) solves these problems by automatically tracking every change to files, storing a complete history, and enabling safe collaboration.

This diagram contrasts centralized VCS (one central server holds the master copy) with distributed VCS (every developer has a full copy of the entire history).

Git is a distributed version control system, meaning each user has a complete repository on their computer, allowing work offline and providing robust backup.

Initializing a Git Repository

To start using Git in a project folder, open a terminal (command line) in that directory and run:

git init

This command creates a new Git repository, initializing a hidden .git folder that stores all version history and metadata.

The command used to initialize a new Git repository in the current directory is git init.

After initialization, Git automatically creates a default branch. Traditionally, the primary branch in a Git repository is called master, though many modern setups now use main.

The Core Git Workflow

Git manages files through three main areas:

- Working Directory: The actual files you see and edit.
- Staging Area (also called Index): A holding area for changes you select to include in the next save point.
- Repository (committed history): The permanent storage of all saved versions in the .git folder.

This official diagram from the Git documentation illustrates the relationship between the working directory, staging area, and repository.

The typical workflow is:

1. Edit files in the working directory.
2. Stage the changes you want to save.
3. Commit (record) the staged changes as a permanent snapshot.

Staging Changes

After modifying files, you must explicitly select which changes to include in the next version. This is done with:

git add <filename>

To stage all changes at once:

git add .

The command to stage changes for the next commit in Git is git add.

Staging allows precise control: you can modify multiple files but commit only specific ones.

Committing Changes

A commit creates a snapshot of the staged changes, permanently recording them in the repository history.

Use the command:

git commit -m A clear, descriptive message about the changes

The -m flag provides the message directly; a good message explains why the change was made.

The command used to record staged changes to the repository is git commit.

Each commit receives a unique identifier (a long hash), along with details like author, date, and message.

Viewing the Commit History

To see the sequence of commits (the project history), run:

git log

This lists commits from newest to oldest, showing the hash, author, date, and message for each.

For a more compact view:

git log --oneline

The command used to view the commit history is git log.

This visualization represents a typical Git commit history as a branching graph (even a simple linear history appears this way).

Summary of Essential Commands

- git init → Initialize a new repository.
- git add → Stage changes for committing.
- git commit → Record staged changes with a message.
- git log → View the commit history.

These concepts and commands form the foundation of Git. Practice them in a test folder to gain confidence before applying them to real projects. Subsequent tutorials will cover branching, collaboration, and remote repositories.'),

    (20, 1, 'Intro to Docker', 'Introduction to containers, images, and Docker CLI basics.', 1, 'Introduction to Docker

Docker has revolutionized the way software is developed, deployed, and run. This tutorial is designed for complete beginners with no prior knowledge of containerization or Docker. We will start from the most basic concepts and progressively introduce Docker fundamental features.

What is Docker and Why Do We Need It?

When developing software, a common problem arises: the application works perfectly on your computer but fails when deployed to a server or when a colleague tries to run it. This happens because of differences in operating systems, installed libraries, system configurations, and dependency versions.

Consider a typical scenario: You build a web application on your laptop using Python 3.9, PostgreSQL 12, and specific libraries. When you deploy it to a production server running different versions or when a teammate uses Python 3.7, the application breaks with cryptic errors.

Traditional solutions include writing lengthy setup documentation, creating complex installation scripts, or using virtual machines. However, these approaches have drawbacks: documentation becomes outdated, installation scripts fail on different systems, and virtual machines are heavy and slow to start.

Docker solves this problem by packaging your application together with everything it needs to run into a standardized unit called a container.

Understanding Containers

A container is a lightweight, standalone, executable package that includes everything needed to run a piece of software: the code, runtime environment, system tools, libraries, and settings.

Think of a container like a shipping container in the physical world. Just as shipping containers standardize how goods are transported regardless of their contents, Docker containers standardize how applications run regardless of the underlying infrastructure.

Containers are different from virtual machines. A virtual machine includes an entire operating system, which makes it heavy (gigabytes in size) and slow to start (minutes). A container shares the host operating system kernel and includes only the application and its dependencies, making it lightweight (megabytes in size) and fast to start (seconds).

The key benefits of containers include consistency across different environments, isolation between applications, efficient resource usage, fast startup times, and easy scalability.

Installing Docker

Before working with Docker, you need to install Docker Desktop (for Windows and Mac) or Docker Engine (for Linux). Visit the official Docker website and download the appropriate version for your operating system.

After installation, verify Docker is working by opening a terminal and running:

docker --version

This command displays the installed Docker version, confirming the installation was successful.

Understanding Docker Images

A Docker image is a read-only template that contains instructions for creating a container. Think of an image as a blueprint or recipe, while a container is the actual running instance created from that image.

Images are built in layers. Each layer represents a set of file system changes. This layered approach makes images efficient: if multiple images share common layers, those layers are stored only once.

For example, if you have two applications both using Ubuntu as a base, the Ubuntu layer is shared between them, saving disk space.

Images are stored in registries. The most popular registry is Docker Hub, a public repository containing thousands of pre-built images for common software like databases, web servers, and programming language runtimes.

Running Your First Container

The simplest way to start with Docker is to run a pre-built image from Docker Hub. Let us run a basic test container:

docker run hello-world

This command does several things automatically: it checks if the hello-world image exists locally, downloads it from Docker Hub if not found, creates a container from the image, runs the container, displays a welcome message, and then stops the container.

The command to run a container from an image is docker run.

Let us try something more interactive. Run an Ubuntu container:

docker run -it ubuntu bash

The -it flags make the container interactive, allowing you to type commands inside it. The ubuntu is the image name, and bash is the command to run inside the container.

You are now inside a Linux container. You can run commands like ls, pwd, or apt-get update. When finished, type exit to leave the container.

Listing and Managing Containers

To see all running containers, use:

docker ps

To see all containers including stopped ones, use:

docker ps -a

The command to list running containers is docker ps.

Each container has a unique ID and a randomly generated name. You can reference containers by either their ID or name in other commands.

To stop a running container:

docker stop <container-id-or-name>

To start a stopped container:

docker start <container-id-or-name>

To remove a container:

docker rm <container-id-or-name>

Managing Docker Images

To see all images stored locally on your system:

docker images

The command to list all local images is docker images.

To download an image without running it:

docker pull <image-name>

For example, to download the nginx web server image:

docker pull nginx

To remove an image from your system:

docker rmi <image-name-or-id>

Note that you cannot remove an image if containers are using it. You must first remove those containers.

Running Containers with Port Mapping

Many applications need to be accessible from outside the container. For example, a web server needs to accept HTTP requests. Docker uses port mapping to expose container ports to the host system.

To run an nginx web server and make it accessible on port 8080:

docker run -d -p 8080:80 nginx

The -d flag runs the container in detached mode (in the background). The -p 8080:80 maps port 8080 on your host to port 80 inside the container.

Now you can open a web browser and navigate to http://localhost:8080 to see the nginx welcome page.

The -p flag is used for port mapping in the format host-port:container-port.

Running Containers with Environment Variables

Applications often need configuration through environment variables. Docker allows passing these variables when running containers.

docker run -e MY_VARIABLE=value <image-name>

For example, many database images use environment variables for initial setup:

docker run -e MYSQL_ROOT_PASSWORD=mypassword mysql

The -e flag sets environment variables inside the container.

Running Containers with Volume Mounts

By default, any data created inside a container is lost when the container is removed. To persist data, Docker uses volumes.

A volume is a storage location managed by Docker that exists outside the container filesystem. Data in volumes persists even after containers are deleted.

To create a volume and use it:

docker volume create my-data
docker run -v my-data:/data <image-name>

The -v flag mounts a volume. The syntax is volume-name:container-path.

You can also mount a directory from your host system into the container:

docker run -v /host/path:/container/path <image-name>

This is useful for development, allowing you to edit files on your host and see changes reflected immediately in the container.

Understanding Dockerfiles

While using pre-built images is convenient, you will often need to create custom images for your applications. This is done with a Dockerfile.

A Dockerfile is a text file containing instructions for building a Docker image. Each instruction creates a new layer in the image.

Here is a simple example of a Dockerfile for a Python application:

FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python app.py

Let us understand each instruction:

FROM specifies the base image to build upon. Here we use the official Python 3.9 image.

WORKDIR sets the working directory inside the container. All subsequent commands run in this directory.

COPY copies files from your host into the container. The first COPY adds the requirements file.

RUN executes commands during the build process. Here it installs Python dependencies.

The second COPY adds the rest of the application code.

CMD specifies the command to run when a container starts from this image.

Building Images from Dockerfiles

To build an image from a Dockerfile, navigate to the directory containing the Dockerfile and run:

docker build -t my-app:v1 .

The -t flag tags the image with a name and optional version. The period (.) at the end specifies the build context (current directory).

The command to build an image from a Dockerfile is docker build.

Docker reads the Dockerfile, executes each instruction in order, and creates a new image. Each instruction creates a layer, and Docker caches these layers. If you rebuild and nothing has changed in early layers, Docker reuses the cached layers, making subsequent builds much faster.

Container Naming and Cleanup

By default, Docker assigns random names to containers. You can specify a custom name:

docker run --name my-container nginx

This makes it easier to reference the container in other commands.

To remove all stopped containers:

docker container prune

To remove all unused images:

docker image prune

To remove everything (containers, images, volumes, networks) that is not currently in use:

docker system prune -a

These cleanup commands help manage disk space as Docker can accumulate many stopped containers and unused images over time.

Basic Docker Commands Summary

- docker run: Create and start a container from an image
- docker ps: List running containers
- docker ps -a: List all containers
- docker images: List all local images
- docker pull: Download an image from a registry
- docker build: Build an image from a Dockerfile
- docker stop: Stop a running container
- docker start: Start a stopped container
- docker rm: Remove a container
- docker rmi: Remove an image
- docker logs: View container logs
- docker exec: Execute a command in a running container

Understanding the Docker Workflow

A typical Docker workflow follows these steps:

1. Write your application code
2. Create a Dockerfile that defines how to build your application image
3. Build the image using docker build
4. Test the image by running it locally with docker run
5. Push the image to a registry (like Docker Hub) to share it
6. Pull and run the image on any system that has Docker installed

This workflow ensures your application runs identically everywhere, from your laptop to production servers.

Practical Example: Running a Simple Web Server

Let us put these concepts together with a practical example. We will create a simple HTML page and serve it with nginx.

First, create a directory and add an index.html file with some content.

Then create a Dockerfile:

FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html

Build the image:

docker build -t my-website .

Run the container:

docker run -d -p 8080:80 my-website

Visit http://localhost:8080 in your browser to see your website running in a container.

Best Practices for Beginners

Keep these best practices in mind as you learn Docker:

Use official images from Docker Hub as base images when possible. They are well-maintained and secure.

Keep your images small by using minimal base images like alpine variants.

Do not run containers as the root user in production environments.

Use .dockerignore files to exclude unnecessary files from your build context, similar to .gitignore for Git.

Tag your images with meaningful version numbers rather than relying on the default latest tag.

Clean up unused containers and images regularly to save disk space.

Always specify exact versions in your Dockerfile FROM instructions for reproducibility.

Next Steps

You now understand the fundamental concepts of Docker: what containers and images are, how to run containers, how to create custom images with Dockerfiles, and the basic Docker CLI commands.

The next tutorial on Advanced Docker will cover more sophisticated topics including networking between containers, managing persistent data with volumes in production, using Docker Compose for multi-container applications, optimizing images for production, and deployment strategies.

Practice these basics by containerizing simple applications. Try creating Dockerfiles for different types of applications and experiment with various Docker commands to build confidence before moving to advanced topics.'),

    (21, 1, 'Advanced Docker', 'Advanced Docker networking, volumes, and production deployments.', 2, 'Advanced Docker

Building on foundational Docker knowledge, this tutorial explores advanced techniques used in production environments. You should already be comfortable with basic Docker concepts like containers, images, Dockerfiles, and commands such as docker run, docker build, and docker ps before proceeding.

Understanding Docker Networking in Depth

When you run a single container, networking is straightforward. However, real applications typically consist of multiple services that need to communicate: a web application talking to a database, a backend API connecting to a cache, or microservices coordinating with each other.

Docker provides several networking options to facilitate container communication while maintaining isolation and security.

Docker Network Types

Docker supports multiple network drivers, each suited for different scenarios:

Bridge Network: The default network type. Containers on the same bridge network can communicate with each other using container names as hostnames. This network is isolated from the host network.

Host Network: Removes network isolation between the container and the host. The container uses the host network stack directly. This offers better performance but less isolation.

None Network: Disables all networking for a container. Useful for containers that do not need network access.

Overlay Network: Enables communication between containers running on different Docker hosts. Essential for Docker Swarm and distributed applications.

Macvlan Network: Assigns a MAC address to containers, making them appear as physical devices on the network. Useful for legacy applications that expect direct network access.

The command to list all Docker networks is docker network ls.

Creating and Using Custom Bridge Networks

While the default bridge network works, custom bridge networks offer advantages: automatic DNS resolution between containers, better isolation, and the ability to connect and disconnect containers dynamically.

To create a custom bridge network:

docker network create my-network

To run a container on this network:

docker run --network my-network --name web nginx

To run another container on the same network:

docker run --network my-network --name api python:3.9

Now the web container can communicate with the api container using the hostname api, and vice versa. Docker internal DNS resolves these names automatically.

The command to create a new network is docker network create.

You can inspect a network to see which containers are connected:

docker network inspect my-network

To connect a running container to a network:

docker network connect my-network existing-container

To disconnect a container from a network:

docker network disconnect my-network existing-container

Inter-Container Communication Example

Let us create a practical example with a web application and a database communicating over a custom network.

First, create the network:

docker network create app-network

Run a PostgreSQL database:

docker run -d --name database --network app-network -e POSTGRES_PASSWORD=secret postgres

Run a web application that connects to the database:

docker run -d --name webapp --network app-network -e DB_HOST=database -e DB_PASSWORD=secret my-web-app

The web application can now connect to PostgreSQL using the hostname database. Docker DNS resolution handles the name-to-IP mapping automatically.

Exposing Services with Port Publishing

While containers on the same network can communicate freely, external access requires explicit port publishing. You can publish ports when creating the network connection:

docker run -d --name webapp --network app-network -p 8080:80 my-web-app

This makes the web application accessible from outside Docker on port 8080, while it can still communicate with the database using the internal network.

Advanced Volume Management

In the introduction, we covered basic volume usage. Production environments require more sophisticated data persistence strategies.

Volume Types in Docker

Docker supports three types of mounts:

Volumes: Managed by Docker, stored in a Docker-specific location on the host. The preferred method for persistent data.

Bind Mounts: Map a specific host directory to a container directory. Useful for development but less portable.

tmpfs Mounts: Stored in host memory only, never written to disk. Useful for sensitive temporary data.

Creating and Managing Volumes

To create a named volume:

docker volume create my-data

To list all volumes:

docker volume ls

To inspect a volume:

docker volume inspect my-data

This shows where Docker stores the volume data on the host system.

To remove a volume:

docker volume rm my-data

To remove all unused volumes:

docker volume prune

The command to create a named volume is docker volume create.

Using Volumes in Production

For databases and stateful applications, volumes are critical. Here is how to run a production database with a persistent volume:

docker volume create postgres-data

docker run -d --name production-db -v postgres-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=securepass postgres

Even if you remove and recreate the container, the data persists in the postgres-data volume.

For applications requiring multiple volumes:

docker run -d --name app -v app-data:/data -v app-logs:/var/log/app -v app-config:/etc/app my-application

Volume Backup and Restore

To backup data from a volume, you can run a temporary container that mounts the volume and copies data out:

docker run --rm -v postgres-data:/data -v /host/backup:/backup ubuntu tar czf /backup/postgres-backup.tar.gz /data

To restore data:

docker run --rm -v postgres-data:/data -v /host/backup:/backup ubuntu tar xzf /backup/postgres-backup.tar.gz -C /

The --rm flag automatically removes the container after it exits, keeping your system clean.

Advanced Dockerfile Techniques

Writing efficient Dockerfiles is crucial for production deployments. Poor Dockerfile practices lead to large images, slow builds, and security vulnerabilities.

Multi-Stage Builds

Multi-stage builds allow you to use multiple FROM statements in a single Dockerfile. This is powerful for separating build dependencies from runtime dependencies, resulting in smaller final images.

Consider a Go application:

FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ./myapp

The first stage uses the full golang image to compile the application. The second stage uses a minimal alpine image and copies only the compiled binary. The final image is much smaller because it does not include the Go compiler and build tools.

The same pattern works for Node.js, Java, Python, and other languages where build tools differ from runtime requirements.

Layer Caching Optimization

Docker caches each layer in a Dockerfile. Understanding this helps optimize build times.

Consider this inefficient Dockerfile:

FROM node:16
WORKDIR /app
COPY . .
RUN npm install
CMD npm start

Every time you change any source file, Docker invalidates the cache from the COPY . . instruction onward, forcing npm install to run again even if dependencies have not changed.

An optimized version:

FROM node:16
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
CMD npm start

Now npm install only reruns when package.json or package-lock.json change, dramatically speeding up builds during development.

The principle is to order Dockerfile instructions from least frequently changing to most frequently changing.

Using .dockerignore

Similar to .gitignore, a .dockerignore file tells Docker which files to exclude from the build context. This reduces build context size and build time.

Example .dockerignore:

node_modules
.git
.env
*.log
README.md
.dockerignore
Dockerfile

This prevents sending unnecessary files to the Docker daemon during builds.

Security Best Practices in Dockerfiles

Never run containers as root. Create a non-privileged user:

FROM node:16
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
CMD node server.js

Use specific image versions, not latest:

FROM node:16.14.2-alpine

This ensures reproducible builds. The latest tag can change unexpectedly, breaking your application.

Minimize the number of layers by combining RUN commands:

RUN apt-get update && apt-get install -y package1 package2 && apt-get clean && rm -rf /var/lib/apt/lists/*

Scan images for vulnerabilities regularly using tools like docker scan or Trivy.

Docker Compose for Multi-Container Applications

While docker run works for single containers, production applications typically involve multiple interconnected services. Managing these with individual docker run commands becomes unwieldy.

Docker Compose solves this by defining multi-container applications in a YAML file.

Creating a docker-compose.yml File

Here is an example for a web application with a database and cache:

version: 3.8

services:
  web:
    build: ./web
    ports:
      - 8080:80
    environment:
      - DB_HOST=database
      - REDIS_HOST=cache
    depends_on:
      - database
      - cache
    networks:
      - app-network
    volumes:
      - ./web:/app

  database:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

  cache:
    image: redis:7-alpine
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  db-data:

This configuration defines three services with their relationships, networks, and volumes in a single declarative file.

Docker Compose Commands

To start all services:

docker-compose up

To start in detached mode:

docker-compose up -d

To stop all services:

docker-compose down

To stop and remove volumes:

docker-compose down -v

To view logs from all services:

docker-compose logs

To view logs from a specific service:

docker-compose logs web

To rebuild images:

docker-compose build

To scale a service:

docker-compose up -d --scale web=3

The command to start services defined in docker-compose.yml is docker-compose up.

Environment Variables in Compose

You can use environment variables in docker-compose.yml and load them from .env files:

version: 3.8

services:
  web:
    image: my-app
    environment:
      - DATABASE_URL=${DB_URL}
      - API_KEY=${API_KEY}

Create a .env file:

DB_URL=postgresql://user:pass@database:5432/mydb
API_KEY=your-secret-key

Docker Compose automatically loads variables from .env files.

Health Checks

Production deployments should include health checks to ensure services are running correctly:

version: 3.8

services:
  web:
    image: my-app
    healthcheck:
      test: [CMD, curl, -f, http://localhost/health]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

Docker marks the container as unhealthy if the health check fails, and orchestration tools can restart it automatically.

Production Deployment Strategies

Running Docker in production requires additional considerations beyond development environments.

Resource Limits

Always set resource limits to prevent containers from consuming all host resources:

docker run -d --name app --memory=512m --cpus=1.0 my-app

In Docker Compose:

services:
  web:
    image: my-app
    deploy:
      resources:
        limits:
          cpus: 1.0
          memory: 512M
        reservations:
          cpus: 0.5
          memory: 256M

Logging Configuration

By default, Docker stores logs in JSON files, which can grow indefinitely. Configure log rotation:

docker run -d --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 my-app

In Docker Compose:

services:
  web:
    image: my-app
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: 3

For production, consider using centralized logging solutions like ELK stack, Splunk, or cloud-native options.

Restart Policies

Configure containers to restart automatically on failure:

docker run -d --restart unless-stopped my-app

Restart policies:
- no: Never restart (default)
- on-failure: Restart only on non-zero exit
- always: Always restart regardless of exit status
- unless-stopped: Always restart unless explicitly stopped

In Docker Compose:

services:
  web:
    image: my-app
    restart: unless-stopped

Container Orchestration

For production deployments at scale, use orchestration platforms:

Docker Swarm: Built into Docker, simpler but less powerful than Kubernetes. Good for smaller deployments.

Kubernetes: Industry standard for container orchestration. Powerful but complex. Handles scheduling, scaling, load balancing, and self-healing.

Amazon ECS, Azure Container Instances, Google Cloud Run: Cloud-native managed container services.

Introduction to Docker Swarm

Docker Swarm allows managing a cluster of Docker hosts as a single virtual system.

Initialize a swarm:

docker swarm init

Deploy a service:

docker service create --name web --replicas 3 -p 8080:80 nginx

Scale a service:

docker service scale web=5

List services:

docker service ls

Swarm handles load balancing, service discovery, and rolling updates automatically.

Image Optimization for Production

Smaller images deploy faster, use less disk space, and have smaller attack surfaces.

Use Alpine-based images when possible:

FROM node:16-alpine instead of FROM node:16

Alpine Linux is a minimal distribution, resulting in images often 10x smaller.

Remove build dependencies in multi-stage builds as shown earlier.

Combine commands to reduce layers:

RUN apt-get update && apt-get install -y package && apt-get clean

Use COPY instead of ADD unless you specifically need ADD features like automatic tar extraction.

Security in Production

Run containers with read-only filesystems when possible:

docker run -d --read-only --tmpfs /tmp my-app

Use Docker secrets for sensitive data instead of environment variables:

echo my-secret-password | docker secret create db-password -

docker service create --secret db-password my-app

Regularly update base images to patch security vulnerabilities.

Use image scanning tools in your CI/CD pipeline.

Enable Docker Content Trust to ensure image integrity:

export DOCKER_CONTENT_TRUST=1

Monitoring and Debugging

Use docker stats to monitor resource usage:

docker stats

Use docker logs to troubleshoot issues:

docker logs --tail 100 -f container-name

Execute commands in running containers for debugging:

docker exec -it container-name bash

Use docker inspect to view detailed container configuration:

docker inspect container-name

For production, implement proper monitoring with Prometheus, Grafana, or cloud-native monitoring solutions.

Summary of Advanced Concepts

This tutorial covered advanced Docker techniques essential for production deployments:

- Custom bridge networks for container communication
- Advanced volume management and backup strategies
- Multi-stage builds and Dockerfile optimization
- Docker Compose for multi-container applications
- Resource limits and restart policies
- Logging configuration and health checks
- Container orchestration with Docker Swarm
- Security best practices
- Image optimization techniques

These skills enable you to design, deploy, and maintain robust containerized applications in production environments. Continue practicing with real projects, experiment with orchestration platforms, and stay updated with Docker best practices as the ecosystem evolves.');

