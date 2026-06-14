# Quick Start Guide - Smart College Assistant

## 🚀 Get Started in 5 Minutes

### Option 1: Using OpenAI API (Easiest)

#### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key

#### Step 3: Set API Key
**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### Step 4: Run the Application
```bash
python college_assistant.py
```

Expected output: Agent will process all test cases with verbose logs showing each tool invocation.

---

### Option 2: Using Ollama (Free, Local LLM)

#### Step 1: Install Ollama
- Download from https://ollama.ai
- Install and run

#### Step 2: Download a Model
```bash
ollama pull llama2
```
(Other options: mistral, neural-chat, openchat)

#### Step 3: Start Ollama
```bash
ollama serve
```
Keep this running in a separate terminal.

#### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run with Ollama
```bash
python college_assistant_ollama.py
```

---

## 📋 Available Scripts

### 1. **college_assistant.py** (Main Application)
- Uses OpenAI API
- Runs all test cases
- Includes multi-tool challenge
- Full verbose output
```bash
python college_assistant.py
```

### 2. **college_assistant_ollama.py** (Local LLM Version)
- Uses Ollama (no API key needed)
- Suitable for offline use
```bash
python college_assistant_ollama.py
```

### 3. **test_tools_direct.py** (Direct Tool Testing)
- Tests each tool independently
- No LLM required
- Good for debugging
```bash
python test_tools_direct.py
```

---

## 🧪 Testing Individual Queries

You can also test specific queries by modifying the code:

```python
# In college_assistant.py, replace the run_test_cases() function call with:

agent = create_college_assistant()
result = agent.invoke({"input": "Your custom query here"})
print(result['output'])
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] API key set (for OpenAI) or Ollama running (for local)
- [ ] Run `python college_assistant.py`
- [ ] See verbose agent output
- [ ] All test cases pass

---

## 🔧 Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### OpenAI API Error
- Check API key is set correctly
- Verify key has remaining balance
- Check internet connection

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check URL: http://localhost:11434
- Try different model: `ollama pull mistral`

### Python Version Error
- Ensure Python 3.8+
- Check: `python --version`

---

## 📊 Expected Output Sample

```
================================================================================
SMART COLLEGE ASSISTANT - TEST CASES
================================================================================

Query 1: I attended 72 classes out of 90. Am I eligible for exams?
--------

> Entering new AgentExecutor...
> Invoking: `attendance_calculator` with `{'total_classes': 90, 'attended_classes': 72}`
> `{'attendance_percentage': 80.0, 'eligibility_status': 'Eligible for Exam', ...}`
> Finished chain.

Agent Response:
Based on your attendance record of 72 classes out of 90 total, your attendance 
percentage is 80.0%. Since this exceeds the 75% threshold, you ARE ELIGIBLE FOR 
EXAM. Your attendance is good and you can proceed with your examinations.
```

---

## 🎯 Key Features

✓ **5 Required Tools**
- Attendance Calculator
- Result Calculator  
- Fee Balance Calculator
- Library Fine Calculator
- Hostel Fee Calculator

✓ **Bonus Features**
- Student Information Retrieval Tool
- Error Handling
- Input Validation
- Structured Output Format

✓ **Agent Capabilities**
- Automatic tool selection
- Multi-tool queries
- Verbose logging
- Natural language understanding

---

## 📝 Notes

1. Each tool can be used independently without the agent
2. Verbose output shows exact tool calls and parameters
3. All calculations are validated with error handling
4. Agent can handle complex multi-part queries
5. Code is well-commented and extensible

---

## 🎓 For Assignment Submission

When submitting, include:
1. ✓ college_assistant.py (main code)
2. ✓ Screenshot of agent execution (from running the script)
3. ✓ Output showing all test cases
4. ✓ README.md documentation

---

Need help? Check the README.md file for detailed documentation.
