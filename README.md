# Codeforces Tracker

Codeforces Tracker is a web application built with Flask that allows users to track and compare Codeforces submissions of two users. The application retrieves Codeforces submissions for each user and displays them in a sorted manner based on the contest ID and problem code.

## Getting Started

Follow these steps to get the project up and running:

1. **Clone the repository to your local machine:**

    ```bash
    git clone https://github.com/your-username/codeforces-tracker.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd codeforces-tracker
    ```

3. **Install the required Python packages. It's recommended to use a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4. **Run the main.py file:**

    ```bash
    python3 main.py
    ```

5. **Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the Codeforces Tracker.**

## Usage

1. Enter the Codeforces usernames of two users in the provided form.
2. Specify the number of pages to scrape.
3. Click on the "Track" button.
4. View the submissions of both users sorted by contest ID and problem code.
