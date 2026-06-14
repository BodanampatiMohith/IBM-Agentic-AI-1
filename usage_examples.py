"""
Usage Examples - Different ways to use the Smart College Assistant
"""

from college_assistant import (
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_information_tool,
    create_college_assistant
)


# ============================================================================
# EXAMPLE 1: Using Tools Directly (No LLM Required)
# ============================================================================

def example_1_direct_tool_usage():
    """
    Use tools directly without the agent.
    Useful for: batch processing, debugging, programmatic access
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Direct Tool Usage (No Agent/LLM)")
    print("="*70)
    
    # Calculate attendance
    attendance = attendance_calculator(total_classes=100, attended_classes=85)
    print(f"\nAttendance: {attendance['attendance_percentage']}%")
    print(f"Status: {attendance['eligibility_status']}")
    
    # Calculate result
    result = result_calculator(95, 88, 92, 87, 90)
    print(f"\nAverage: {result['average_marks']}")
    print(f"Grade: {result['grade']}")
    
    # Calculate fees
    fees = fee_balance_calculator(50000, 30000)
    print(f"\nPending Fee: ₹{fees['pending_fee']}")


# ============================================================================
# EXAMPLE 2: Using Agent with Single Query
# ============================================================================

def example_2_single_query():
    """
    Simple query using the agent.
    The LLM automatically selects the correct tool(s).
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Single Query via Agent")
    print("="*70)
    
    agent = create_college_assistant()
    
    query = "I attended 95 classes out of 120. Am I eligible for exams?"
    print(f"\nQuery: {query}")
    print("-" * 70)
    
    result = agent.invoke({"input": query})
    print(f"\nResponse:\n{result['output']}")


# ============================================================================
# EXAMPLE 3: Using Agent with Multi-Tool Query
# ============================================================================

def example_3_multi_tool_query():
    """
    Complex query requiring multiple tools.
    Agent automatically chains tool calls.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Tool Query via Agent")
    print("="*70)
    
    agent = create_college_assistant()
    
    query = """
    Please provide me a complete academic summary:
    - I attended 88 classes out of 100
    - My marks are: 92, 88, 95, 89, 91
    - My course fee is 60000, and I've paid 40000
    """
    
    print(f"\nQuery: {query}")
    print("-" * 70)
    
    result = agent.invoke({"input": query})
    print(f"\nResponse:\n{result['output']}")


# ============================================================================
# EXAMPLE 4: Using Agent with Conditional Logic
# ============================================================================

def example_4_conditional_query():
    """
    Query that might or might not use certain tools.
    Agent decides based on understanding.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Conditional Tool Selection")
    print("="*70)
    
    agent = create_college_assistant()
    
    # Query that only needs one tool
    query1 = "What will be the fine for returning my library book 12 days late?"
    
    print(f"\nQuery 1: {query1}")
    print("-" * 70)
    result = agent.invoke({"input": query1})
    print(f"Response:\n{result['output']}")


# ============================================================================
# EXAMPLE 5: Batch Processing
# ============================================================================

def example_5_batch_processing():
    """
    Process multiple student records in batch.
    Use direct tool calls for efficiency.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Processing")
    print("="*70)
    
    # Sample student data
    students = [
        {
            "id": 1,
            "name": "Student A",
            "attended": 75,
            "total": 100,
            "marks": [80, 85, 82, 88, 84]
        },
        {
            "id": 2,
            "name": "Student B",
            "attended": 60,
            "total": 100,
            "marks": [70, 72, 68, 75, 71]
        },
        {
            "id": 3,
            "name": "Student C",
            "attended": 95,
            "total": 100,
            "marks": [95, 93, 96, 94, 97]
        }
    ]
    
    print("\nProcessing", len(students), "students...\n")
    
    for student in students:
        print(f"\nStudent {student['id']}: {student['name']}")
        print("-" * 50)
        
        # Calculate attendance
        att = attendance_calculator(
            total_classes=student['total'],
            attended_classes=student['attended']
        )
        
        # Calculate result
        res = result_calculator(*student['marks'])
        
        print(f"Attendance: {att['attendance_percentage']}% - {att['eligibility_status']}")
        print(f"Result: Grade {res['grade']}, Average {res['average_marks']} - {res['status']}")


# ============================================================================
# EXAMPLE 6: Error Handling
# ============================================================================

def example_6_error_handling():
    """
    Handle invalid inputs gracefully.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling")
    print("="*70)
    
    print("\n❌ Invalid attendance (attended > total):")
    result = attendance_calculator(100, 120)
    print(f"   Result: {result}")
    
    print("\n❌ Invalid marks (out of range):")
    result = result_calculator(95, 150, 80, 85, 90)
    print(f"   Result: {result}")
    
    print("\n❌ Invalid fee (paid > total):")
    result = fee_balance_calculator(30000, 40000)
    print(f"   Result: {result}")
    
    print("\n✓ Agent handles errors gracefully")


# ============================================================================
# EXAMPLE 7: Custom Queries
# ============================================================================

def example_7_custom_queries():
    """
    Examples of various query types the agent can handle.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Various Query Types")
    print("="*70)
    
    agent = create_college_assistant()
    
    queries = [
        "Calculate my attendance percentage: 45 classes attended out of 50",
        "I have 5 subjects with marks 78, 82, 85, 80, 88. What's my average and grade?",
        "Total hostel cost calculation: 4000 per month for 8 months",
        "Show me the record for student STU003",
        "Multiple needs: 88/100 attendance, marks 92 84 89 91 86, fee 45000 paid 35000"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n\nQuery {i}: {query}")
        print("-" * 70)
        try:
            result = agent.invoke({"input": query})
            print(f"Response:\n{result['output'][:200]}...")  # First 200 chars
        except Exception as e:
            print(f"Error: {str(e)[:100]}")


# ============================================================================
# EXAMPLE 8: Direct Student Information Lookup
# ============================================================================

def example_8_student_lookup():
    """
    Lookup student information directly (bonus feature).
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Student Information Lookup")
    print("="*70)
    
    # Valid lookup
    print("\n✓ Looking up STU002:")
    result = student_information_tool("STU002")
    for key, value in result.items():
        if key != "found":
            print(f"  {key}: {value}")
    
    # Invalid lookup
    print("\n❌ Looking up STU999:")
    result = student_information_tool("STU999")
    print(f"  {result['error']}")
    print(f"  Available IDs: {result['available_ids']}")


# ============================================================================
# EXAMPLE 9: Integration - Web Service Style
# ============================================================================

def example_9_api_style():
    """
    Use tools as if they were API endpoints.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: API-Style Tool Usage")
    print("="*70)
    
    # Request 1
    print("\nRequest 1: POST /api/attendance")
    print("Body: {'total_classes': 100, 'attended_classes': 92}")
    result = attendance_calculator(100, 92)
    print(f"Response: {result['eligibility_status']}")
    
    # Request 2
    print("\nRequest 2: POST /api/results")
    print("Body: {'marks': [88, 92, 85, 90, 87]}")
    result = result_calculator(88, 92, 85, 90, 87)
    print(f"Response: Grade {result['grade']}")


# ============================================================================
# EXAMPLE 10: Agent with Detailed Analysis
# ============================================================================

def example_10_detailed_analysis():
    """
    Get detailed analysis from agent.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Detailed Analysis Query")
    print("="*70)
    
    agent = create_college_assistant()
    
    query = """
    I need a comprehensive analysis. Here's my situation:
    - Attendance: 78 out of 100 classes
    - Marks (5 subjects): 85, 88, 80, 87, 82
    - Course fees: Total is 50000, I've paid 30000
    - Library book delay: 10 days
    
    Please analyze each aspect and tell me:
    1. Am I eligible for exams?
    2. What grade will I get?
    3. How much more fee should I pay?
    4. What's my library fine?
    """
    
    print(f"\nQuery:\n{query}")
    print("-" * 70)
    
    result = agent.invoke({"input": query})
    print(f"\nDetailed Response:\n{result['output']}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  USAGE EXAMPLES - Smart College Assistant".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    try:
        # Run all examples
        example_1_direct_tool_usage()
        example_2_single_query()
        example_3_multi_tool_query()
        example_4_conditional_query()
        example_5_batch_processing()
        example_6_error_handling()
        example_7_custom_queries()
        example_8_student_lookup()
        example_9_api_style()
        example_10_detailed_analysis()
        
        print("\n" + "█" * 70)
        print("█" + " " * 68 + "█")
        print("█" + "  ALL EXAMPLES COMPLETED SUCCESSFULLY".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure to:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Install requirements: pip install -r requirements.txt")
        print("3. Have internet connection for OpenAI API calls")
