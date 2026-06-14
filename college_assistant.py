"""
Smart College Assistant using LangChain Tool Calling Agent
Implements multiple tools for student-related calculations
"""

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json

# ============================================================================
# TOOL DEFINITIONS USING @tool DECORATOR
# ============================================================================

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> dict:
    """
    Calculate attendance percentage and exam eligibility status.
    
    Args:
        total_classes: Total number of classes held
        attended_classes: Number of classes attended by student
    
    Returns:
        Dictionary with attendance percentage and exam eligibility status
    """
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
    """
    Calculate average marks, grade, and pass/fail status from 5 subjects.
    
    Args:
        marks_subject1-5: Marks obtained in each of 5 subjects
    
    Returns:
        Dictionary with average marks, grade, and pass/fail status
    """
    marks_list = [marks_subject1, marks_subject2, marks_subject3, marks_subject4, marks_subject5]
    
    # Validate marks
    for marks in marks_list:
        if marks < 0 or marks > 100:
            return {"error": "Marks must be between 0 and 100"}
    
    average_marks = sum(marks_list) / len(marks_list)
    
    # Determine grade
    if average_marks >= 90:
        grade = "A"
    elif average_marks >= 75:
        grade = "B"
    elif average_marks >= 60:
        grade = "C"
    else:
        grade = "D"
    
    # Determine pass/fail
    pass_fail = "Pass" if average_marks >= 50 else "Fail"
    
    return {
        "marks": marks_list,
        "average_marks": round(average_marks, 2),
        "grade": grade,
        "status": pass_fail
    }


@tool
def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> dict:
    """
    Calculate pending fee amount.
    
    Args:
        total_course_fee: Total course fee amount
        amount_paid: Amount already paid by student
    
    Returns:
        Dictionary with pending fee details
    """
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
    """
    Calculate library fine based on number of delayed days.
    Rule: Fine = ₹5 × Delayed Days
    
    Args:
        delayed_days: Number of days the book was delayed
    
    Returns:
        Dictionary with fine amount
    """
    if delayed_days < 0:
        return {"error": "Delayed days cannot be negative"}
    
    fine_per_day = 5  # ₹5 per day
    total_fine = delayed_days * fine_per_day
    
    return {
        "delayed_days": delayed_days,
        "fine_per_day": fine_per_day,
        "total_fine": total_fine,
        "fine_message": f"Fine Amount: ₹{total_fine}"
    }


@tool
def hostel_fee_calculator(monthly_hostel_fee: float, number_of_months: int) -> dict:
    """
    Calculate total hostel fee.
    
    Args:
        monthly_hostel_fee: Monthly hostel fee amount
        number_of_months: Number of months stayed in hostel
    
    Returns:
        Dictionary with total hostel fee
    """
    if monthly_hostel_fee < 0 or number_of_months < 0:
        return {"error": "Fee and months cannot be negative"}
    
    total_hostel_fee = monthly_hostel_fee * number_of_months
    
    return {
        "monthly_hostel_fee": monthly_hostel_fee,
        "number_of_months": number_of_months,
        "total_hostel_fee": round(total_hostel_fee, 2),
        "fee_breakdown": f"₹{monthly_hostel_fee} × {number_of_months} months = ₹{round(total_hostel_fee, 2)}"
    }


# ============================================================================
# BONUS: STUDENT INFORMATION TOOL
# ============================================================================

# Sample student database
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


@tool
def student_information_tool(student_id: str) -> dict:
    """
    BONUS: Retrieve student details from student database using Student ID.
    
    Args:
        student_id: Student ID to look up
    
    Returns:
        Dictionary with student information or error message
    """
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
# AGENT SETUP AND EXECUTION
# ============================================================================

def create_college_assistant():
    """
    Create and configure the College Assistant agent.
    Uses a simplified approach compatible with current LangChain version.
    """
    # Define the tools list
    tools = [
        attendance_calculator,
        result_calculator,
        fee_balance_calculator,
        library_fine_calculator,
        hostel_fee_calculator,
        student_information_tool
    ]
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Create a simple agent executor class
    class SimpleAgent:
        def __init__(self, llm_with_tools, tools):
            self.llm = llm_with_tools
            self.tools = {tool.name: tool for tool in tools}
            self.verbose = True
            
        def invoke(self, inputs):
            query = inputs.get("input", "")
            print(f"\n{'='*70}")
            print(f"User Query: {query}")
            print(f"{'='*70}")
            
            # Get tool choice from LLM
            messages = [{"role": "user", "content": query}]
            response = self.llm.invoke(messages)
            
            print(f"\nAgent Thinking: {response.content}")
            
            # Process tool calls if any
            if hasattr(response, 'tool_calls') and response.tool_calls:
                output_parts = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_input = tool_call['args']
                    
                    print(f"\n>>> Invoking tool: {tool_name}")
                    print(f"    Input: {tool_input}")
                    
                    if tool_name in self.tools:
                        result = self.tools[tool_name].func(**tool_input)
                        print(f"    Output: {result}")
                        output_parts.append(f"{tool_name}: {result}")
                
                final_output = "\n".join(output_parts)
            else:
                final_output = response.content
            
            return {"output": final_output}
    
    # Return agent instance
    agent = SimpleAgent(llm_with_tools, tools)
    return agent


# ============================================================================
# TEST EXECUTION
# ============================================================================

def run_test_cases():
    """
    Run all test cases to verify the agent functionality.
    """
    print("="*80)
    print("SMART COLLEGE ASSISTANT - TEST CASES")
    print("="*80)
    print()
    
    # Initialize the agent
    agent_executor = create_college_assistant()
    
    # Test cases
    test_queries = [
        {
            "name": "Query 1",
            "query": "I attended 72 classes out of 90. Am I eligible for exams?"
        },
        {
            "name": "Query 2",
            "query": "My marks are 95, 90, 88, 91 and 87. What is my grade?"
        },
        {
            "name": "Query 3",
            "query": "My course fee is 50000 and I have paid 35000. How much fee is pending?"
        },
        {
            "name": "Query 4",
            "query": "I returned a library book 8 days late. What is the fine amount?"
        },
        {
            "name": "Query 5",
            "query": "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee."
        }
    ]
    
    # Run individual test cases
    for test in test_queries:
        print(f"\n{'-'*80}")
        print(f"{test['name']}: {test['query']}")
        print(f"{'-'*80}")
        
        try:
            result = agent_executor.invoke({"input": test['query']})
            print(f"\nAgent Response:\n{result['output']}\n")
        except Exception as e:
            print(f"Error executing query: {str(e)}\n")
    
    # Multi-tool Challenge
    print(f"\n{'='*80}")
    print("MULTI-TOOL CHALLENGE")
    print(f"{'='*80}")
    
    multi_tool_query = """
    I attended 80 classes out of 100.
    My marks are 90, 85, 88, 92 and 95.
    My course fee is 60000 and I paid 45000.
    
    Provide:
    1. Attendance Status
    2. Grade
    3. Pending Fee
    """
    
    print(f"\nQuery:\n{multi_tool_query}")
    print(f"\n{'-'*80}")
    
    try:
        result = agent_executor.invoke({"input": multi_tool_query})
        print(f"\nAgent Response:\n{result['output']}\n")
    except Exception as e:
        print(f"Error executing multi-tool query: {str(e)}\n")
    
    # Bonus: Student Information Query
    print(f"\n{'='*80}")
    print("BONUS: STUDENT INFORMATION RETRIEVAL")
    print(f"{'='*80}")
    
    bonus_query = "Can you retrieve the student information for student ID STU002?"
    
    print(f"\nQuery: {bonus_query}")
    print(f"\n{'-'*80}")
    
    try:
        result = agent_executor.invoke({"input": bonus_query})
        print(f"\nAgent Response:\n{result['output']}\n")
    except Exception as e:
        print(f"Error executing bonus query: {str(e)}\n")
    
    print(f"\n{'='*80}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_test_cases()
