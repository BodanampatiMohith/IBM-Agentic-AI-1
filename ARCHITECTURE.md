# Implementation Architecture & Design Document

## Overview
Smart College Assistant is a LangChain-based AI agent that intelligently processes student queries and invokes appropriate calculation tools.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                               │
│        ("I attended 72 classes out of 90...")                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ChatPromptTemplate                            │
│  (System: You are a college assistant)                          │
│  (Input: User query)                                            │
│  (Scratchpad: Agent reasoning)                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM (ChatOpenAI)                             │
│  Understands query and determines needed tools                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│          Tool Calling Agent (create_tool_calling_agent)         │
│  Decides which tools to call based on LLM output                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Available Tools                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ • attendance_calculator(total, attended)                │   │
│  │ • result_calculator(m1, m2, m3, m4, m5)               │   │
│  │ • fee_balance_calculator(total_fee, paid)             │   │
│  │ • library_fine_calculator(delayed_days)               │   │
│  │ • hostel_fee_calculator(monthly_fee, months)          │   │
│  │ • student_information_tool(student_id)                │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│               AgentExecutor (verbose=True)                       │
│  Orchestrates tool calls and manages execution flow              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Structured Response                           │
│  {"attendance_percentage": 80.0, "eligibility": "Eligible"}     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Final User Response                           │
│  LLM formats structured output into natural language             │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tool Specifications

### 1. Attendance Calculator
**Purpose:** Determine exam eligibility based on attendance percentage

**Input Parameters:**
- `total_classes: int` - Total number of classes held
- `attended_classes: int` - Number of classes attended

**Output Structure:**
```python
{
    "total_classes": 90,
    "attended_classes": 72,
    "attendance_percentage": 80.0,
    "eligibility_status": "Eligible for Exam",
    "is_eligible": true
}
```

**Logic:**
- Attendance % = (Attended / Total) × 100
- Eligible if % ≥ 75, else Not Eligible

**Example:** 72/90 = 80% → Eligible ✓

---

### 2. Result Calculator
**Purpose:** Calculate grades and pass/fail status from marks

**Input Parameters:**
- `marks_subject1-5: int` - Marks (0-100) for each subject

**Output Structure:**
```python
{
    "marks": [95, 90, 88, 91, 87],
    "average_marks": 90.2,
    "grade": "A",
    "status": "Pass"
}
```

**Grading Logic:**
| Average | Grade |
|---------|-------|
| ≥ 90    | A     |
| 75-89   | B     |
| 60-74   | C     |
| < 60    | D     |

**Pass/Fail:** Pass if Average ≥ 50

**Example:** Avg 90.2 → Grade A, Pass ✓

---

### 3. Fee Balance Calculator
**Purpose:** Calculate outstanding fee balance

**Input Parameters:**
- `total_course_fee: float` - Total fee amount
- `amount_paid: float` - Amount already paid

**Output Structure:**
```python
{
    "total_course_fee": 50000,
    "amount_paid": 35000,
    "pending_fee": 15000.0,
    "payment_status": "Pending: ₹15000.0"
}
```

**Logic:**
- Pending = Total - Paid
- Validation: Paid ≤ Total

**Example:** 50000 - 35000 = ₹15000 pending ✓

---

### 4. Library Fine Calculator
**Purpose:** Calculate library fine for overdue books

**Input Parameters:**
- `delayed_days: int` - Number of days book was late

**Output Structure:**
```python
{
    "delayed_days": 8,
    "fine_per_day": 5,
    "total_fine": 40,
    "fine_message": "Fine Amount: ₹40"
}
```

**Logic:**
- Fine = Days × ₹5
- Per day charge: ₹5 (can be customized)

**Example:** 8 days × ₹5 = ₹40 ✓

---

### 5. Hostel Fee Calculator
**Purpose:** Calculate total hostel accommodation fees

**Input Parameters:**
- `monthly_hostel_fee: float` - Monthly fee
- `number_of_months: int` - Duration of stay

**Output Structure:**
```python
{
    "monthly_hostel_fee": 6000,
    "number_of_months": 5,
    "total_hostel_fee": 30000.0,
    "fee_breakdown": "₹6000 × 5 months = ₹30000.0"
}
```

**Logic:**
- Total = Monthly × Months

**Example:** ₹6000 × 5 = ₹30000 ✓

---

### 6. Student Information Tool (Bonus)
**Purpose:** Retrieve student profile from database

**Input Parameters:**
- `student_id: str` - Student ID to lookup

**Output Structure (Found):**
```python
{
    "student_id": "STU002",
    "found": true,
    "name": "Priya Sharma",
    "email": "priya.sharma@college.edu",
    "course": "B.Tech Electronics",
    "semester": 3,
    "enrollment_date": "2024-01-10"
}
```

**Output Structure (Not Found):**
```python
{
    "student_id": "STU999",
    "found": false,
    "error": "Student with ID STU999 not found in database",
    "available_ids": ["STU001", "STU002", "STU003", "STU004"]
}
```

**Database:**
- STU001: Rajesh Kumar - B.Tech CS
- STU002: Priya Sharma - B.Tech Electronics
- STU003: Amit Patel - B.Tech Mechanical
- STU004: Anjali Singh - B.Tech Civil

---

## Agent Configuration

### ChatPromptTemplate Structure
```
System Role: College Assistant
- Specializes in student calculations
- Uses provided tools accurately
- Explains results clearly

Human Input: Actual user query

Agent Scratchpad: 
- Tool calls made
- Results obtained
- Intermediate reasoning
```

### Agent Executor Settings
```python
agent_executor = AgentExecutor(
    agent=agent,                      # Tool calling agent
    tools=tools,                       # All available tools
    verbose=True,                      # Detailed logs
    handle_parsing_errors=True        # Graceful error handling
)
```

### Verbose Output Includes
1. Tool invocation details
2. Input parameters
3. Tool output
4. LLM reasoning
5. Final response

---

## Query Processing Examples

### Simple Query (Single Tool)
```
User: "I attended 72 classes out of 90. Am I eligible?"

Agent Flow:
1. Understand query → attendance calculation needed
2. Extract parameters → total=90, attended=72
3. Call → attendance_calculator(90, 72)
4. Get result → 80% attendance, Eligible
5. Format response → Natural language explanation
```

### Complex Query (Multi-Tool)
```
User: "I attended 80 classes out of 100. My marks are 90, 85, 88, 92, 95.
       My course fee is 60000 and I paid 45000."

Agent Flow:
1. Parse query → 3 separate calculations needed
2. Call attendance_calculator(100, 80)
3. Call result_calculator(90, 85, 88, 92, 95)
4. Call fee_balance_calculator(60000, 45000)
5. Aggregate results
6. Format consolidated response
```

---

## Error Handling Strategy

### Input Validation
- Attendance: classes > 0, attended ≤ total
- Marks: 0-100 range per subject
- Fees: amounts ≥ 0, paid ≤ total
- Days: ≥ 0 (no negative values)

### Error Responses
```python
{
    "error": "Descriptive error message",
    "suggestion": "What user should do"
}
```

### AgentExecutor Error Handling
- `handle_parsing_errors=True` prevents crashes
- Gracefully handles LLM response parsing issues
- Returns meaningful error messages

---

## Design Principles

1. **Modularity:** Each tool is independent and testable
2. **Clarity:** Tools have clear names and docstrings
3. **Validation:** Input validation at tool level
4. **Extensibility:** Easy to add new tools
5. **Documentation:** Comprehensive docstrings
6. **User-Friendly:** Natural language responses

---

## Key Features

✅ **LangChain Integration**
- Uses @tool decorator for tool definition
- create_tool_calling_agent() for automatic tool selection
- AgentExecutor for orchestration

✅ **Tool Calling**
- LLM automatically selects appropriate tools
- Handles multi-tool queries
- Parameters extracted from natural language

✅ **Verbose Output**
- Shows thinking process
- Tool call details visible
- Parameter extraction shown

✅ **Error Resilience**
- Input validation
- Error handling
- Graceful degradation

✅ **Extensibility**
- Add new tools easily
- Modify grading criteria
- Customize fine rates
- Extend student database

---

## Testing Approach

### Unit Testing (test_tools_direct.py)
- Tests each tool independently
- Verifies calculations
- Tests edge cases
- No LLM required

### Integration Testing (college_assistant.py)
- Tests agent with LLM
- Multi-tool queries
- Full workflow validation

### Test Coverage
- 5 Required tools ✓
- 1 Bonus tool ✓
- 5 Individual queries ✓
- 1 Multi-tool challenge ✓
- Error cases ✓

---

## Performance Considerations

1. **LLM Latency:** OpenAI API calls take ~1-2 seconds
2. **Tool Execution:** Direct calculation tools are instant (<10ms)
3. **Total Response Time:** Typically 2-5 seconds
4. **Offline Mode:** Use Ollama for zero latency

---

## Future Enhancement Ideas

1. Database integration for persistent student records
2. Attendance trends analysis
3. Academic performance prediction
4. Payment plan generation
5. Exam schedule optimization
6. Multi-language support
7. Mobile app interface
8. Automated report generation

---

## Document Summary

This implementation provides a production-ready college assistant that:
- ✓ Meets all assignment requirements
- ✓ Uses LangChain tool calling agent
- ✓ Handles complex multi-tool queries
- ✓ Provides verbose, transparent output
- ✓ Includes comprehensive error handling
- ✓ Is extensible and maintainable
- ✓ Has clear documentation

---

**Version:** 1.0  
**Last Updated:** June 2026  
**Status:** Ready for Submission
