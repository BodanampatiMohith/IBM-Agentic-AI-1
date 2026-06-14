"""
Alternative Implementation using Ollama (Local LLM)
Use this if you don't want to use OpenAI API
"""

from langchain_core.tools import tool
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ============================================================================
# IDENTICAL TOOLS (same as college_assistant.py)
# ============================================================================

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> dict:
    """Calculate attendance percentage and exam eligibility status."""
    if total_classes <= 0:
        return {"error": "Total classes must be greater than 0"}
    
    if attended_classes > total_classes:
        return {"error": "Attended classes cannot exceed total classes"}
    
    attendance_percentage = (attended_classes / total_classes) * 100
    is_eligible = attendance_percentage >= 75
    
    return {
        "total_classes": total_classes,
        "attended_classes": attended_classes,
        "attendance_percentage": round(attendance_percentage, 2),
        "eligibility_status": "Eligible for Exam" if is_eligible else "Not Eligible for Exam",
        "is_eligible": is_eligible
    }


@tool
def result_calculator(marks_subject1: int, marks_subject2: int, marks_subject3: int, 
                     marks_subject4: int, marks_subject5: int) -> dict:
    """Calculate average marks, grade, and pass/fail status from 5 subjects."""
    marks_list = [marks_subject1, marks_subject2, marks_subject3, marks_subject4, marks_subject5]
    
    for marks in marks_list:
        if marks < 0 or marks > 100:
            return {"error": "Marks must be between 0 and 100"}
    
    average_marks = sum(marks_list) / len(marks_list)
    
    if average_marks >= 90:
        grade = "A"
    elif average_marks >= 75:
        grade = "B"
    elif average_marks >= 60:
        grade = "C"
    else:
        grade = "D"
    
    pass_fail = "Pass" if average_marks >= 50 else "Fail"
    
    return {
        "marks": marks_list,
        "average_marks": round(average_marks, 2),
        "grade": grade,
        "status": pass_fail
    }


@tool
def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> dict:
    """Calculate pending fee amount."""
    if amount_paid > total_course_fee:
        return {"error": "Amount paid cannot exceed total course fee"}
    
    if amount_paid < 0 or total_course_fee < 0:
        return {"error": "Fee amounts cannot be negative"}
    
    pending_fee = total_course_fee - amount_paid
    
    return {
        "total_course_fee": total_course_fee,
        "amount_paid": amount_paid,
        "pending_fee": round(pending_fee, 2),
        "payment_status": "Fully Paid" if pending_fee == 0 else f"Pending: ₹{round(pending_fee, 2)}"
    }


@tool
def library_fine_calculator(delayed_days: int) -> dict:
    """Calculate library fine based on number of delayed days."""
    if delayed_days < 0:
        return {"error": "Delayed days cannot be negative"}
    
    fine_per_day = 5
    total_fine = delayed_days * fine_per_day
    
    return {
        "delayed_days": delayed_days,
        "fine_per_day": fine_per_day,
        "total_fine": total_fine,
        "fine_message": f"Fine Amount: ₹{total_fine}"
    }


@tool
def hostel_fee_calculator(monthly_hostel_fee: float, number_of_months: int) -> dict:
    """Calculate total hostel fee."""
    if monthly_hostel_fee < 0 or number_of_months < 0:
        return {"error": "Fee and months cannot be negative"}
    
    total_hostel_fee = monthly_hostel_fee * number_of_months
    
    return {
        "monthly_hostel_fee": monthly_hostel_fee,
        "number_of_months": number_of_months,
        "total_hostel_fee": round(total_hostel_fee, 2),
        "fee_breakdown": f"₹{monthly_hostel_fee} × {number_of_months} months = ₹{round(total_hostel_fee, 2)}"
    }


@tool
def student_information_tool(student_id: str) -> dict:
    """Retrieve student details from database using Student ID."""
    STUDENT_DATABASE = {
        "STU001": {
            "name": "Rajesh Kumar",
            "email": "rajesh.kumar@college.edu",
            "course": "B.Tech Computer Science",
            "semester": 4,
            "enrollment_date": "2023-08-15"
        },
        "STU002": {
            "name": "Priya Sharma",
            "email": "priya.sharma@college.edu",
            "course": "B.Tech Electronics",
            "semester": 3,
            "enrollment_date": "2024-01-10"
        },
        "STU003": {
            "name": "Amit Patel",
            "email": "amit.patel@college.edu",
            "course": "B.Tech Mechanical",
            "semester": 2,
            "enrollment_date": "2024-08-20"
        },
        "STU004": {
            "name": "Anjali Singh",
            "email": "anjali.singh@college.edu",
            "course": "B.Tech Civil",
            "semester": 1,
            "enrollment_date": "2025-08-01"
        }
    }
    
    if student_id in STUDENT_DATABASE:
        student_info = STUDENT_DATABASE[student_id]
        return {
            "student_id": student_id,
            "found": True,
            **student_info
        }
    else:
        return {
            "student_id": student_id,
            "found": False,
            "error": f"Student with ID {student_id} not found in database",
            "available_ids": list(STUDENT_DATABASE.keys())
        }


# ============================================================================
# AGENT WITH OLLAMA
# ============================================================================

def create_college_assistant_ollama():
    """
    Create College Assistant agent using Ollama (Local LLM).
    Ensure Ollama is running: ollama serve
    """
    tools = [
        attendance_calculator,
        result_calculator,
        fee_balance_calculator,
        library_fine_calculator,
        hostel_fee_calculator,
        student_information_tool
    ]
    
    # Initialize Ollama LLM (make sure it's running on localhost:11434)
    llm = ChatOllama(
        model="llama2",  # or "mistral", "neural-chat", etc.
        base_url="http://localhost:11434",
        temperature=0.7
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful College Assistant that helps students with:
1. Attendance calculations and exam eligibility
2. Result calculations including grades and pass/fail status
3. Fee balance calculations
4. Library fine calculations
5. Hostel fee calculations
6. Student information retrieval

Use the provided tools to answer student queries accurately and comprehensively.
Always provide clear explanations along with the calculations."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create and return the agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor


if __name__ == "__main__":
    print("="*80)
    print("OLLAMA VERSION - Smart College Assistant")
    print("="*80)
    print("\nMake sure Ollama is running:")
    print("$ ollama serve")
    print("\nThen run this script")
    print("\nSupported models: llama2, mistral, neural-chat, etc.")
    print("="*80)
    
    try:
        agent = create_college_assistant_ollama()
        
        # Test query
        query = "I attended 72 classes out of 90. Am I eligible for exams?"
        print(f"\nTest Query: {query}\n")
        result = agent.invoke({"input": query})
        print(f"\nResponse:\n{result['output']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure Ollama is running on localhost:11434")
        print("Run: ollama serve")
