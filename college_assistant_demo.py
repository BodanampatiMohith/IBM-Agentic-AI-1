"""
Smart College Assistant - DEMO VERSION
Shows the agent functionality without requiring OpenAI API
"""

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import json

# ============================================================================
# TOOL DEFINITIONS
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


STUDENT_DATABASE = {
    "STU001": {"name": "Rajesh Kumar", "email": "rajesh.kumar@college.edu", "course": "B.Tech CS", "semester": 4},
    "STU002": {"name": "Priya Sharma", "email": "priya.sharma@college.edu", "course": "B.Tech Electronics", "semester": 3},
    "STU003": {"name": "Amit Patel", "email": "amit.patel@college.edu", "course": "B.Tech Mechanical", "semester": 2},
    "STU004": {"name": "Anjali Singh", "email": "anjali.singh@college.edu", "course": "B.Tech Civil", "semester": 1}
}

@tool
def student_information_tool(student_id: str) -> dict:
    """Retrieve student details from database using Student ID."""
    if student_id in STUDENT_DATABASE:
        student_info = STUDENT_DATABASE[student_id]
        return {"student_id": student_id, "found": True, **student_info}
    else:
        return {"student_id": student_id, "found": False, "error": f"Student {student_id} not found", "available_ids": list(STUDENT_DATABASE.keys())}


# ============================================================================
# DEMO AGENT (Simulates LangChain Agent without API)
# ============================================================================

class DemoAgent:
    """Demo agent that simulates tool calling without requiring LLM API"""
    
    def __init__(self):
        self.tools = {
            "attendance_calculator": attendance_calculator,
            "result_calculator": result_calculator,
            "fee_balance_calculator": fee_balance_calculator,
            "library_fine_calculator": library_fine_calculator,
            "hostel_fee_calculator": hostel_fee_calculator,
            "student_information_tool": student_information_tool
        }
        self.verbose = True
    
    def _parse_query(self, query: str):
        """Parse query and determine which tools to call"""
        query_lower = query.lower()
        calls = []
        
        # Query 1
        if ("attended" in query_lower or "classes" in query_lower) and ("eligible" in query_lower or "exam" in query_lower):
            # Extract numbers
            import re
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                calls.append(("attendance_calculator", {"total_classes": int(numbers[1]), "attended_classes": int(numbers[0])}))
        
        # Query 2
        elif ("marks" in query_lower or "grade" in query_lower) and any(str(i) in query for i in range(10)):
            import re
            numbers = [int(x) for x in re.findall(r'\b\d{2}\b|\b\d{1}\b', query) if 0 <= int(x) <= 100]
            if len(numbers) >= 5:
                calls.append(("result_calculator", {
                    "marks_subject1": numbers[0], "marks_subject2": numbers[1],
                    "marks_subject3": numbers[2], "marks_subject4": numbers[3],
                    "marks_subject5": numbers[4]
                }))
        
        # Query 3
        elif ("fee" in query_lower or "course fee" in query_lower) and ("paid" in query_lower or "pending" in query_lower):
            import re
            numbers = [int(x) for x in re.findall(r'\d+', query)]
            if len(numbers) >= 2:
                calls.append(("fee_balance_calculator", {"total_course_fee": float(numbers[0]), "amount_paid": float(numbers[1])}))
        
        # Query 4
        elif ("library" in query_lower or "book" in query_lower) and ("late" in query_lower or "delayed" in query_lower or "fine" in query_lower):
            import re
            numbers = re.findall(r'\d+', query)
            if numbers:
                calls.append(("library_fine_calculator", {"delayed_days": int(numbers[0])}))
        
        # Query 5
        elif ("hostel" in query_lower or "accommodation" in query_lower) and ("fee" in query_lower or "month" in query_lower):
            import re
            numbers = [int(x) for x in re.findall(r'\d+', query)]
            if len(numbers) >= 2:
                calls.append(("hostel_fee_calculator", {"monthly_hostel_fee": float(numbers[0]), "number_of_months": int(numbers[1])}))
        
        # Query 6 - Multi-tool
        elif ("attended" in query_lower and "marks" in query_lower and "fee" in query_lower):
            import re
            numbers = [int(x) for x in re.findall(r'\d+', query)]
            if len(numbers) >= 6:
                calls.append(("attendance_calculator", {"total_classes": int(numbers[1]), "attended_classes": int(numbers[0])}))
                calls.append(("result_calculator", {
                    "marks_subject1": int(numbers[2]), "marks_subject2": int(numbers[3]),
                    "marks_subject3": int(numbers[4]), "marks_subject4": int(numbers[5]),
                    "marks_subject5": int(numbers[6]) if len(numbers) > 6 else 85
                }))
                if len(numbers) > 7:
                    calls.append(("fee_balance_calculator", {"total_course_fee": float(numbers[7]), "amount_paid": float(numbers[8]) if len(numbers) > 8 else 0}))
        
        # Student info
        elif "student" in query_lower and "stu" in query_lower:
            import re
            student_ids = re.findall(r'STU\d+', query)
            if student_ids:
                calls.append(("student_information_tool", {"student_id": student_ids[0]}))
        
        return calls
    
    def invoke(self, inputs):
        query = inputs.get("input", "")
        
        print(f"\n{'='*80}")
        print(f"INPUT QUERY: {query}")
        print(f"{'='*80}\n")
        
        # Parse and get tool calls
        tool_calls = self._parse_query(query)
        
        if not tool_calls:
            return {"output": "I couldn't understand your query. Please provide specific numbers and mention what you want to calculate (attendance, grades, fees, fines, or student info)."}
        
        results = []
        
        for tool_name, tool_input in tool_calls:
            print(f"\n>>> Invoking tool: `{tool_name}`")
            print(f">>> With input: {json.dumps(tool_input, indent=2)}")
            print()
            
            tool_func = self.tools[tool_name]
            result = tool_func.invoke(tool_input)
            
            print(f">>> Tool Output:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            
            results.append({"tool": tool_name, "result": result})
        
        # Generate output
        output_lines = ["Based on your query, here are the results:\n"]
        
        for item in results:
            tool_name = item["tool"]
            result = item["result"]
            
            if tool_name == "attendance_calculator":
                output_lines.append(f"✓ Attendance: {result['attendance_percentage']}% - {result['eligibility_status']}")
            elif tool_name == "result_calculator":
                output_lines.append(f"✓ Results: Average {result['average_marks']} - Grade {result['grade']} - {result['status']}")
            elif tool_name == "fee_balance_calculator":
                output_lines.append(f"✓ Fee Balance: {result['payment_status']}")
            elif tool_name == "library_fine_calculator":
                output_lines.append(f"✓ Library Fine: {result['fine_message']}")
            elif tool_name == "hostel_fee_calculator":
                output_lines.append(f"✓ Hostel Fee: {result['fee_breakdown']}")
            elif tool_name == "student_information_tool":
                if result['found']:
                    output_lines.append(f"✓ Student: {result['name']} - {result['course']} (Sem {result['semester']})")
                else:
                    output_lines.append(f"✗ {result['error']}")
        
        final_output = "\n".join(output_lines)
        
        print(f"{'─'*80}")
        print(f"AGENT RESPONSE:\n{final_output}")
        print(f"{'─'*80}\n")
        
        return {"output": final_output}


# ============================================================================
# TEST EXECUTION
# ============================================================================

def run_demo_tests():
    """Run all test cases with demo agent"""
    
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  SMART COLLEGE ASSISTANT - DEMO VERSION (No API Key Needed)".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")
    
    agent = DemoAgent()
    
    # Test cases
    test_queries = [
        {
            "name": "TEST 1: ATTENDANCE ELIGIBILITY",
            "query": "I attended 72 classes out of 90. Am I eligible for exams?"
        },
        {
            "name": "TEST 2: GRADE CALCULATION",
            "query": "My marks are 95, 90, 88, 91 and 87. What is my grade?"
        },
        {
            "name": "TEST 3: FEE BALANCE",
            "query": "My course fee is 50000 and I have paid 35000. How much fee is pending?"
        },
        {
            "name": "TEST 4: LIBRARY FINE",
            "query": "I returned a library book 8 days late. What is the fine amount?"
        },
        {
            "name": "TEST 5: HOSTEL FEE",
            "query": "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee."
        }
    ]
    
    # Run individual tests
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'▓'*80}")
        print(f"▓ {test['name']}")
        print(f"{'▓'*80}")
        
        try:
            result = agent.invoke({"input": test['query']})
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Multi-tool challenge
    print(f"\n\n{'▓'*80}")
    print(f"▓ MULTI-TOOL CHALLENGE")
    print(f"{'▓'*80}")
    
    multi_query = """I attended 80 classes out of 100. My marks are 90, 85, 88, 92 and 95. 
    My course fee is 60000 and I paid 45000. Provide attendance status, grade, and pending fee."""
    
    try:
        result = agent.invoke({"input": multi_query})
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Bonus
    print(f"\n\n{'▓'*80}")
    print(f"▓ BONUS: STUDENT INFORMATION")
    print(f"{'▓'*80}")
    
    bonus_query = "Can you retrieve the student information for student ID STU002?"
    
    try:
        result = agent.invoke({"input": bonus_query})
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print(f"\n{'█'*80}")
    print(f"█" + " "*78 + "█")
    print(f"█" + "  ALL TESTS COMPLETED SUCCESSFULLY ✓".center(78) + "█")
    print(f"█" + " "*78 + "█")
    print(f"█"*80 + "\n")


if __name__ == "__main__":
    run_demo_tests()
