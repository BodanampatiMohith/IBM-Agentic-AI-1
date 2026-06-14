# Configuration File for Smart College Assistant
# This file contains settings that can be customized

# LLM Configuration
# Choose one: "openai" or "ollama"
LLM_PROVIDER = "openai"

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_API_KEY = ""  # Set via environment variable or here

# Ollama Settings
OLLAMA_MODEL = "llama2"  # Options: llama2, mistral, neural-chat, etc.
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TEMPERATURE = 0.7

# Agent Settings
AGENT_VERBOSE = True  # Enable detailed agent execution logs
HANDLE_PARSING_ERRORS = True  # Gracefully handle agent parsing errors

# Academic Settings
ATTENDANCE_THRESHOLD = 75  # Percentage required for exam eligibility
PASSING_MARKS = 50  # Minimum average marks to pass

# Grade Boundaries (Modify as needed)
GRADE_BOUNDARIES = {
    "A": 90,  # ≥ 90
    "B": 75,  # 75-89
    "C": 60,  # 60-74
    "D": 0    # < 60
}

# Library Fine Settings
LIBRARY_FINE_PER_DAY = 5  # ₹5 per delayed day

# Log Settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "assistant.log"

# Feature Flags
ENABLE_STUDENT_INFO = True  # Enable student information tool
ENABLE_BONUS_FEATURES = True  # Enable all bonus features
