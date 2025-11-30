# SupportLine Agent 🚨

**SupportLine** is a Python-based emergency response application that helps users locate the nearest help centers in Bangalore. It combines **Agent-Based Modeling (Mesa)** with a reactive web interface built using **Solara**.

## 🌟 Features

* **Emergency Service Locator:** Quickly find nearest Police Stations, Hospitals, Cyber Crime units, Consultations, Pharmacies, and Fire stations.
* **Interactive Dashboard:** A modern, reactive UI powered by Solara.
* **Agent-Based Backend:** Utilizes `Mesa` to model help centers as agents (`CenterAgent`) to calculate distances and logic.
* **Data Driven:** Uses a JSON database (`centers.json`) of Bangalore locations to populate the map.
* **Manager Mode:** Includes a dedicated flow for registering new centers dynamically.
* [cite_start]**Container Ready:** Fully Dockerized for easy deployment on platforms like Hugging Face Spaces[cite: 1, 2].

## 🛠️ Tech Stack

* [cite_start]**Language:** Python 3.9 [cite: 1]
* **Frontend:** [Solara](https://solara.dev/)
* **Simulation:** [Mesa](https://mesa.readthedocs.io/)
* **Data:** JSON
* **Deployment:** Docker

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | Entry point for the application. |
| `backend.py` | Manages global state, themes, and Solara reactive variables. |
| `agents.py` | Defines Mesa agents: `CenterAgent` and `UserAgent`. |
| `centers.json` | Database containing help center coordinates and details. |
| `about.py` | The "About Us" view and team information. |
| `Dockerfile` | [cite_start]Configuration for building the Docker image[cite: 1]. |

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* pip

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/supportline-agent.git](https://github.com/your-username/supportline-agent.git)
    cd supportline-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    solara run main.py
    ```
    The app should now be running at `http://localhost:8765` (or the port specified in your console).

### 🐳 Docker Deployment

[cite_start]The application is configured to run on port `7860` inside the container (standard for Hugging Face Spaces)[cite: 3].

1.  **Build the image:**
    ```bash
    docker build -t supportline .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 7860:7860 supportline
    ```
