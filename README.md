# Telegram Exam Bot

This project is a Telegram bot designed to improve communication between an educational institution and families. It provides an easy way for users to access transcripts and other information. The bot is developed based on real needs and is made public for those interested in Telegram bots and automation.

## Features

- Login with username and password
- Retrieve student transcripts
- Submit feedback on exams
- High security with password encryption

## Requirements

Before running the project, ensure that the following are installed:

- Python 3.6 or higher
- Python libraries: `telebot`, `psycopg2`, `bcrypt`

## Installation

1. Clone the project repository:

    ```bash
    git clone https://github.com/username/repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd repository
    ```

3. Install the required libraries:

    ```bash
    pip install pyTelegramBotAPI psycopg2-binary bcrypt
    ```

4. Configure database and API key settings:
   - Update the `constants.py` file with your database and Telegram API credentials.

## Usage

1. Start the bot by running the main script:

    ```bash
    python main.py
    ```

2. Interact with the bot in Telegram:
   - Use the `/start` command to begin.
   - Enter your username and password when prompted.
   - Choose to receive your transcript or provide feedback through the bot menu.

## Purpose

This bot is part of a larger project aimed at automating school operations through a web-based backend. We also plan to integrate it with attendance systems in the future. By making the code public, we hope to support those interested in Telegram bots and automation.

## Contributing

Feel free to submit issues, create pull requests, or suggest improvements. 

## Contact

For any questions or support, please contact mahdimoghassemi@gmail.com.
