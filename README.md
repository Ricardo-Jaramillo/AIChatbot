# Chatbot Project

This project is a chatbot application that integrates with the DeepSeek API and provides a user interface using Streamlit. The architecture is designed with Object-Oriented Programming (OOP) principles, allowing for easy switching between interfaces, environments, and language models such as OpenAI and Llama.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Integration with multiple LLM models (OpenAI, DeepSeek, Llama).
- User interfaces: Streamlit for web-based interaction and CLI for command-line interaction.
- Environment management using a `.env` file for secure API key storage.
- Docker support for easy deployment.
- Model tuning and personality evaluation scripts.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chatbot-project.git
   cd chatbot-project
   ```

2. Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Build the Docker image (optional):
   ```
   docker build -t chatbot-project .
   ```

## Usage

To run the chatbot application, execute the following command:

```
python src/main.py
```

You can choose between the Streamlit interface or the CLI interface based on your preference.

## Project Structure

```
chatbot-project
├── src
│   ├── main.py                  # Entry point for the chatbot application
│   ├── interfaces                # Contains interface implementations
│   ├── llm_models                # Contains language model implementations
│   ├── utils                     # Utility functions and classes
│   └── evaluation                # Scripts for model tuning and personality evaluation
├── .env                          # Environment variables and API keys
├── .gitignore                    # Files and directories to ignore in Git
├── Dockerfile                    # Docker setup for the project
├── requirements.txt              # Required Python packages
└── README.md                     # Project documentation
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.