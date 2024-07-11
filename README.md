# YouTubed

A simple YouTube video and playlist downloader.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- Download videos from YouTube with ease.
- Supports multiple video formats and qualities.
- User-friendly command-line interface.

## Installation

### Prerequisites

Ensure you have the following installed:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/mauriciobellon/youtubed.git
    cd youtubed
    ```
2. **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

## Usage

To use the YouTube downloader, run:
```bash
youtubed --help
```
This command will display all available options and usage instructions for YouTubed.

### Examples
Download a video:

```bash
youtubed download --url "https://www.youtube.com/watch?v=example"
```

Download playlist:

```bash
youtubed download --url "https://www.youtube.com/playlist?list=example"
```

## Contributing
Contributions are welcome! Please read our Contributing Guidelines for details on the process of submitting pull requests.

- Fork the repository.

- Create a new branch (git checkout -b feature-branch).

- Commit your changes (git commit -m 'Add some feature').

- Push to the branch (git push origin feature-branch).

- Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/mauriciobellon/youtubed/blob/main/LICENSE) file for details.

## Contact

Author: [Mauricio Bellon](https://github.com/mauriciobellon)

For any questions, feel free to open an issue or contact me directly.
