# Django Channels Async Chat consumer


## Want to use this project?

### 0. Fork/Clone the repository on your server 

### 1. have docker-compose and python on :
This document guides you through installing Docker, Docker Compose, and Python on Windows, macOS, and Linux.These tools are essential for developing and deploying applications in containerized environments.Important: Please make sure you have administrator privileges on your system before proceeding.Choosing the Right Version
    
    Docker: Check the latest supported version for your operating system on the official Docker website: https://docs.docker.com/install/
    Docker Compose: Ensure your chosen Docker version is compatible with the Docker Compose version. Refer to the Compose documentation: https://docs.docker.com/compose/install/
    Python: Consider your project requirements and choose a compatible version (e.g., Python 3.x is recommended). Check the official Python website: https://www.python.org/downloads/
    
#### Installation Instructions
    
    Windows:
    
        Docker Desktop: Download and install the latest Docker Desktop for Windows from https://www.docker.com/products/docker-desktop.
        Python: Download and install the latest Python installer for Windows from https://www.python.org/downloads/windows/.
        Docker Compose: Open a PowerShell window as administrator and run the following command:
    
    PowerShell
    
    (New-Object System.Net.WebClient).DownloadFile('https://github.com/docker/compose/releases/download/v2.7.1/docker-compose-Windows-x86_64.exe', 'docker-compose.exe')
    Move-Item docker-compose.exe -Destination c:\Users\<your_username>\AppData\Local\Docker\
    

    
    macOS:
    
        Docker: Download and install the latest Docker Desktop for macOS from https://www.docker.com/products/docker-desktop.
        Python: Use Homebrew to install Python by running the following command in your terminal:
    
    Bash
    
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
    
    Use code with caution.
    
        Docker Compose: Download and install the latest Docker Compose binary for macOS from https://github.com/docker/compose/releases/. Extract the binary and add it to your PATH.
    
    Linux:
    
        Docker: Follow the official installation instructions for your specific Linux distribution: [[invalid URL removed]]([invalid URL removed])
    
        Python: Use your package manager to install Python:
            Debian/Ubuntu: sudo apt install python3
            Fedora/CentOS: sudo dnf install python3
            Arch Linux: sudo pacman -S python
    
        Docker Compose: Install Docker Compose by running the following command in your terminal:
    
    Bash
    
    sudo curl -L https://github.com/docker/compose/releases/download/v2.7.1/docker-compose-Linux-x86_64 -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    Use code with caution.
    
    Verification:
    
        Open a terminal or command prompt and run docker --version to check Docker installation.
        Run docker-compose --version to verify Docker Compose installation.
        Type python --version to confirm Python installation.

1. Install the requirements:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

1. Apply the migrations:

    ```sh
    (venv)$ python manage.py migrate
    ```

1. Start a Redis server for backing storage:

    ```sh
    (venv)$ docker run -p 6379:6379 -d redis:5
    ```

1. Run the server:

    ```sh
    (venv)$ python manage.py runserver
    ```

1. By default, only authenticated users can chat. To create a test user:

    ```sh
    (venv)$ python manage.py createsuperuser
    ```

1. Log in using your newly created user at [http://localhost:8000/admin/](http://localhost:8000/admin/).

1. Navigate to [http://localhost:8000/chat/](http://localhost:8000/chat/).
