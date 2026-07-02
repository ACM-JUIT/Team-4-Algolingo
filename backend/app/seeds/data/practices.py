from __future__ import annotations

from typing import Any, NotRequired, TypedDict

from app.models.enums import ChallengeType, PracticeStatus


class PracticeSeedData(TypedDict):
    key: str
    planet_key: str
    title: str
    challenge_type: ChallengeType
    difficulty: int
    description: str | None
    learning_outcome: str | None
    starter_code: NotRequired[str | None]
    expected_solution: NotRequired[str | None]
    xp_reward: int
    solution_code: str | None
    sample_input: NotRequired[str | None]
    sample_output: NotRequired[str | None]
    hints: list[str]
    test_cases: list[dict[str, Any]]
    order_number: int
    status: PracticeStatus


PRACTICES: tuple[PracticeSeedData, ...] = (
    {
        "key": "python_variables_p1",
        "planet_key": "python_variables",
        "title": "Launch Label",
        "challenge_type": ChallengeType.WRITE_OUTPUT,
        "description": (
            "Create a variable named `mission_name` with the value `\"AlgoLingo\"` and print it exactly once."
        ),
        "difficulty": 1,
        "learning_outcome": "Create a string variable and print its stored value.",
        "solution_code": 'mission_name = "AlgoLingo"\nprint(mission_name)',
        "test_cases": [
            {
                "name": "prints_mission_name",
                "input": "",
                "expected_output": "AlgoLingo",
            }
        ],
        "hints": [
            "Store the text `AlgoLingo` in a variable called `mission_name`.",
            "Text values need quotes around them.",
            "Use `print(mission_name)` after creating the variable.",
        ],
        "xp_reward": 50,
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_variables_p2",
        "planet_key": "python_variables",
        "title": "Astronaut Introduction",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read a name from input, store it in a variable called `astronaut_name`, "
            "and print `Welcome, <name>!`."
        ),
        "difficulty": 1,
        "learning_outcome": "Store user input in a variable and use it in output.",
        "solution_code": "astronaut_name = input().strip()\nprint(f\"Welcome, {astronaut_name}!\")",
        "test_cases": [
            {
                "name": "simple_name",
                "input": "Ava",
                "expected_output": "Welcome, Ava!",
            },
            {
                "name": "another_name",
                "input": "Ravi",
                "expected_output": "Welcome, Ravi!",
            },
        ],
        "hints": [
            "Use `input()` to read the user's name.",
            "Store the result in `astronaut_name`.",
            "An f-string is a clean way to build the output message.",
        ],
        "xp_reward": 60,
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_variables_p3",
        "planet_key": "python_variables",
        "title": "Fuel Calculator",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read two whole numbers: the fuel in the main tank and the fuel in the reserve tank. "
            "Store them in variables, add them, and print the total."
        ),
        "difficulty": 2,
        "learning_outcome": "Convert input to integers, store numeric values, and use variables in arithmetic.",
        "solution_code": (
            "main_tank = int(input())\n"
            "reserve_tank = int(input())\n"
            "total_fuel = main_tank + reserve_tank\n"
            "print(total_fuel)"
        ),
        "test_cases": [
            {
                "name": "basic_values",
                "input": "30\n12",
                "expected_output": "42",
            },
            {
                "name": "small_values",
                "input": "7\n8",
                "expected_output": "15",
            },
        ],
        "hints": [
            "Use `int(input())` because the values are numbers.",
            "Store the sum in a third variable like `total_fuel`.",
            "Print only the final total.",
        ],
        "xp_reward": 80,
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_variables_p4",
        "planet_key": "python_variables",
        "title": "Temperature Check",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "A spacecraft sensor gives the temperature in Celsius. "
            "Read one number, store it in a variable, convert it to Fahrenheit using "
            "`fahrenheit = celsius * 9 / 5 + 32`, and print the result."
        ),
        "difficulty": 2,
        "learning_outcome": "Use variables in a formula and understand that variable values may be numeric floats.",
        "solution_code": (
            "celsius = float(input())\n"
            "fahrenheit = celsius * 9 / 5 + 32\n"
            "print(fahrenheit)"
        ),
        "test_cases": [
            {
                "name": "freezing_point",
                "input": "0",
                "expected_output": "32.0",
            },
            {
                "name": "warm_day",
                "input": "10",
                "expected_output": "50.0",
            },
        ],
        "hints": [
            "Use `float(input())` so decimal temperatures also work.",
            "Store the converted result in a variable named `fahrenheit`.",
            "Follow the formula carefully: multiply first, then divide, then add 32.",
        ],
        "xp_reward": 100,
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_variables_p5",
        "planet_key": "python_variables",
        "title": "Mission Budget Summary",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read three whole numbers representing `fuel_cost`, `food_cost`, and `tool_cost`. "
            "Store each one in a descriptive variable. Then print two lines:\n"
            "`Total: <total_cost>`\n"
            "`Remaining: <remaining_budget>`\n"
            "Assume the mission budget is 500."
        ),
        "difficulty": 3,
        "learning_outcome": "Use multiple descriptive variables, combine arithmetic steps, and print formatted results.",
        "solution_code": (
            "fuel_cost = int(input())\n"
            "food_cost = int(input())\n"
            "tool_cost = int(input())\n"
            "MISSION_BUDGET = 500\n"
            "total_cost = fuel_cost + food_cost + tool_cost\n"
            "remaining_budget = MISSION_BUDGET - total_cost\n"
            'print(f"Total: {total_cost}")\n'
            'print(f"Remaining: {remaining_budget}")'
        ),
        "test_cases": [
            {
                "name": "balanced_budget",
                "input": "120\n80\n50",
                "expected_output": "Total: 250\nRemaining: 250",
            },
            {
                "name": "high_budget_use",
                "input": "200\n150\n75",
                "expected_output": "Total: 425\nRemaining: 75",
            },
        ],
        "hints": [
            "Add all three costs to make `total_cost`.",
            "Use another variable for the fixed mission budget.",
            "Print the answers exactly as `Total: ...` and `Remaining: ...`.",
        ],
        "xp_reward": 120,
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_data_types_p1",
        "planet_key": "python_data_types",
        "title": "Type Badge Printer",
        "challenge_type": ChallengeType.WRITE_OUTPUT,
        "description": (
            "Create four variables named `whole_number`, `decimal_number`, `greeting`, and `is_ready`. "
            "Store an integer, float, string, and boolean in them. Print the type name of each value "
            "using `type(...).__name__`, one per line."
        ),
        "difficulty": 1,
        "learning_outcome": "Create basic typed values and inspect them with type().",
        "xp_reward": 6,
        "solution_code": (
            'whole_number = 7\n'
            'decimal_number = 3.5\n'
            'greeting = "hello"\n'
            'is_ready = True\n'
            'print(type(whole_number).__name__)\n'
            'print(type(decimal_number).__name__)\n'
            'print(type(greeting).__name__)\n'
            'print(type(is_ready).__name__)'
        ),
        "hints": [
            "Use one integer, one float, one string, and one boolean value.",
            "Use `type(variable).__name__` for readable output.",
            "Print each type on a separate line.",
        ],
        "test_cases": [
            {
                "name": "basic_type_names",
                "input": "",
                "expected_output": "int\nfloat\nstr\nbool",
            }
        ],
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_data_types_p2",
        "planet_key": "python_data_types",
        "title": "Collection Roll Call",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Create a list, a tuple, a set, and a dictionary. Print the type name of each one "
            "on separate lines."
        ),
        "difficulty": 1,
        "learning_outcome": "Recognize common Python collection types by creating and inspecting them.",
        "xp_reward": 7,
        "solution_code": (
            'items = [1, 2, 3]\n'
            'coordinates = (4, 5)\n'
            'unique_numbers = {1, 2, 3}\n'
            'profile = {"name": "Ava"}\n'
            'print(type(items).__name__)\n'
            'print(type(coordinates).__name__)\n'
            'print(type(unique_numbers).__name__)\n'
            'print(type(profile).__name__)'
        ),
        "hints": [
            "A list uses `[]`.",
            "A tuple uses `()`.",
            "A set uses `{}` with unique values.",
            "A dictionary uses `{key: value}` pairs.",
        ],
        "test_cases": [
            {
                "name": "collection_type_names",
                "input": "",
                "expected_output": "list\ntuple\nset\ndict",
            }
        ],
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_data_types_p3",
        "planet_key": "python_data_types",
        "title": "Convert and Add",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read two values from input. Each value will arrive as text. Convert both to integers, "
            "add them, and print the result."
        ),
        "difficulty": 2,
        "learning_outcome": "Convert string input into integers before performing arithmetic.",
        "xp_reward": 8,
        "solution_code": (
            "first_value = input().strip()\n"
            "second_value = input().strip()\n"
            "first_number = int(first_value)\n"
            "second_number = int(second_value)\n"
            "print(first_number + second_number)"
        ),
        "hints": [
            "`input()` gives strings, not integers.",
            "Use `int(...)` on both inputs.",
            "Print only the final sum.",
        ],
        "test_cases": [
            {
                "name": "sum_one",
                "input": "12\n8",
                "expected_output": "20",
            },
            {
                "name": "sum_two",
                "input": "7\n15",
                "expected_output": "22",
            },
        ],
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_data_types_p4",
        "planet_key": "python_data_types",
        "title": "Student Profile Card",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read a student's name and age. Convert the age to an integer and store both values inside "
            "a dictionary with keys `name` and `age`. Then print two lines: the dictionary type name, "
            "and the stored age."
        ),
        "difficulty": 2,
        "learning_outcome": "Combine dictionaries and type conversion in one small program.",
        "xp_reward": 9,
        "solution_code": (
            "student_name = input().strip()\n"
            "age_text = input().strip()\n"
            "profile = {\"name\": student_name, \"age\": int(age_text)}\n"
            "print(type(profile).__name__)\n"
            "print(profile[\"age\"])"
        ),
        "hints": [
            "Convert the age before storing it in the dictionary.",
            "Use `type(profile).__name__` for the first line.",
            "Access the age using the key `\"age\"`.",
        ],
        "test_cases": [
            {
                "name": "profile_one",
                "input": "Lina\n19",
                "expected_output": "dict\n19",
            },
            {
                "name": "profile_two",
                "input": "Ravi\n21",
                "expected_output": "dict\n21",
            },
        ],
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_data_types_p5",
        "planet_key": "python_data_types",
        "title": "Travel Time Report",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read a distance and a speed as text values. Convert both to floats. Compute "
            "`time_needed = distance / speed`. Then print three lines exactly:\n"
            "`distance:<type>`\n"
            "`speed:<type>`\n"
            "`time:<result>`"
        ),
        "difficulty": 2,
        "learning_outcome": "Use type conversion, arithmetic, and type inspection together in one program.",
        "xp_reward": 10,
        "solution_code": (
            "distance_text = input().strip()\n"
            "speed_text = input().strip()\n"
            "distance = float(distance_text)\n"
            "speed = float(speed_text)\n"
            "time_needed = distance / speed\n"
            'print(f"distance:{type(distance).__name__}")\n'
            'print(f"speed:{type(speed).__name__}")\n'
            'print(f"time:{time_needed}")'
        ),
        "hints": [
            "Use `float(...)` for both text inputs.",
            "Store the converted values in variables named `distance` and `speed`.",
            "Print the type names using `type(variable).__name__`.",
        ],
        "test_cases": [
            {
                "name": "travel_case_one",
                "input": "12.5\n2.5",
                "expected_output": "distance:float\nspeed:float\ntime:5.0",
            },
            {
                "name": "travel_case_two",
                "input": "9.0\n3.0",
                "expected_output": "distance:float\nspeed:float\ntime:3.0",
            },
        ],
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_operators_p1",
        "planet_key": "python_operators",
        "title": "Arithmetic Warm-Up",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read two whole numbers. Print three lines in this order: their sum, their difference "
            "(first minus second), and their product."
        ),
        "difficulty": 1,
        "learning_outcome": "Use arithmetic operators to perform basic calculations with variables.",
        "xp_reward": 8,
        "solution_code": (
            "first_number = int(input())\n"
            "second_number = int(input())\n"
            "print(first_number + second_number)\n"
            "print(first_number - second_number)\n"
            "print(first_number * second_number)"
        ),
        "hints": [
            "Use `int(input())` for both numbers.",
            "You need `+`, `-`, and `*`.",
            "Print each answer on its own line in the required order.",
        ],
        "test_cases": [
            {
                "name": "positive_numbers",
                "input": "8\n3",
                "expected_output": "11\n5\n24",
            },
            {
                "name": "another_case",
                "input": "10\n4",
                "expected_output": "14\n6\n40",
            },
        ],
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_operators_p2",
        "planet_key": "python_operators",
        "title": "Score Booster",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read a starting score and a bonus score. Store the starting score in a variable, "
            "update it using `+=`, and print the final score."
        ),
        "difficulty": 1,
        "learning_outcome": "Use an assignment operator to update a variable cleanly.",
        "xp_reward": 9,
        "solution_code": (
            "score = int(input())\n"
            "bonus = int(input())\n"
            "score += bonus\n"
            "print(score)"
        ),
        "hints": [
            "Read the starting score first.",
            "Use `score += bonus` instead of writing a longer update expression.",
            "Print the updated score only once.",
        ],
        "test_cases": [
            {
                "name": "small_bonus",
                "input": "50\n10",
                "expected_output": "60",
            },
            {
                "name": "larger_bonus",
                "input": "72\n8",
                "expected_output": "80",
            },
        ],
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_operators_p3",
        "planet_key": "python_operators",
        "title": "Comparison Judge",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read two whole numbers. Print three lines in this order: whether the first number is greater "
            "than the second, whether the two numbers are equal, and whether the first number is less than "
            "or equal to the second."
        ),
        "difficulty": 2,
        "learning_outcome": "Use comparison operators to create boolean results from numeric input.",
        "xp_reward": 10,
        "solution_code": (
            "first_number = int(input())\n"
            "second_number = int(input())\n"
            "print(first_number > second_number)\n"
            "print(first_number == second_number)\n"
            "print(first_number <= second_number)"
        ),
        "hints": [
            "Use `>`, `==`, and `<=` in that exact order.",
            "Each printed result should be `True` or `False`.",
            "Compare the two variables directly.",
        ],
        "test_cases": [
            {
                "name": "greater_case",
                "input": "9\n4",
                "expected_output": "True\nFalse\nFalse",
            },
            {
                "name": "equal_case",
                "input": "6\n6",
                "expected_output": "False\nTrue\nTrue",
            },
        ],
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_operators_p4",
        "planet_key": "python_operators",
        "title": "Club Membership Check",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "A club accepts only three topic names: `python`, `math`, and `science`. "
            "Read one topic name from input, store the allowed topics in a collection, and print whether "
            "the given topic is in the collection."
        ),
        "difficulty": 2,
        "learning_outcome": "Use the `in` operator to test membership in a collection.",
        "xp_reward": 11,
        "solution_code": (
            "topic = input().strip().lower()\n"
            "allowed_topics = {\"python\", \"math\", \"science\"}\n"
            "print(topic in allowed_topics)"
        ),
        "hints": [
            "Use a set or list for the allowed topics.",
            "Convert input to lowercase so the comparison is more reliable.",
            "Use the `in` operator directly in `print()`.",
        ],
        "test_cases": [
            {
                "name": "member_topic",
                "input": "python",
                "expected_output": "True",
            },
            {
                "name": "non_member_topic",
                "input": "history",
                "expected_output": "False",
            },
        ],
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_operators_p5",
        "planet_key": "python_operators",
        "title": "Launch Decision",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "A rocket can launch if its fuel is at least 50 and at least one system is ready. "
            "Read three inputs: fuel as an integer, `engine_ready` as text (`yes` or `no`), "
            "and `backup_ready` as text (`yes` or `no`). Print whether launch is allowed."
        ),
        "difficulty": 2,
        "learning_outcome": (
            "Combine comparison and logical operators in a realistic multi-condition expression."
        ),
        "xp_reward": 12,
        "solution_code": (
            "fuel = int(input())\n"
            "engine_ready = input().strip().lower()\n"
            "backup_ready = input().strip().lower()\n"
            "can_launch = fuel >= 50 and (engine_ready == \"yes\" or backup_ready == \"yes\")\n"
            "print(can_launch)"
        ),
        "hints": [
            "First compare the fuel using `>=`.",
            "Then combine the readiness checks using `or`.",
            "Use parentheses to make the logical grouping clear.",
        ],
        "test_cases": [
            {
                "name": "launch_allowed_engine",
                "input": "60\nyes\nno",
                "expected_output": "True",
            },
            {
                "name": "launch_allowed_backup",
                "input": "55\nno\nyes",
                "expected_output": "True",
            },
            {
                "name": "not_enough_fuel",
                "input": "40\nyes\nyes",
                "expected_output": "False",
            },
        ],
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_conditionals_p1",
        "planet_key": "python_conditionals",
        "title": "Positive, Negative, or Zero",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read one whole number. Print `Positive` if it is greater than zero, `Negative` if it is less than zero, "
            "and `Zero` if it is exactly zero."
        ),
        "difficulty": 1,
        "learning_outcome": "Use if-elif-else to classify numeric input.",
        "xp_reward": 10,
        "solution_code": (
            "number = int(input())\n"
            "if number > 0:\n"
            "    print(\"Positive\")\n"
            "elif number < 0:\n"
            "    print(\"Negative\")\n"
            "else:\n"
            "    print(\"Zero\")"
        ),
        "hints": [
            "You need three possible outcomes.",
            "Check `> 0` first, then `< 0`, and use `else` for the remaining case.",
            "Print exactly one word as output.",
        ],
        "test_cases": [
            {"name": "positive_case", "input": "7", "expected_output": "Positive"},
            {"name": "negative_case", "input": "-2", "expected_output": "Negative"},
            {"name": "zero_case", "input": "0", "expected_output": "Zero"},
        ],
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_conditionals_p2",
        "planet_key": "python_conditionals",
        "title": "Voting Eligibility",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read a person's age. Print `Eligible to vote` if the age is 18 or above. "
            "Otherwise, print `Not eligible to vote`."
        ),
        "difficulty": 1,
        "learning_outcome": "Use a simple if-else decision with a comparison operator.",
        "xp_reward": 12,
        "solution_code": (
            "age = int(input())\n"
            "if age >= 18:\n"
            "    print(\"Eligible to vote\")\n"
            "else:\n"
            "    print(\"Not eligible to vote\")"
        ),
        "hints": [
            "Compare the age to 18.",
            "Use `>=` for '18 or above'.",
            "This challenge needs only two branches.",
        ],
        "test_cases": [
            {"name": "eligible_case", "input": "18", "expected_output": "Eligible to vote"},
            {"name": "not_eligible_case", "input": "16", "expected_output": "Not eligible to vote"},
        ],
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_conditionals_p3",
        "planet_key": "python_conditionals",
        "title": "Largest of Three",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read three whole numbers. Print the largest value. You may assume there is always one value "
            "that is greater than or equal to the others."
        ),
        "difficulty": 2,
        "learning_outcome": "Use multiple comparisons and branching to find the largest value.",
        "xp_reward": 14,
        "solution_code": (
            "a = int(input())\n"
            "b = int(input())\n"
            "c = int(input())\n"
            "if a >= b and a >= c:\n"
            "    print(a)\n"
            "elif b >= a and b >= c:\n"
            "    print(b)\n"
            "else:\n"
            "    print(c)"
        ),
        "hints": [
            "Compare one value against both of the others.",
            "Logical `and` is useful here.",
            "Use `elif` for the second main case.",
        ],
        "test_cases": [
            {"name": "largest_first", "input": "9\n4\n2", "expected_output": "9"},
            {"name": "largest_third", "input": "3\n7\n12", "expected_output": "12"},
        ],
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_conditionals_p4",
        "planet_key": "python_conditionals",
        "title": "Grade Calculator",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read a score from 0 to 100. Print the grade using this scale:\n"
            "A for 90 and above\n"
            "B for 75 to 89\n"
            "C for 50 to 74\n"
            "D for below 50"
        ),
        "difficulty": 2,
        "learning_outcome": "Use ordered elif conditions to classify a score into grade categories.",
        "xp_reward": 16,
        "solution_code": (
            "score = int(input())\n"
            "if score >= 90:\n"
            "    print(\"A\")\n"
            "elif score >= 75:\n"
            "    print(\"B\")\n"
            "elif score >= 50:\n"
            "    print(\"C\")\n"
            "else:\n"
            "    print(\"D\")"
        ),
        "hints": [
            "Check the highest range first.",
            "Once a higher range fails, Python can continue to the next one.",
            "Use `elif` to avoid repeated separate `if` statements.",
        ],
        "test_cases": [
            {"name": "grade_a", "input": "93", "expected_output": "A"},
            {"name": "grade_b", "input": "80", "expected_output": "B"},
            {"name": "grade_c", "input": "50", "expected_output": "C"},
            {"name": "grade_d", "input": "42", "expected_output": "D"},
        ],
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_conditionals_p5",
        "planet_key": "python_conditionals",
        "title": "ATM Approval Check",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Build a simple ATM decision system. Read three inputs in this order:\n"
            "1. account balance as an integer\n"
            "2. withdrawal amount as an integer\n"
            "3. PIN status as text (`correct` or `wrong`)\n\n"
            "Rules:\n"
            "- If the PIN is wrong, print `Invalid PIN`\n"
            "- Otherwise, if the withdrawal amount is greater than the balance, print `Insufficient funds`\n"
            "- Otherwise, print `Transaction approved`"
        ),
        "difficulty": 3,
        "learning_outcome": "Use nested or ordered conditionals to model realistic decision logic.",
        "xp_reward": 18,
        "solution_code": (
            "balance = int(input())\n"
            "withdraw_amount = int(input())\n"
            "pin_status = input().strip().lower()\n"
            "if pin_status != \"correct\":\n"
            "    print(\"Invalid PIN\")\n"
            "elif withdraw_amount > balance:\n"
            "    print(\"Insufficient funds\")\n"
            "else:\n"
            "    print(\"Transaction approved\")"
        ),
        "hints": [
            "The PIN check should happen first.",
            "Only check the balance if the PIN is correct.",
            "Use `!=` to test for a wrong PIN.",
        ],
        "test_cases": [
            {"name": "invalid_pin", "input": "500\n100\nwrong", "expected_output": "Invalid PIN"},
            {"name": "insufficient_funds", "input": "200\n250\ncorrect", "expected_output": "Insufficient funds"},
            {"name": "approved", "input": "500\n120\ncorrect", "expected_output": "Transaction approved"},
        ],
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_loops_p1",
        "planet_key": "python_loops",
        "title": "Count to N",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read one whole number `n`. Print all numbers from 1 to `n`, each on its own line."
        ),
        "difficulty": 1,
        "learning_outcome": "Use a for loop with range() to print a simple sequence.",
        "xp_reward": 10,
        "solution_code": (
            "n = int(input())\n"
            "for number in range(1, n + 1):\n"
            "    print(number)"
        ),
        "hints": [
            "Use `range(1, n + 1)` so the loop includes `n`.",
            "Print the loop variable inside the loop body.",
            "Each number should appear on its own line.",
        ],
        "test_cases": [
            {"name": "count_to_5", "input": "5", "expected_output": "1\n2\n3\n4\n5"},
            {"name": "count_to_3", "input": "3", "expected_output": "1\n2\n3"},
        ],
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_loops_p2",
        "planet_key": "python_loops",
        "title": "Sum of First N Numbers",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Read one whole number `n`. Use a loop to calculate the sum of numbers from 1 to `n`, then print the result."
        ),
        "difficulty": 1,
        "learning_outcome": "Use a loop and an accumulator variable to compute a running total.",
        "xp_reward": 12,
        "solution_code": (
            "n = int(input())\n"
            "total = 0\n"
            "for number in range(1, n + 1):\n"
            "    total += number\n"
            "print(total)"
        ),
        "hints": [
            "Start with `total = 0`.",
            "Add each number to `total` inside the loop.",
            "Print the total after the loop finishes.",
        ],
        "test_cases": [
            {"name": "sum_to_5", "input": "5", "expected_output": "15"},
            {"name": "sum_to_4", "input": "4", "expected_output": "10"},
        ],
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_loops_p3",
        "planet_key": "python_loops",
        "title": "Multiplication Table",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read one whole number `n`. Print the multiplication table for that number from 1 to 10 in the format `n x i = result`."
        ),
        "difficulty": 2,
        "learning_outcome": "Use a loop to generate repeated formatted arithmetic output.",
        "xp_reward": 14,
        "solution_code": (
            "n = int(input())\n"
            "for i in range(1, 11):\n"
            "    print(f\"{n} x {i} = {n * i}\")"
        ),
        "hints": [
            "Use `range(1, 11)` to include 10.",
            "Multiply `n` by the loop variable.",
            "Use an f-string to match the required format exactly.",
        ],
        "test_cases": [
            {
                "name": "table_of_3",
                "input": "3",
                "expected_output": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n3 x 6 = 18\n3 x 7 = 21\n3 x 8 = 24\n3 x 9 = 27\n3 x 10 = 30",
            },
            {
                "name": "table_of_2",
                "input": "2",
                "expected_output": "2 x 1 = 2\n2 x 2 = 4\n2 x 3 = 6\n2 x 4 = 8\n2 x 5 = 10\n2 x 6 = 12\n2 x 7 = 14\n2 x 8 = 16\n2 x 9 = 18\n2 x 10 = 20",
            },
        ],
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_loops_p4",
        "planet_key": "python_loops",
        "title": "Star Triangle",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Read one whole number `n`. Print a right-angled triangle pattern using `*` characters. "
            "For example, if `n = 3`, print:\n*\n**\n***"
        ),
        "difficulty": 2,
        "learning_outcome": "Use nested loops to generate simple text patterns.",
        "xp_reward": 16,
        "solution_code": (
            "n = int(input())\n"
            "for row in range(1, n + 1):\n"
            "    print(\"*\" * row)"
        ),
        "hints": [
            "Think of each line as one row.",
            "A row number tells you how many stars to print.",
            "You can solve this with a loop and string repetition.",
        ],
        "test_cases": [
            {"name": "triangle_3", "input": "3", "expected_output": "*\n**\n***"},
            {"name": "triangle_4", "input": "4", "expected_output": "*\n**\n***\n****"},
        ],
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_loops_p5",
        "planet_key": "python_loops",
        "title": "Number Guessing Loop",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Create a simple number guessing game. The secret number is 7. Keep reading guesses until the user enters 7. "
            "For each wrong guess, print:\n- `Too low` if the guess is smaller than 7\n- `Too high` if the guess is greater than 7\nWhen the guess is correct, print `Correct` and stop."
        ),
        "difficulty": 3,
        "learning_outcome": "Use a while loop with break-style thinking to repeat until a target condition is reached.",
        "xp_reward": 18,
        "solution_code": (
            "secret_number = 7\n"
            "while True:\n"
            "    guess = int(input())\n"
            "    if guess < secret_number:\n"
            "        print(\"Too low\")\n"
            "    elif guess > secret_number:\n"
            "        print(\"Too high\")\n"
            "    else:\n"
            "        print(\"Correct\")\n"
            "        break"
        ),
        "hints": [
            "Use `while True` and stop with `break` when the guess is correct.",
            "Compare the guess with the secret number using `<` and `>`.",
            "Only print `Correct` when the guess matches exactly.",
        ],
        "test_cases": [
            {"name": "low_then_correct", "input": "3\n7", "expected_output": "Too low\nCorrect"},
            {"name": "high_then_low_then_correct", "input": "9\n5\n7", "expected_output": "Too high\nToo low\nCorrect"},
        ],
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_functions_p1",
        "planet_key": "python_functions",
        "title": "Greeting Function",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Write a function named `greet_user` that accepts one parameter called `name` and prints `Hello, <name>!`. "
            "Then call the function using the input value."
        ),
        "difficulty": 1,
        "learning_outcome": "Define a simple function, pass one argument, and call it correctly.",
        "xp_reward": 14,
        "solution_code": (
            "def greet_user(name):\n"
            "    print(f\"Hello, {name}!\")\n\n"
            "user_name = input().strip()\n"
            "greet_user(user_name)"
        ),
        "hints": [
            "Use `def greet_user(name):` to define the function.",
            "Use an f-string to print the message.",
            "Read the name first, then pass it into the function call.",
        ],
        "test_cases": [
            {"name": "greet_ava", "input": "Ava", "expected_output": "Hello, Ava!"},
            {"name": "greet_ravi", "input": "Ravi", "expected_output": "Hello, Ravi!"},
        ],
        "order_number": 1,
        "status": PracticeStatus.AVAILABLE,
    },
    {
        "key": "python_functions_p2",
        "planet_key": "python_functions",
        "title": "Rectangle Area",
        "challenge_type": ChallengeType.CODE_WRITING,
        "description": (
            "Write a function named `rectangle_area` that accepts `width` and `height`, returns the area, "
            "and print the returned result after reading the two inputs."
        ),
        "difficulty": 1,
        "learning_outcome": "Write a function with parameters and a return value.",
        "xp_reward": 16,
        "solution_code": (
            "def rectangle_area(width, height):\n"
            "    return width * height\n\n"
            "width = int(input())\n"
            "height = int(input())\n"
            "print(rectangle_area(width, height))"
        ),
        "hints": [
            "The area of a rectangle is width multiplied by height.",
            "Use `return`, not `print`, inside the function.",
            "Print the returned value outside the function.",
        ],
        "test_cases": [
            {"name": "small_rectangle", "input": "4\n5", "expected_output": "20"},
            {"name": "larger_rectangle", "input": "7\n3", "expected_output": "21"},
        ],
        "order_number": 2,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_functions_p3",
        "planet_key": "python_functions",
        "title": "Maximum of Two",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Write a function named `maximum_of_two` that accepts two numbers and returns the larger one. "
            "Read two integers and print the returned result."
        ),
        "difficulty": 2,
        "learning_outcome": "Combine functions with conditionals and return values.",
        "xp_reward": 18,
        "solution_code": (
            "def maximum_of_two(first_number, second_number):\n"
            "    if first_number >= second_number:\n"
            "        return first_number\n"
            "    return second_number\n\n"
            "a = int(input())\n"
            "b = int(input())\n"
            "print(maximum_of_two(a, b))"
        ),
        "hints": [
            "Compare the two numbers inside the function.",
            "Return one value if the first is larger, otherwise return the second.",
            "Use `>=` so equal values still work correctly.",
        ],
        "test_cases": [
            {"name": "first_is_larger", "input": "9\n4", "expected_output": "9"},
            {"name": "second_is_larger", "input": "3\n12", "expected_output": "12"},
        ],
        "order_number": 3,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_functions_p4",
        "planet_key": "python_functions",
        "title": "Mini Calculator",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Build a small calculator using multiple functions: `add_numbers`, `subtract_numbers`, and `multiply_numbers`. "
            "Read two integers and print three lines in this order: sum, difference, product."
        ),
        "difficulty": 2,
        "learning_outcome": "Break a problem into multiple reusable functions.",
        "xp_reward": 20,
        "solution_code": (
            "def add_numbers(a, b):\n"
            "    return a + b\n\n"
            "def subtract_numbers(a, b):\n"
            "    return a - b\n\n"
            "def multiply_numbers(a, b):\n"
            "    return a * b\n\n"
            "first_number = int(input())\n"
            "second_number = int(input())\n"
            "print(add_numbers(first_number, second_number))\n"
            "print(subtract_numbers(first_number, second_number))\n"
            "print(multiply_numbers(first_number, second_number))"
        ),
        "hints": [
            "Create one function per operation.",
            "Each function should return a value.",
            "Call the functions after reading the inputs.",
        ],
        "test_cases": [
            {"name": "calculator_case_one", "input": "8\n3", "expected_output": "11\n5\n24"},
            {"name": "calculator_case_two", "input": "10\n4", "expected_output": "14\n6\n40"},
        ],
        "order_number": 4,
        "status": PracticeStatus.LOCKED,
    },
    {
        "key": "python_functions_p5",
        "planet_key": "python_functions",
        "title": "Student Report Card Generator",
        "challenge_type": ChallengeType.SCENARIO,
        "description": (
            "Build a reusable report card generator using functions. Write one function named `calculate_average` "
            "that returns the average of three scores, and another function named `get_result` that returns "
            "`Pass` if the average is at least 50, otherwise `Fail`. Read a student name and three scores. "
            "Print exactly three lines:\n"
            "`Name: <name>`\n"
            "`Average: <average>`\n"
            "`Result: <result>`"
        ),
        "difficulty": 3,
        "learning_outcome": "Design reusable functions that work together to solve a larger practical problem.",
        "xp_reward": 22,
        "solution_code": (
            "def calculate_average(score1, score2, score3):\n"
            "    return (score1 + score2 + score3) / 3\n\n"
            "def get_result(average):\n"
            "    if average >= 50:\n"
            "        return \"Pass\"\n"
            "    return \"Fail\"\n\n"
            "student_name = input().strip()\n"
            "score1 = int(input())\n"
            "score2 = int(input())\n"
            "score3 = int(input())\n"
            "average = calculate_average(score1, score2, score3)\n"
            "result = get_result(average)\n"
            "print(f\"Name: {student_name}\")\n"
            "print(f\"Average: {average}\")\n"
            "print(f\"Result: {result}\")"
        ),
        "hints": [
            "Split the problem into two functions, not one.",
            "The average should be returned first, then passed into the result function.",
            "Print the final report after all calculations are done.",
        ],
        "test_cases": [
            {"name": "passing_student", "input": "Ava\n60\n70\n80", "expected_output": "Name: Ava\nAverage: 70.0\nResult: Pass"},
            {"name": "failing_student", "input": "Ravi\n30\n40\n50", "expected_output": "Name: Ravi\nAverage: 40.0\nResult: Fail"},
        ],
        "order_number": 5,
        "status": PracticeStatus.LOCKED,
    },
)
