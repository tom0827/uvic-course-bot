# UVic Course Bot

A Discord bot designed to provide students with course information, prerequisites, descriptions, and more for the University of Victoria.

## Features

- **Course Prerequisites:** Retrieve prerequisites and corequisites for specific courses.
- **Course Descriptions:** Get detailed descriptions of courses offered.
- **HEAT Outlines:** Access course outlines via the HEAT system.
- **Section Information:** View detailed section and scheduling information for courses.
- **Discord Integration:** Easy-to-use commands for interaction within Discord servers.

## Setup

### Prerequisites

- Docker (For local development and testing)

### Docker Deployment (For Local Development)

1. Clone the repository:
   ```
   git clone https://github.com/tom0827/uvic-course-bot.git
   cd uvic-course-bot
   ```

2. Build and run the Docker image:
   ```
   docker compose up --build
   ```

## Commands

### Sections
Retrieve all sections with their meeting times and current enrollment
```
/sections department:<department> course_number:<course_number> term:<term> year:<year>
```

### Prerequisites
Retrieve prerequisites and corequisites for a course:
```
/prereqs department:<department> course_number:<course_number>
```

### Course Description
Fetch a course description:
```
/description department:<department> course_number:<course_number>
```

### HEAT Outline
Get the course outline from the HEAT system:
```
/outline department:<department> course_number:<course_number> term:<term> year:<year>
```

## Contributing

Contributions are welcome! Please open an issue or create a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).