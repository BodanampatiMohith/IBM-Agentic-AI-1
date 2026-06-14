"""
Direct Tool Testing - Test individual tools without the agent
Useful for quick verification and debugging
"""

import json
from college_assistant import (
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_information_tool,
    STUDENT_DATABASE
)


def print_tool_output(tool_name, output):
    """Pretty print tool output"""
    print(f"\n{'='*60}")
    print(f"Tool: {tool_name}")
    print(f"{'-'*60}")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"{'='*60}")


def test_all_tools():
    """Test all tools directly without the agent"""
    
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█  DIRECT TOOL TESTING - Smart College Assistant  " + " " * 9 + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    # Test 1: Attendance Calculator
    print("\n\n📊 TEST 1: ATTENDANCE CALCULATOR")
    print("-" * 60)
    print("Scenario: Student attended 72 classes out of 90")
    result = attendance_calculator.invoke({"total_classes": 90, "attended_classes": 72})
    print_tool_output("attendance_calculator(90, 72)", result)
    
    # Test 2: Attendance - Eligible Case
    print("\n\n📊 TEST 2: ATTENDANCE CALCULATOR (Eligible Case)")
    print("-" * 60)
    print("Scenario: Student attended 80 classes out of 100")
    result = attendance_calculator.invoke({"total_classes": 100, "attended_classes": 80})
    print_tool_output("attendance_calculator(100, 80)", result)
    
    # Test 3: Result Calculator
    print("\n\n📈 TEST 3: RESULT CALCULATOR")
    print("-" * 60)
    print("Scenario: Marks are 95, 90, 88, 91, 87")
    result = result_calculator.invoke({
        "marks_subject1": 95,
        "marks_subject2": 90,
        "marks_subject3": 88,
        "marks_subject4": 91,
        "marks_subject5": 87
    })
    print_tool_output("result_calculator(95, 90, 88, 91, 87)", result)
    
    # Test 4: Result Calculator - Different Grade
    print("\n\n📈 TEST 4: RESULT CALCULATOR (Different Grade)")
    print("-" * 60)
    print("Scenario: Marks are 90, 85, 88, 92, 95")
    result = result_calculator.invoke({
        "marks_subject1": 90,
        "marks_subject2": 85,
        "marks_subject3": 88,
        "marks_subject4": 92,
        "marks_subject5": 95
    })
    print_tool_output("result_calculator(90, 85, 88, 92, 95)", result)
    
    # Test 5: Fee Balance Calculator
    print("\n\n💰 TEST 5: FEE BALANCE CALCULATOR")
    print("-" * 60)
    print("Scenario: Course fee is ₹50000, paid ₹35000")
    result = fee_balance_calculator.invoke({"total_course_fee": 50000, "amount_paid": 35000})
    print_tool_output("fee_balance_calculator(50000, 35000)", result)
    
    # Test 6: Fee Balance Calculator - Multi-tool Challenge
    print("\n\n💰 TEST 6: FEE BALANCE CALCULATOR (Multi-tool Case)")
    print("-" * 60)
    print("Scenario: Course fee is ₹60000, paid ₹45000")
    result = fee_balance_calculator.invoke({"total_course_fee": 60000, "amount_paid": 45000})
    print_tool_output("fee_balance_calculator(60000, 45000)", result)
    
    # Test 7: Library Fine Calculator
    print("\n\n📚 TEST 7: LIBRARY FINE CALCULATOR")
    print("-" * 60)
    print("Scenario: Book returned 8 days late")
    result = library_fine_calculator.invoke({"delayed_days": 8})
    print_tool_output("library_fine_calculator(8)", result)
    
    # Test 8: Library Fine Calculator - Different Days
    print("\n\n📚 TEST 8: LIBRARY FINE CALCULATOR (Different Days)")
    print("-" * 60)
    print("Scenario: Book returned 15 days late")
    result = library_fine_calculator.invoke({"delayed_days": 15})
    print_tool_output("library_fine_calculator(15)", result)
    
    # Test 9: Hostel Fee Calculator
    print("\n\n🏨 TEST 9: HOSTEL FEE CALCULATOR")
    print("-" * 60)
    print("Scenario: Monthly fee ₹6000 for 5 months")
    result = hostel_fee_calculator.invoke({"monthly_hostel_fee": 6000, "number_of_months": 5})
    print_tool_output("hostel_fee_calculator(6000, 5)", result)
    
    # Test 10: Hostel Fee Calculator - Different Duration
    print("\n\n🏨 TEST 10: HOSTEL FEE CALCULATOR (Different Duration)")
    print("-" * 60)
    print("Scenario: Monthly fee ₹5000 for 12 months")
    result = hostel_fee_calculator.invoke({"monthly_hostel_fee": 5000, "number_of_months": 12})
    print_tool_output("hostel_fee_calculator(5000, 12)", result)
    
    # Test 11: Student Information Tool
    print("\n\n👤 TEST 11: STUDENT INFORMATION TOOL (Found)")
    print("-" * 60)
    print("Scenario: Retrieve student info for STU002")
    result = student_information_tool.invoke({"student_id": "STU002"})
    print_tool_output("student_information_tool('STU002')", result)
    
    # Test 12: Student Information Tool - Not Found
    print("\n\n👤 TEST 12: STUDENT INFORMATION TOOL (Not Found)")
    print("-" * 60)
    print("Scenario: Retrieve student info for STU999")
    result = student_information_tool.invoke({"student_id": "STU999"})
    print_tool_output("student_information_tool('STU999')", result)
    
    # Summary of Available Students
    print("\n\n📋 AVAILABLE STUDENTS IN DATABASE")
    print("=" * 60)
    for student_id, info in STUDENT_DATABASE.items():
        print(f"\n{student_id}: {info['name']}")
        print(f"  Course: {info['course']}")
        print(f"  Semester: {info['semester']}")
    
    # Test Error Cases
    print("\n\n⚠️  TEST ERROR CASES")
    print("=" * 60)
    
    print("\n❌ Attendance: More attended than total")
    result = attendance_calculator.invoke({"total_classes": 50, "attended_classes": 60})
    print_tool_output("attendance_calculator(50, 60)", result)
    
    print("\n❌ Result: Marks out of range")
    result = result_calculator.invoke({
        "marks_subject1": 95, "marks_subject2": 150, "marks_subject3": 80,
        "marks_subject4": 85, "marks_subject5": 90
    })
    print_tool_output("result_calculator with invalid marks", result)
    
    print("\n❌ Fee: More paid than total")
    result = fee_balance_calculator.invoke({"total_course_fee": 30000, "amount_paid": 40000})
    print_tool_output("fee_balance_calculator(30000, 40000)", result)
    
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█  ALL TOOL TESTS COMPLETED SUCCESSFULLY          " + " " * 7 + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    test_all_tools()
