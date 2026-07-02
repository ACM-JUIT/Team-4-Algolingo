from __future__ import annotations

from typing import NotRequired, TypedDict

from app.models.enums import DiscoveryStatus


class DiscoverySeedData(TypedDict):
    key: str
    planet_key: str
    title: str
    short_description: NotRequired[str | None]
    description: str | None
    markdown_content: NotRequired[str | None]
    content_md: str | None
    learning_objective: str | None
    estimated_read_time: NotRequired[int | None]
    read_time_minutes: int | None
    difficulty: int
    xp_reward: int
    order_number: int
    status: DiscoveryStatus
    prerequisites: list[str]


DISCOVERIES: tuple[DiscoverySeedData, ...] = (
    {
        "key": "python_variables_d1",
        "planet_key": "python_variables",
        "title": "What Is a Variable?",
        "description": "Understand variables as named pieces of data that a program can remember and use.",
        "learning_objective": (
            "Explain what a variable is and identify how variables help programs store useful information."
        ),
        "content_md": """
# What Is a Variable?

When people solve problems, they often **remember information** for later.

- A student remembers a score.
- A shopkeeper remembers a price.
- A game remembers a player's name.

A program needs that same ability.

A **variable** is a name that points to a value so your program can use that value later.

## A Simple Example

```python
student_name = \"Ava\"
score = 92
```

Here:

- `student_name` is a variable
- `\"Ava\"` is the value stored in it
- `score` is another variable
- `92` is its value

## Why Variables Matter

Without variables, programs would be full of repeated values and hard to update.

Imagine writing this:

```python
print(\"Welcome, Ava!\")
print(\"Ava has started the quiz.\")
print(\"Ava scored 92.\")
```

That works, but what if the student changes?

With variables, you only update one place:

```python
student_name = \"Ava\"
score = 92

print(\"Welcome,\", student_name)
print(student_name, \"has started the quiz.\")
print(student_name, \"scored\", score)
```

That is more flexible and easier to maintain.

## Think of Variables Like Labels

A useful beginner image is:

- the **label** is the variable name
- the **value** is the information attached to that label

Example:

```python
planet = \"Mars\"
fuel_level = 85
```

The program can now use `planet` and `fuel_level` whenever it needs them.

## Variables Can Store Different Kinds of Data

A variable can hold:

- text like `\"Python\"`
- whole numbers like `10`
- decimal numbers like `3.5`
- true/false values like `True`

```python
language = \"Python\"
level = 1
accuracy = 99.5
is_ready = True
```

## Common Mistakes

### Mistake 1: Thinking the variable *is* the value

A variable is **not** the value itself.  
It is the **name used to access** the value.

### Mistake 2: Using values without names everywhere

This makes programs harder to read.

```python
print(\"Mia\")
print(18)
```

Compare that with:

```python
name = \"Mia\"
age = 18

print(name)
print(age)
```

The second version is clearer.

## Tip

Choose variable names that explain the meaning of the data:

- `name` ✅
- `score` ✅
- `x` 😐 for a beginner program
- `thing` ❌ too vague

## Mini Summary

- A **variable** is a name that stores or refers to a value.
- Variables help programs remember information.
- Good variable names make code easier to understand.
- Variables are one of the building blocks of programming.
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 60,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_variables_d2",
        "planet_key": "python_variables",
        "title": "Creating Variables in Python",
        "description": "Use the assignment operator to create variables with text and numbers.",
        "learning_objective": (
            "Create variables using the assignment operator and print their values correctly."
        ),
        "content_md": """
# Creating Variables in Python

In Python, you create a variable by using the **assignment operator** `=`.

```python
name = \"Lina\"
age = 19
```

Python reads this as:

- store `\"Lina\"` in `name`
- store `19` in `age`

## Assignment Is Not the Same as Equality in Math

In mathematics, `=` often means “is equal to.”

In programming, `=` usually means:

> take the value on the right and assign it to the name on the left

```python
score = 50
```

This means “put `50` into `score`.”

## Basic Examples

### Storing text

```python
city = \"Chennai\"
```

### Storing a whole number

```python
level = 3
```

### Storing a decimal

```python
temperature = 27.5
```

## Printing Variables

Once a variable is created, you can use it:

```python
planet = \"Earth\"
crew_count = 4

print(planet)
print(crew_count)
```

You can also combine text and variables:

```python
planet = \"Earth\"
print(\"Current planet:\", planet)
```

## Reassigning a Variable

A variable can be updated later.

```python
score = 10
print(score)

score = 15
print(score)
```

Output:

```python
10
15
```

The old value is replaced by the new one.

## Useful Beginner Pattern

A common first pattern is:

1. create a variable
2. store a value
3. print it

```python
favorite_language = \"Python\"
print(favorite_language)
```

## Common Mistakes

### Mistake 1: Forgetting quotes around text

```python
name = Ava
```

This causes an error because Python thinks `Ava` is another variable name.

Correct version:

```python
name = \"Ava\"
```

### Mistake 2: Writing backwards

```python
\"Python\" = language
```

This is invalid.  
The variable name should go on the left.

Correct version:

```python
language = \"Python\"
```

### Mistake 3: Printing the text of the variable name instead of the variable

```python
score = 88
print(\"score\")
```

That prints the word `score`, not the value.

Correct version:

```python
print(score)
```

## Tip

Read your code aloud:

```python
age = 20
```

“Age gets 20.”

That mental habit helps beginners understand assignment.

## Mini Summary

- Use `=` to create and assign variables.
- Put the variable name on the left.
- Put the value on the right.
- Use quotes for text values.
- Use `print()` to check stored values.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 1,
        "xp_reward": 70,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_variables_d3",
        "planet_key": "python_variables",
        "title": "Variable Naming Rules",
        "description": "Learn which names Python accepts and how to choose names that humans can understand.",
        "learning_objective": (
            "Apply Python naming rules and write clear, valid variable names using snake_case."
        ),
        "content_md": """
# Variable Naming Rules

A variable name must be both:

1. **valid for Python**
2. **clear for humans**

Good programmers care about both.

## Rule 1: Use Letters, Numbers, and Underscores

Valid examples:

```python
user_name = \"Nina\"
score2 = 95
planet_name = \"Mars\"
```

## Rule 2: A Name Cannot Start with a Number

Invalid:

```python
2score = 95
```

Valid:

```python
score2 = 95
```

## Rule 3: No Spaces

Invalid:

```python
student name = \"Omar\"
```

Use underscores instead:

```python
student_name = \"Omar\"
```

## Rule 4: Avoid Python Keywords

Some words already have special meaning in Python.

Invalid:

```python
class = \"Math\"
if = 5
```

Python keywords include words like:

- `if`
- `for`
- `while`
- `class`
- `def`

These should not be used as variable names.

## Rule 5: Variable Names Are Case Sensitive

Python treats these as different names:

```python
score = 10
Score = 20
```

That can confuse beginners, so be careful.

## Preferred Style: snake_case

In Python, the common style is **snake_case**:

```python
student_age = 18
total_marks = 480
favorite_color = \"blue\"
```

This is better than unclear styles like:

```python
studentage
StudentAge
x1
```

## Choosing Good Names

Compare these:

```python
x = 19
```

versus

```python
student_age = 19
```

The second one is much easier to understand.

## Common Mistakes

### Mistake 1: Names that are too short

```python
a = \"Ravi\"
b = 92
```

This works, but it is unclear.

### Mistake 2: Names that are too vague

```python
thing = 500
data = \"hello\"
```

These names do not explain the purpose.

### Mistake 3: Inconsistent style

```python
studentName = \"Lia\"
student_age = 18
```

This is harder to read than staying consistent.

## Tip

Ask yourself:

> “If another student reads this variable name, will they understand its purpose?”

If the answer is yes, your name is probably good.

## Mini Summary

- Variable names may use letters, digits, and underscores.
- They cannot start with a digit.
- They cannot contain spaces.
- They should not use Python keywords.
- Use **snake_case** for readable Python code.
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 70,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_variables_d4",
        "planet_key": "python_variables",
        "title": "Dynamic Typing in Python",
        "description": "See how Python lets variables hold values of different types without separate declarations.",
        "learning_objective": (
            "Describe dynamic typing, inspect variable types, and recognize when reassignment changes a variable's type."
        ),
        "content_md": """
# Dynamic Typing in Python

In some programming languages, you must declare a variable's type before using it.

Python is different.

Python uses **dynamic typing**, which means Python figures out the type from the value you assign.

## Example

```python
age = 18
name = \"Ava\"
temperature = 26.5
is_logged_in = True
```

Python automatically understands:

- `age` is an integer
- `name` is a string
- `temperature` is a float
- `is_logged_in` is a boolean

## Checking a Type with `type()`

You can ask Python what kind of value a variable currently has.

```python
age = 18
print(type(age))
```

Output:

```python
<class 'int'>
```

More examples:

```python
print(type(\"hello\"))
print(type(3.14))
print(type(False))
```

## A Variable Can Change Type

Because Python is dynamically typed, the same variable name can later point to a different kind of value.

```python
value = 10
print(type(value))

value = \"ten\"
print(type(value))
```

This is allowed.

## Why This Is Helpful

Dynamic typing makes beginner code quicker to write because you do not need special declarations like:

```python
int age
string name
```

Instead, you can focus on the logic.

## But Be Careful

Just because Python allows changing a type does not always mean it is a good idea.

Example:

```python
score = 100
score = \"excellent\"
```

This may confuse readers because `score` first looked numeric, then became text.

## Common Mistakes

### Mistake 1: Mixing strings and integers by accident

```python
age = \"18\"
print(age + 2)
```

This causes an error because `\"18\"` is text, not a number.

You may need conversion:

```python
age = int(\"18\")
print(age + 2)
```

### Mistake 2: Assuming input gives a number

```python
number = input()
print(number + 5)
```

`input()` gives a string, so convert it when needed:

```python
number = int(input())
print(number + 5)
```

## Tip

Use `type()` while learning.  
It is a great debugging tool for beginners.

## Mini Summary

- Python is **dynamically typed**.
- Python figures out a variable's type from the assigned value.
- A variable can later be assigned a different type.
- `type()` helps you inspect values while learning.
- Be careful when using values from `input()`.
""".strip(),
        "read_time_minutes": 10,
        "difficulty": 2,
        "xp_reward": 80,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_variables_d5",
        "planet_key": "python_variables",
        "title": "Variable Best Practices",
        "description": "Write variable code that is readable, consistent, and easier to debug.",
        "learning_objective": (
            "Use meaningful variable names, keep values predictable, and write beginner-friendly variable code."
        ),
        "content_md": """
# Variable Best Practices

Writing code that *works* is only the beginning.

Good programmers also write code that is:

- easy to read
- easy to update
- easy to debug

Variables play a big role in that.

## 1. Use Meaningful Names

Bad:

```python
x = 450
y = 18
```

Better:

```python
total_marks = 450
student_age = 18
```

A reader should understand the purpose of a variable without guessing.

## 2. Keep Naming Style Consistent

Choose one style and stay with it.

Preferred Python style:

```python
course_name = \"Python Basics\"
quiz_score = 95
```

Avoid mixing styles:

```python
courseName = \"Python Basics\"
quiz_score = 95
```

## 3. Do Not Reuse a Variable for Unrelated Meanings

Confusing:

```python
data = \"Ava\"
data = 95
data = True
```

This is hard to follow.

Clearer:

```python
student_name = \"Ava\"
quiz_score = 95
is_present = True
```

## 4. Update Variables Carefully

Variables can change, but changes should make sense.

```python
score = 50
score = score + 10
```

This is clear: the score increased.

## 5. Use Variables to Avoid Repetition

Instead of repeating a value:

```python
print(\"Welcome, Sam!\")
print(\"Sam is ready.\")
```

Use a variable:

```python
student_name = \"Sam\"
print(\"Welcome,\", student_name)
print(student_name, \"is ready.\")
```

## 6. Check Your Variables While Debugging

If your program behaves strangely, print the variable:

```python
age = input()
print(age)
print(type(age))
```

This helps you find problems quickly.

## 7. Use UPPER_CASE for Fixed Values by Convention

Python beginners sometimes keep an unchanging value in a variable such as a limit or budget.

```python
MAX_SCORE = 100
```

This is a **convention**, not a rule, but it helps readers understand that the value should stay fixed.

## Common Mistakes

### Mistake 1: Vague names

```python
thing = 12
stuff = \"blue\"
```

### Mistake 2: Too many unnecessary reassignments

```python
name = \"Ava\"
name = \"Lia\"
name = \"Mira\"
```

Only reassign when there is a real reason.

### Mistake 3: Hiding meaning

```python
a1 = 450
b2 = 120
```

Technically valid, but poor for readability.

## Tip

Ask:

> “Will this variable name still make sense when I read the code tomorrow?”

If yes, it is probably a good choice.

## Mini Summary

- Choose clear and meaningful names.
- Stay consistent with `snake_case`.
- Avoid using one variable for unrelated meanings.
- Reassign variables only when it makes logical sense.
- Print variable values and types when debugging.
""".strip(),
        "read_time_minutes": 10,
        "difficulty": 2,
        "xp_reward": 90,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_data_types_d1",
        "planet_key": "python_data_types",
        "title": "What Is a Data Type?",
        "description": "Understand why Python needs data types and how they help programs behave correctly.",
        "learning_objective": (
            "Explain what a data type is and describe why Python treats different values differently."
        ),
        "content_md": """
# What Is a Data Type?

When you write a Python program, you work with **values**:

- numbers like `10`
- text like `\"hello\"`
- truth values like `True`

Even though they are all values, Python does **not** treat them the same way.

That is where **data types** come in.

## Definition

A **data type** tells Python what kind of value something is and what operations make sense for it.

For example:

```python
print(10 + 5)
print(\"hello\" + \" world\")
```

Both lines use `+`, but the behavior is different:

- numbers are added
- strings are joined together

Python can do this because it understands the **type** of each value.

## Why Data Types Matter

Imagine a program that stores:

- a student's age
- a student's name
- whether they passed a quiz

These should not all be handled the same way.

```python
student_age = 19
student_name = \"Ava\"
passed_quiz = True
```

Each of these values has a different type, and that helps Python process them correctly.

## Categories of Types

At a beginner level, it helps to think about two big groups:

### Primitive-like single values

These usually store one main value:

- `int`
- `float`
- `str`
- `bool`
- `None`

### Collection values

These store multiple values together:

- `list`
- `tuple`
- `set`
- `dict`

## Real-World Analogy

Think of values like items in labeled containers:

- a number goes in a **number box**
- text goes in a **message box**
- a group of values goes in a **collection box**

If you put the wrong thing in the wrong box, your program may become confusing or fail.

## First Examples

```python
age = 20          # integer
height = 1.72     # float
name = \"Lina\"     # string
is_ready = False  # boolean
```

## Tips

- When you store information, ask: **what kind of value is this?**
- Choosing the right data type makes your code easier to understand.
- Good type choices reduce bugs.

## Common Mistakes

### Mistake 1: Treating `\"5\"` and `5` as the same

They look similar, but they are different:

```python
text_number = \"5\"
real_number = 5
```

### Mistake 2: Assuming Python can guess your intention every time

Python is helpful, but it still depends on the actual type of the value.

## Did You Know?

Python is called a **dynamically typed** language because it figures out a value's type when you assign it.

## Mini Summary

- A data type tells Python what kind of value it is using.
- Different types support different behaviors.
- Choosing the right type helps your program stay correct and readable.
- Python has both single-value types and collection types.
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 1,
        "xp_reward": 6,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_data_types_d2",
        "planet_key": "python_data_types",
        "title": "Numbers and Truth: int, float, and bool",
        "description": "Learn how Python stores whole numbers, decimal numbers, and true-or-false values.",
        "learning_objective": (
            "Differentiate integers, floats, and booleans and use each in a suitable situation."
        ),
        "content_md": """
# Numbers and Truth: `int`, `float`, and `bool`

Some of the most common Python values represent:

- counting
- measuring
- making decisions

That is why `int`, `float`, and `bool` are so important.

## `int` — Whole Numbers

An `int` stores a whole number.

```python
lives = 3
students = 45
temperature = -2
```

Use `int` when the value has **no decimal part**.

## `float` — Decimal Numbers

A `float` stores a number with a decimal point.

```python
height = 1.75
price = 49.99
speed = 88.5
```

Use `float` when a value can include fractions or decimal measurements.

## `bool` — True or False

A `bool` stores one of two values:

- `True`
- `False`

```python
is_logged_in = True
has_submitted = False
```

Booleans are useful for conditions and decisions.

## Comparing the Three

```python
age = 18
average_score = 91.5
passed = True
```

These values all look different because they serve different purposes.

## Real-World Analogy

Imagine a classroom:

- number of students → `int`
- average class score → `float`
- is attendance complete? → `bool`

The type should match the kind of information.

## A Small Example

```python
score = 92
bonus = 2.5
passed = True

print(score)
print(bonus)
print(passed)
```

## Tips

- Use `int` for counts
- Use `float` for measurements
- Use `bool` for yes/no states

## Common Mistakes

### Mistake 1: Writing a boolean as text

```python
passed = \"True\"
```

This is a string, not a boolean.

Correct:

```python
passed = True
```

### Mistake 2: Assuming `5` and `5.0` are the same type

They are close in meaning, but different in type.

- `5` → `int`
- `5.0` → `float`

### Mistake 3: Forgetting that booleans are capitalized

```python
ready = true
```

Incorrect.

Correct:

```python
ready = True
```

## Did You Know?

In Python, `bool` is closely related to numbers:
- `True` behaves like `1`
- `False` behaves like `0`

But you should still treat booleans as logic values, not normal numbers.

## Mini Summary

- `int` stores whole numbers
- `float` stores decimal numbers
- `bool` stores `True` or `False`
- Use the type that matches the meaning of the information
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 1,
        "xp_reward": 7,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_data_types_d3",
        "planet_key": "python_data_types",
        "title": "Strings, Collections, and None",
        "description": "Explore text, grouped data, and Python's special value for 'no value'.",
        "learning_objective": (
            "Use strings, lists, tuples, sets, dictionaries, and None in simple beginner-friendly examples."
        ),
        "content_md": """
# Strings, Collections, and `None`

Not all values are just numbers and booleans.

Python also lets you work with:

- text
- grouped values
- special placeholders

## `str` — Text

A string stores text.

```python
name = \"Ava\"
message = \"Welcome to AlgoLingo\"
```

Strings always use quotes.

## `list` — Ordered and Changeable

A list stores multiple values in order.

```python
colors = [\"red\", \"blue\", \"green\"]
```

Lists are **mutable**, so they can be changed later.

```python
colors[0] = \"yellow\"
```

## `tuple` — Ordered and Not Changeable

A tuple also stores multiple values in order, but it is **immutable**.

```python
coordinates = (10, 20)
```

Tuples are useful when the values should stay fixed.

## `set` — Unique Values

A set stores unique items.

```python
tags = {\"python\", \"coding\", \"python\"}
```

The repeated `\"python\"` does not stay twice.

## `dict` — Labeled Data

A dictionary stores **key-value pairs**.

```python
student = {
    \"name\": \"Lina\",
    \"score\": 92
}
```

This is useful when data has labels.

## `None` — No Value Yet

`None` is Python's special value for “nothing is set here yet.”

```python
middle_name = None
```

It is useful when a value might be filled in later.

## Real-World Analogy

Imagine a student profile:

- student name → `str`
- list of favorite topics → `list`
- fixed seat coordinates → `tuple`
- unique club names → `set`
- student profile details → `dict`
- optional nickname not chosen yet → `None`

## Common Mistakes

### Mistake 1: Forgetting that strings need quotes

```python
language = Python
```

Incorrect.

Correct:

```python
language = \"Python\"
```

### Mistake 2: Expecting sets to keep duplicates

```python
items = {\"pen\", \"pen\", \"book\"}
```

A set keeps only unique values.

### Mistake 3: Treating `None` like text

```python
value = \"None\"
```

That is a string, not the special Python value `None`.

## Tips

- Use `str` for messages and names
- Use `list` when order matters and changes are expected
- Use `tuple` when values should stay fixed
- Use `set` when uniqueness matters
- Use `dict` when your data needs labels

## Did You Know?

A dictionary is one of Python's most useful data structures because it lets you organize data with meaningful labels instead of only positions.

## Mini Summary

- `str` stores text
- `list`, `tuple`, `set`, and `dict` store groups of values
- `None` represents “no value”
- Different types are useful for different situations
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 1,
        "xp_reward": 8,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_data_types_d4",
        "planet_key": "python_data_types",
        "title": "Checking and Converting Types",
        "description": "Use type() to inspect values and convert data safely with int(), float(), str(), and bool().",
        "learning_objective": (
            "Inspect values with type() and perform explicit type conversion for beginner-level programs."
        ),
        "content_md": """
# Checking and Converting Types

Now that you know Python has many data types, you need two important tools:

1. checking a type
2. converting a type

## Using `type()`

The `type()` function tells you what kind of value you have.

```python
print(type(10))
print(type(\"hello\"))
print(type([1, 2, 3]))
```

If you want cleaner output, use:

```python
print(type(10).__name__)
print(type(\"hello\").__name__)
```

## Why Type Checking Is Useful

Suppose you read input:

```python
value = input()
print(type(value).__name__)
```

Even if the user enters `25`, Python stores it as a string.

That matters if you want to do arithmetic.

## Type Conversion

Python provides functions to convert values.

### Convert to `int`

```python
age = int(\"18\")
```

### Convert to `float`

```python
price = float(\"19.5\")
```

### Convert to `str`

```python
score = str(95)
```

### Convert to `bool`

```python
print(bool(1))
print(bool(0))
```

## Input Example

```python
a = int(input())
b = int(input())
print(a + b)
```

Without conversion, `input()` would give strings.

## Common Mistakes

### Mistake 1: Trying to add text and numbers directly

```python
number = input()
print(number + 5)
```

This fails because `number` is text.

### Mistake 2: Converting invalid text

```python
int(\"hello\")
```

This causes an error because `\"hello\"` is not a valid integer.

### Mistake 3: Forgetting that `bool(\"False\")` is `True`

Any non-empty string becomes `True`.

```python
print(bool(\"False\"))
```

## Tips

- Use `type()` when debugging
- Convert values before arithmetic
- Always think: **what type do I have, and what type do I need?**

## Did You Know?

`type(value).__name__` is popular because it is easier for humans to read than the full class output.

## Mini Summary

- `type()` helps you inspect values
- `input()` returns strings
- Use `int()`, `float()`, `str()`, and `bool()` for conversion
- Type conversion is one of the most useful beginner skills in Python
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 2,
        "xp_reward": 9,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_data_types_d5",
        "planet_key": "python_data_types",
        "title": "Mutable vs Immutable and Choosing the Right Type",
        "description": "Learn how changeable values behave and how to choose types more thoughtfully.",
        "learning_objective": (
            "Explain mutable vs immutable objects, choose suitable data types, and apply beginner-friendly best practices."
        ),
        "content_md": """
# Mutable vs Immutable and Choosing the Right Type

When you choose a data type, you are not only choosing what the value looks like.

You are also choosing how it behaves.

## Mutable vs Immutable

### Mutable

A mutable object can be changed after it is created.

Example:

```python
numbers = [1, 2, 3]
numbers[0] = 9
print(numbers)
```

Output:

```python
[9, 2, 3]
```

### Immutable

An immutable object cannot be changed after creation.

Examples:

- `int`
- `float`
- `str`
- `bool`
- `tuple`

```python
name = \"Ava\"
```

You cannot directly change part of the string.

## Reassignment vs Mutation

These are different ideas.

```python
score = 10
score = 20
```

This is **reassignment**.

But this changes the inside of a mutable object:

```python
items = [1, 2, 3]
items[1] = 99
```

That is **mutation**.

## Choosing the Correct Type

Ask these questions:

### Is it a whole number?
Use `int`

### Is it a decimal measurement?
Use `float`

### Is it text?
Use `str`

### Is it true or false?
Use `bool`

### Is it a changeable sequence?
Use `list`

### Is it a fixed sequence?
Use `tuple`

### Do I need unique values only?
Use `set`

### Do I need labels and values together?
Use `dict`

### Is the value missing for now?
Use `None`

## Best Practices

- choose the simplest type that matches the data
- do not use one type when another would be clearer
- use descriptive variable names
- check types while debugging
- avoid changing a variable's meaning too often

## Common Mistakes

### Mistake 1: Using a list when the data should stay fixed

If the value should never change, a tuple may communicate that better.

### Mistake 2: Using a string for a number you want to calculate with

```python
marks = \"90\"
```

If you need arithmetic, convert it.

### Mistake 3: Reusing one variable for unrelated types

```python
data = 5
data = \"hello\"
data = [1, 2]
```

This is legal, but often confusing for beginners.

## Tips

- Let the meaning of the data guide the type choice.
- Prefer clarity over cleverness.
- If a value may change, think about mutability early.

## Did You Know?

Many programming bugs happen not because the code is long, but because the wrong type was chosen for the data.

## Mini Summary

- Mutable values can change after creation
- Immutable values cannot
- Reassignment and mutation are not the same
- Choosing the right data type makes programs easier to read, debug, and improve
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 2,
        "xp_reward": 10,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_operators_d1",
        "planet_key": "python_operators",
        "title": "What Are Operators?",
        "description": "Understand what operators are and why they are essential in Python expressions.",
        "learning_objective": (
            "Explain what an operator is and recognize operators as symbols or keywords that perform actions on values."
        ),
        "content_md": """
# What Are Operators?

Python programs do not just store values—they **do things** with those values.

That is where **operators** come in.

An **operator** is a symbol or keyword that tells Python to perform an action.

Examples:

- `+` adds numbers
- `==` compares values
- `and` combines conditions
- `in` checks membership

## A Simple Idea

If variables are the data containers, operators are the **tools** you use to work with that data.

```python
a = 10
b = 5
print(a + b)
```

Here, `+` is the operator.
It tells Python to add `a` and `b`.

## Operators Help You Answer Questions

Operators can help with many tasks:

- arithmetic: `3 + 2`
- comparisons: `age >= 18`
- logic: `is_ready and has_ticket`
- membership: `"a" in "cat"`

## Operators Can Be Symbols or Words

Some operators are symbols:

```python
+
-
*
/
==
>
```

Some operators are words:

```python
and
or
not
in
is
```

## Real-World Analogy

Imagine a toolbox:

- values are the materials
- operators are the tools

If you want to build something useful, you need both.

## Expressions

When you combine values and operators, you get an **expression**.

```python
5 + 3
score > 50
name == "Ava"
```

Python evaluates expressions and gives a result.

## Why Operators Matter

Without operators, your program could store values, but it could not:

- calculate totals
- compare scores
- update balances
- test conditions
- make decisions later in `if` statements

That is why operators are a major part of programming.

## Tips

- Read expressions slowly from left to right while learning.
- Ask: **what is this operator trying to do?**
- Use parentheses when an expression feels confusing.

## Common Mistakes

### Mistake 1: Confusing `=` with `==`

```python
score = 10
```

This assigns a value.

```python
score == 10
```

This compares values.

### Mistake 2: Treating word operators like variable names

Words like `and`, `or`, and `not` have special meaning in Python.

## Did You Know?

Python has different groups of operators for different jobs, which helps programmers write more expressive code.

## Mini Summary

- Operators perform actions on values.
- They can be symbols like `+` or words like `and`.
- Expressions are built from values and operators.
- Operators help programs calculate, compare, and reason.
""".strip(),
        "read_time_minutes": 7,
        "difficulty": 1,
        "xp_reward": 8,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_operators_d2",
        "planet_key": "python_operators",
        "title": "Arithmetic and Assignment Operators",
        "description": "Use Python to calculate values and update variables efficiently.",
        "learning_objective": (
            "Apply arithmetic operators and assignment operators to perform calculations and update variables."
        ),
        "content_md": """
# Arithmetic and Assignment Operators

Two of the most common operator groups in beginner Python are:

- **arithmetic operators**
- **assignment operators**

These help your program calculate and update values.

## Arithmetic Operators

Python supports the following arithmetic operators:

### Addition `+`

```python
print(4 + 3)
```

### Subtraction `-`

```python
print(10 - 2)
```

### Multiplication `*`

```python
print(6 * 5)
```

### Division `/`

```python
print(8 / 2)
```

This gives a **float** in Python.

### Floor Division `//`

```python
print(9 // 2)
```

This keeps only the whole-number part.

### Modulus `%`

```python
print(9 % 2)
```

This gives the remainder.

### Exponentiation `**`

```python
print(2 ** 3)
```

This means 2 to the power of 3.

## Assignment Operators

The basic assignment operator is:

```python
score = 10
```

You can also update a variable more quickly.

### Add and assign `+=`

```python
score = 10
score += 5
print(score)
```

### Subtract and assign `-=`

```python
score = 10
score -= 3
```

### Multiply and assign `*=`

```python
score = 4
score *= 2
```

### Divide and assign `/=`

```python
score = 8
score /= 2
```

## Real-World Analogy

Imagine a wallet:

- `+` means money added
- `-` means money spent
- `+=` means update the wallet balance after adding money

## Why These Matter

These operators appear in many beginner programs:

- calculating totals
- updating scores
- tracking remaining fuel
- checking even/odd numbers
- computing powers and areas

## Common Mistakes

### Mistake 1: Expecting `/` to return an integer

```python
print(5 / 2)
```

This gives `2.5`, not `2`.

### Mistake 2: Confusing `//` and `/`

- `/` gives regular division
- `//` gives floor division

### Mistake 3: Forgetting `%` means remainder

```python
print(10 % 3)
```

This gives `1`, not `3`.

## Tips

- Use `% 2` to test even or odd numbers.
- Use `**` for powers.
- Use `+=` and `-=` when updating a variable repeatedly.

## Did You Know?

Even simple games often depend on arithmetic and assignment operators to update health, coins, score, and position.

## Mini Summary

- Arithmetic operators calculate values.
- Assignment operators store and update values.
- `/` returns a float.
- `//` returns the floor result.
- `%` returns the remainder.
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 9,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_operators_d3",
        "planet_key": "python_operators",
        "title": "Comparison Operators",
        "description": "Compare values and understand how Python produces True or False results.",
        "learning_objective": (
            "Use comparison operators to compare numbers, strings, and variable values correctly."
        ),
        "content_md": """
# Comparison Operators

Comparison operators let Python answer questions like:

- Is this value bigger?
- Are these values equal?
- Is this score different?

The result of a comparison is always:

- `True`
- `False`

## Common Comparison Operators

### Equal to `==`

```python
print(5 == 5)
```

### Not equal to `!=`

```python
print(5 != 3)
```

### Greater than `>`

```python
print(10 > 4)
```

### Less than `<`

```python
print(2 < 8)
```

### Greater than or equal to `>=`

```python
print(7 >= 7)
```

### Less than or equal to `<=`

```python
print(3 <= 9)
```

## Comparing Variables

```python
score = 85
target = 80

print(score >= target)
```

## Strings Can Be Compared Too

```python
print("cat" == "cat")
print("cat" != "dog")
```

For beginners, equality and inequality are the most useful string comparisons.

## Real-World Analogy

Think of comparison operators as a judge asking yes/no questions:

- Is the student old enough?
- Is the answer correct?
- Is the balance greater than zero?

## Why These Matter

Comparison operators are the foundation of decision-making in programming.

Later, you will use them heavily with:

- `if`
- `elif`
- `while`

## Common Mistakes

### Mistake 1: Using `=` instead of `==`

```python
score = 50
```

This assigns.

```python
score == 50
```

This compares.

### Mistake 2: Forgetting comparisons return booleans

```python
result = 10 > 5
print(result)
```

The result is `True`, not the larger number.

### Mistake 3: Comparing incompatible ideas carelessly

Always ask whether the comparison makes sense for the values involved.

## Tips

- Read `>=` as “greater than or equal to”
- Read `<=` as “less than or equal to”
- Store comparisons in variables if it improves readability

```python
is_passing = score >= 50
```

## Did You Know?

Every time a program checks a rule, a score, or a condition, it is usually using comparison operators somewhere.

## Mini Summary

- Comparison operators return `True` or `False`
- `==` checks equality
- `!=` checks difference
- `>`, `<`, `>=`, and `<=` compare size or order
- Comparisons are essential for decision-making
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 10,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_operators_d4",
        "planet_key": "python_operators",
        "title": "Logical, Membership, and Identity Operators",
        "description": "Combine conditions, check containment, and understand object identity at a beginner level.",
        "learning_objective": (
            "Use logical operators, membership operators, and basic identity checks in beginner-friendly expressions."
        ),
        "content_md": """
# Logical, Membership, and Identity Operators

Python also has operators that help you reason about relationships and conditions.

This discovery introduces:

- logical operators
- membership operators
- identity operators

## Logical Operators

Logical operators combine boolean expressions.

### `and`

Both sides must be `True`.

```python
age = 20
has_ticket = True

print(age >= 18 and has_ticket)
```

### `or`

At least one side must be `True`.

```python
print(age >= 18 or has_ticket)
```

### `not`

Reverses a boolean value.

```python
print(not True)
```

## Membership Operators

Membership operators check whether a value appears inside another value.

### `in`

```python
colors = ["red", "blue", "green"]
print("blue" in colors)
```

### `not in`

```python
print("yellow" not in colors)
```

Membership works with strings too:

```python
print("py" in "python")
```

## Identity Operators

Identity operators check whether two references point to the same object.

### `is`

```python
value = None
print(value is None)
```

### `is not`

```python
name = "Ava"
print(name is not None)
```

## Important Beginner Note

For beginners, the most common safe use of identity operators is with `None`:

```python
if result is None:
    print("No value yet")
```

Do not use `is` when you really mean value equality.

### Use `==` for value comparison

```python
print(5 == 5)
```

### Use `is` mainly for identity checks like `None`

```python
print(result is None)
```

## Real-World Analogy

- `and` is like needing **two keys** to open a box
- `or` is like needing **either key**
- `in` is like checking whether a book is in a bag
- `is None` is like checking whether a seat is still empty

## Common Mistakes

### Mistake 1: Confusing `and` and `or`

- `and` needs both conditions
- `or` needs only one

### Mistake 2: Using `is` instead of `==`

```python
# Prefer this for values
print(a == b)
```

### Mistake 3: Forgetting that `not` changes the truth value

```python
is_ready = False
print(not is_ready)
```

This prints `True`.

## Tips

- Use parentheses if a logical expression feels confusing.
- Use `in` with lists, strings, sets, and dictionaries.
- Use `is None` when checking for a missing value.

## Did You Know?

Search bars, login checks, and filters often rely on logical and membership operators behind the scenes.

## Mini Summary

- `and`, `or`, and `not` work with boolean logic
- `in` and `not in` check membership
- `is` and `is not` check identity
- For beginners, `is None` is the most useful identity pattern
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 2,
        "xp_reward": 11,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_operators_d5",
        "planet_key": "python_operators",
        "title": "Operator Precedence and Best Practices",
        "description": "Learn how Python decides expression order and how to write cleaner operator-based code.",
        "learning_objective": (
            "Interpret operator precedence correctly and apply best practices when writing expressions."
        ),
        "content_md": """
# Operator Precedence and Best Practices

When an expression contains multiple operators, Python needs rules for deciding **what happens first**.

Those rules are called **operator precedence**.

## Example

```python
result = 2 + 3 * 4
print(result)
```

Python does multiplication before addition, so the result is:

```python
14
```

not `20`.

## Parentheses Come First

If you want a different order, use parentheses.

```python
result = (2 + 3) * 4
print(result)
```

Now the result is:

```python
20
```

## A Helpful Beginner Rule

You do not need to memorize every precedence rule immediately.

Just remember:

1. Parentheses first
2. Exponents
3. Multiplication / division / floor division / modulus
4. Addition / subtraction
5. Comparisons
6. Logical operators

## Best Practices for Operators

### 1. Use parentheses when the meaning is not obvious

```python
can_enter = age >= 18 and (has_id or has_parent_permission)
```

This is easier to understand than relying only on precedence.

### 2. Keep expressions readable

Bad:

```python
result = a+b*c-d/e
```

Better:

```python
result = a + b * c - d / e
```

### 3. Break complex logic into variables

```python
is_old_enough = age >= 18
has_access = has_ticket or has_pass

print(is_old_enough and has_access)
```

### 4. Use the right operator

- use `==` for value comparison
- use `is None` for missing-value checks
- use `in` for membership tests

## Real-World Analogy

Think of operator precedence like rules in a recipe:

- some steps must happen before others
- if you want a different order, you must clearly show it

Parentheses are your way of giving Python better instructions.

## Common Mistakes

### Mistake 1: Assuming left-to-right is always enough

```python
2 + 3 * 4
```

Not all expressions are handled left-to-right.

### Mistake 2: Writing expressions that are too crowded

Too many operators in one line can confuse both you and future readers.

### Mistake 3: Depending on memory instead of clarity

If parentheses improve readability, use them.

## Tips

- When in doubt, add parentheses.
- Write spaces around operators.
- Use intermediate variables for long conditions.

## Did You Know?

Readable code is not just easier for humans—it also reduces mistakes during debugging and future updates.

## Mini Summary

- Operator precedence decides evaluation order.
- Parentheses override the default order.
- Clear code is better than clever code.
- Use readable expressions and helper variables when needed.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 2,
        "xp_reward": 12,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_conditionals_d1",
        "planet_key": "python_conditionals",
        "title": "Why Programs Need Decisions",
        "description": "Learn how conditionals let a program choose different actions based on different situations.",
        "learning_objective": (
            "Explain why programs need decision-making and identify boolean expressions as the foundation of conditional logic."
        ),
        "content_md": """
# Why Programs Need Decisions

Until now, your Python programs have mostly followed a straight path:

1. read input  
2. do some work  
3. print output  

But real programs must often **choose** what to do.

For example:

- If a student scores 50 or more, show **Pass**
- If a user enters the correct password, allow access
- If a number is negative, handle it differently

This is called **decision making**.

## What Is a Conditional?

A **conditional** allows code to run only when a condition is true.

The condition is usually a **boolean expression**, meaning an expression that becomes either:

- `True`
- `False`

Example:

```python
score = 72
print(score >= 50)
```

Output:

```python
True
```

The expression `score >= 50` is a boolean expression.

## Decision-Making in Everyday Life

Humans use conditionals constantly:

- If it is raining, take an umbrella.
- If the traffic light is green, go.
- If the battery is low, charge the device.

Programs do the same thing.

## First Conditional Example

```python
age = 20

if age >= 18:
    print("You are an adult.")
```

If the condition is true, the indented line runs.

If the condition is false, nothing happens.

## Flow of a Conditional

### Simple flow diagram

```text
Start
  ↓
Check condition
  ↓
True? ── Yes ──> Run block
  │
  No
  ↓
Continue program
```

## Indentation Matters

Python uses indentation to show which lines belong inside the conditional block.

Correct:

```python
age = 20

if age >= 18:
    print("Adult")
```

Incorrect:

```python
age = 20

if age >= 18:
print("Adult")
```

The second version causes an indentation error.

## Real-World Analogy

Imagine a security guard at a gate:

- If your ID is valid, the gate opens.
- Otherwise, it stays closed.

The program acts like that guard.

## Common Mistakes

### Mistake 1: Forgetting the colon

```python
if age >= 18
    print("Adult")
```

Every `if` statement needs a colon.

### Mistake 2: Writing a condition that is not meaningful

A condition should ask a clear question.

```python
score >= 50
```

This is meaningful.

### Mistake 3: Forgetting indentation

Python depends on indentation to group code correctly.

## Tips

- Read `if` as: **“If this is true, do this.”**
- Start with simple yes/no conditions.
- Always check that your condition produces `True` or `False`.

## Did You Know?

Many major apps—from bank systems to games—rely on conditionals every second to decide what happens next.

## Mini Summary

- Conditionals help programs make decisions.
- They depend on boolean expressions.
- A condition evaluates to `True` or `False`.
- Python uses indentation and a colon to define an `if` block.
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 10,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_conditionals_d2",
        "planet_key": "python_conditionals",
        "title": "Using if and if-else",
        "description": "Write programs that perform one action when a condition is true and another when it is false.",
        "learning_objective": (
            "Use if and if-else statements correctly to control program flow in simple decision-making tasks."
        ),
        "content_md": """
# Using `if` and `if-else`

The `if` statement lets your program do something **only when a condition is true**.

Sometimes, however, you want one action for `True` and a different action for `False`.

That is where `if-else` becomes useful.

## `if` Statement

```python
temperature = 32

if temperature > 30:
    print("It is a hot day.")
```

This prints a message only when the condition is true.

## `if-else` Statement

```python
temperature = 22

if temperature > 30:
    print("It is a hot day.")
else:
    print("It is not a hot day.")
```

Now the program has **two possible paths**.

## Flow Diagram

```text
Start
  ↓
Check condition
  ↓
True? ── Yes ──> Run if block
  │
  No
  ↓
Run else block
```

## A Practical Example

```python
marks = 67

if marks >= 50:
    print("Pass")
else:
    print("Fail")
```

This is a classic decision-making pattern.

## Why `else` Is Useful

Without `else`, the program only handles the true case.

With `else`, the program also clearly handles the false case.

That makes your logic more complete.

## Real-World Analogy

Think of an elevator door:

- If a person is detected, stay open.
- Else, close.

Two outcomes. One condition.

## Common Mistakes

### Mistake 1: Forgetting that `else` has no condition

Incorrect:

```python
else marks < 50:
    print("Fail")
```

Correct:

```python
else:
    print("Fail")
```

### Mistake 2: Writing both branches at the same indentation level incorrectly

The code inside `if` and `else` must be indented properly.

### Mistake 3: Repeating the same condition unnecessarily

If there are only two outcomes, `if-else` is often clearer than multiple separate checks.

## Tips

- Use `if` for one-sided decisions.
- Use `if-else` when you want both outcomes to be explicit.
- Keep each branch focused and readable.

## Did You Know?

A large amount of beginner programming is simply making “if this, then that” decisions.

## Mini Summary

- `if` handles the true case.
- `else` handles the false case.
- `if-else` gives a clear two-path decision structure.
- Good indentation is essential.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 1,
        "xp_reward": 12,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_conditionals_d3",
        "planet_key": "python_conditionals",
        "title": "Multiple Choices with elif and Nested if",
        "description": "Handle multiple possible outcomes and place decisions inside other decisions when necessary.",
        "learning_objective": (
            "Use elif for multi-way branching and nested if statements for layered decision-making."
        ),
        "content_md": """
# Multiple Choices with `elif` and Nested `if`

Sometimes a program has more than two possible outcomes.

That is when `elif` becomes helpful.

## The `elif` Statement

`elif` means:

> “Else, if this other condition is true...”

Example:

```python
score = 83

if score >= 90:
    print("Grade A")
elif score >= 75:
    print("Grade B")
elif score >= 50:
    print("Grade C")
else:
    print("Grade D")
```

This lets the program choose from several paths.

## How Python Checks an `if-elif-else` Chain

Python checks conditions from top to bottom.

The **first true condition** runs, and the rest are skipped.

That means the order matters.

## Flow Diagram

```text
Start
  ↓
Check first condition
  ↓
True? ── Yes ──> Run first block
  │
  No
  ↓
Check next condition
  ↓
True? ── Yes ──> Run next block
  │
  No
  ↓
Run else block
```

## Nested `if`

A nested `if` is an `if` inside another `if`.

Example:

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
```

This is useful when one decision depends on another.

## When to Use Nested if

Use nested `if` when the second decision should only happen **after** the first one passes.

Example:
- first check age
- then check ID
- then allow entry

## Real-World Analogy

Imagine airport security:

1. If you have a ticket, continue.
2. If your ID is valid, continue.
3. Then allow boarding.

That is a layered decision process.

## Common Mistakes

### Mistake 1: Wrong order in `elif`

If you place a broad condition first, later cases may never be reached.

### Mistake 2: Using too many nested levels

Deep nesting can become hard to read.

### Mistake 3: Forgetting that only one branch in an `if-elif-else` chain runs

Once Python finds a true condition, it stops checking the rest.

## Tips

- Put the most specific conditions first when needed.
- Use `elif` for multiple exclusive choices.
- Use nested `if` only when it improves meaning.

## Did You Know?

Many validation systems, grading tools, and menu-driven programs use `elif` chains behind the scenes.

## Mini Summary

- `elif` handles additional conditions after `if`.
- Python checks conditions from top to bottom.
- Only the first matching branch runs.
- Nested `if` helps with layered decisions.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 2,
        "xp_reward": 14,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_conditionals_d4",
        "planet_key": "python_conditionals",
        "title": "Logical Conditions and Boolean Thinking",
        "description": "Combine comparisons and logical operators to express richer conditions.",
        "learning_objective": (
            "Build compound boolean expressions using comparison operators and logical operators inside conditionals."
        ),
        "content_md": """
# Logical Conditions and Boolean Thinking

Conditionals become more powerful when you combine multiple checks.

That is where **boolean expressions** and logical operators become very useful.

## Boolean Expressions

A boolean expression is any expression that becomes either:

- `True`
- `False`

Example:

```python
age >= 18
score < 50
username == "admin"
```

## Combining Conditions with `and`

`and` means both conditions must be true.

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("You may enter.")
```

## Combining Conditions with `or`

`or` means at least one condition must be true.

```python
day = "Saturday"
is_holiday = False

if day == "Saturday" or is_holiday:
    print("No class today.")
```

## Reversing a Condition with `not`

`not` flips a boolean value.

```python
is_raining = False

if not is_raining:
    print("Go for a walk.")
```

## Boolean Flow Diagram

```text
Condition A
   ↓
Condition B
   ↓
Combine with and/or/not
   ↓
Final True/False result
```

## Using Comparisons Inside Conditions

```python
temperature = 24

if temperature >= 20 and temperature <= 30:
    print("Comfortable")
```

This is a very common pattern.

## Real-World Analogy

Imagine a scholarship application:

- if marks are high **and** attendance is strong → eligible
- if one of the documents is missing **or** the deadline passed → not eligible

That is logical decision-making.

## Common Mistakes

### Mistake 1: Forgetting parentheses in longer conditions

While Python has precedence rules, parentheses can make logic easier to read.

### Mistake 2: Using `or` when you really need `and`

These two operators produce very different behavior.

### Mistake 3: Writing complicated logic without testing small parts

Break big conditions into simpler pieces if needed.

## Tips

- Start with one condition, then combine carefully.
- Use helper variables if the condition becomes long.

```python
is_old_enough = age >= 18
has_access = has_ticket or has_pass
```

- Use parentheses for readability.

## Did You Know?

Search filters, login rules, and recommendation systems often depend on many combined boolean conditions.

## Mini Summary

- Boolean expressions become `True` or `False`
- `and` needs both conditions
- `or` needs at least one
- `not` reverses truth
- Combined conditions help programs make smarter decisions
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 2,
        "xp_reward": 16,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_conditionals_d5",
        "planet_key": "python_conditionals",
        "title": "Conditional Expressions and Best Practices",
        "description": "Write cleaner decision logic using ternary expressions and readable conditional style.",
        "learning_objective": (
            "Use Python's conditional expression and apply best practices for clear, maintainable conditional code."
        ),
        "content_md": """
# Conditional Expressions and Best Practices

Python also offers a short way to choose between two values.

This is called a **conditional expression**, or sometimes a **ternary expression**.

## Conditional Expression Syntax

```python
value_if_true if condition else value_if_false
```

Example:

```python
age = 20
message = "Adult" if age >= 18 else "Minor"
print(message)
```

This is compact and useful for simple cases.

## When to Use It

Conditional expressions are helpful when:

- the decision is short
- you are choosing between two simple values
- readability is still clear

## When Not to Use It

Avoid using a conditional expression if it makes the code harder to understand.

For complex logic, a full `if-else` block is usually better.

## Example Comparison

### Full if-else

```python
score = 72

if score >= 50:
    result = "Pass"
else:
    result = "Fail"
```

### Conditional expression

```python
score = 72
result = "Pass" if score >= 50 else "Fail"
```

Both are correct.

## Best Practices for Conditionals

### 1. Keep conditions readable

Bad:

```python
if age>=18 and has_id==True:
    print("Allowed")
```

Better:

```python
if age >= 18 and has_id:
    print("Allowed")
```

### 2. Use meaningful variable names

```python
is_eligible = marks >= 50
```

### 3. Avoid deeply nested logic if a simpler structure works

### 4. Use parentheses when they improve clarity

```python
if age >= 18 and (has_id or has_guardian_permission):
    print("Allowed")
```

### 5. Test edge cases

For example:
- exactly 18
- exactly 50
- empty input
- zero values

## Flow Diagram

```text
Check condition
   ↓
True? ── Yes ──> use first value
  │
  No
  ↓
use second value
```

## Real-World Analogy

A ternary expression is like a fast mental shortcut:

- If it rains, take a jacket
- Else, take sunglasses

Quick decision. Two clear outcomes.

## Common Mistakes

### Mistake 1: Using ternary expressions for complicated logic

If readers need to stop and decode the line, it is too complex.

### Mistake 2: Overusing nested conditionals

Readable code matters more than short code.

### Mistake 3: Forgetting clarity in conditions

A correct condition is good, but a clear condition is better.

## Tips

- Use conditional expressions for small decisions only.
- Prefer clarity over compactness.
- Review your conditionals as if another beginner will read them.

## Did You Know?

In professional codebases, maintainability often matters more than writing the shortest possible code.

## Mini Summary

- A conditional expression is Python's short two-choice form.
- Use it only when the logic stays easy to read.
- Clean, readable conditionals are better than clever ones.
- Good decision-making code is easy to test and maintain.
""".strip(),
        "read_time_minutes": 10,
        "difficulty": 2,
        "xp_reward": 18,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_loops_d1",
        "planet_key": "python_loops",
        "title": "Why Loops Exist",
        "description": "Learn why repeating code manually is inefficient and how loops solve that problem.",
        "learning_objective": (
            "Explain why loops are useful and identify repeated tasks that should be solved with iteration."
        ),
        "content_md": """
# Why Loops Exist

Imagine writing a program that prints the numbers from 1 to 5.

Without loops, you might write:

```python
print(1)
print(2)
print(3)
print(4)
print(5)
```

That works, but it becomes tiring, repetitive, and hard to maintain.

What if you needed to print 1 to 100?  
Or process 500 student marks?  
Or repeat a check until a user gives the correct answer?

This is why **loops** exist.

## What Is a Loop?

A **loop** lets your program repeat a block of code.

Instead of copying code many times, you define the repeated action once and let Python run it again and again.

## Why Loops Matter

Loops help you:

- reduce repeated code
- process groups of data
- repeat actions until a condition changes
- write programs that scale better

## Real-World Analogy

Think of a washing machine.

It does not ask a person to repeat “wash, rinse, spin” manually 20 times.  
It follows a repeated cycle automatically.

A loop works like that cycle.

## A First Example

```python
for number in range(1, 6):
    print(number)
```

Output:

```python
1
2
3
4
5
```

The loop repeats the `print(number)` line with different values.

## Flow Diagram

```text
Start
  ↓
Set up loop
  ↓
Run loop body
  ↓
Need another repetition?
  ├─ Yes → Run body again
  └─ No  → Continue program
```

## Two Big Loop Types in Python

You will mainly use:

- `for` loops → when repeating over a sequence or known range
- `while` loops → when repeating while a condition remains true

## Common Mistakes

### Mistake 1: Using repeated print statements instead of a loop

That works for tiny examples but does not scale well.

### Mistake 2: Thinking loops are only for numbers

Loops can also work with:

- strings
- lists
- ranges
- input-driven conditions

### Mistake 3: Forgetting that repetition should still be meaningful

A loop should help a real repeated task, not just add complexity.

## Tips

- When you see repeated code, ask: **Should this be a loop?**
- Start by understanding the repeated action.
- Then decide what controls the repetition.

## Did You Know?

Many programs you use every day rely on loops to process messages, update game screens, load files, and check user input.

## Mini Summary

- Loops repeat code automatically.
- They reduce duplication.
- They make programs more powerful and scalable.
- Python mainly uses `for` loops and `while` loops for repetition.
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 1,
        "xp_reward": 10,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_loops_d2",
        "planet_key": "python_loops",
        "title": "for Loops and range()",
        "description": "Use for loops to repeat actions over a sequence or a range of numbers.",
        "learning_objective": (
            "Write for loops with range() and predict how many times a loop body will run."
        ),
        "content_md": """
# `for` Loops and `range()`

A `for` loop is one of the most beginner-friendly loop tools in Python.

It is useful when you want to repeat something a known number of times or loop through a sequence.

## Basic `for` Loop

```python
for item in [1, 2, 3]:
    print(item)
```

The loop takes each item one by one and runs the body.

## Using `range()`

`range()` is commonly used with `for` loops.

```python
for number in range(5):
    print(number)
```

Output:

```python
0
1
2
3
4
```

### Important Note

`range(5)` starts at `0` and stops **before** `5`.

## Common `range()` Patterns

### `range(stop)`

```python
range(5)
```

Gives:

```python
0, 1, 2, 3, 4
```

### `range(start, stop)`

```python
range(1, 6)
```

Gives:

```python
1, 2, 3, 4, 5
```

### `range(start, stop, step)`

```python
range(2, 11, 2)
```

Gives:

```python
2, 4, 6, 8, 10
```

## Example: Print 1 to 5

```python
for number in range(1, 6):
    print(number)
```

## Example: Repeat a message

```python
for _ in range(3):
    print("Keep learning!")
```

The `_` is often used when the loop variable itself is not important.

## Flow Diagram

```text
Start
  ↓
Get next value from range/sequence
  ↓
Run loop body
  ↓
More values left?
  ├─ Yes → Repeat
  └─ No  → Exit loop
```

## Real-World Analogy

Imagine a teacher calling attendance from a list of names one by one.

That is similar to how a `for` loop moves through values in order.

## Common Mistakes

### Mistake 1: Expecting `range(5)` to include 5

It stops before the endpoint.

### Mistake 2: Forgetting indentation

```python
for i in range(3):
print(i)
```

This causes an error.

### Mistake 3: Choosing a confusing loop variable name

Good:

```python
for number in range(5):
```

Less clear:

```python
for x in range(5):
```

## Tips

- Use `range(start, stop)` when you want exact visible boundaries.
- Use clear loop variable names like `number`, `student`, or `item`.
- If you only need repetition, `_` is acceptable.

## Did You Know?

A `for` loop is often safer than a `while` loop for known repetition because it is less likely to run forever by accident.

## Mini Summary

- `for` loops repeat over a sequence.
- `range()` helps generate numeric repetition.
- `range(stop)` excludes the stop value.
- `range(start, stop, step)` gives more control.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 1,
        "xp_reward": 11,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_loops_d3",
        "planet_key": "python_loops",
        "title": "while Loops and Repetition by Condition",
        "description": "Use while loops when repetition should continue only while a condition stays true.",
        "learning_objective": (
            "Write while loops that update conditions correctly and stop at the right time."
        ),
        "content_md": """
# `while` Loops and Repetition by Condition

A `while` loop repeats **as long as a condition remains true**.

This makes it useful when you do not know exactly how many times repetition will be needed.

## Basic Structure

```python
while condition:
    # code to repeat
```

Python checks the condition before each repetition.

## Example: Count from 1 to 5

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

## Why the Update Matters

The line:

```python
count += 1
```

changes the value of `count`.

Without that update, the condition may stay true forever.

## When to Use `while`

Use a `while` loop when repetition depends on a condition, such as:

- trying again until the answer is correct
- repeating until a value reaches a limit
- running until a user chooses to stop

## Example: Password Retry

```python
password = ""

while password != "python123":
    password = input("Enter password: ")
```

This repeats until the correct password is entered.

## Flow Diagram

```text
Start
  ↓
Check condition
  ↓
True? ── Yes ──> Run loop body
  │                 ↓
  │            Update something
  │                 ↓
  └────── Check condition again
False
  ↓
Exit loop
```

## Real-World Analogy

Think of knocking on a door until someone answers.

- while nobody answers → knock again
- when someone answers → stop

## Common Mistakes

### Mistake 1: Forgetting to update the variable

```python
count = 1

while count <= 5:
    print(count)
```

This becomes an infinite loop.

### Mistake 2: Writing a condition that never becomes false

Always make sure the loop has a realistic stopping point.

### Mistake 3: Using `while` when a `for` loop would be simpler

If you know the number of repetitions in advance, `for` is often clearer.

## Tips

- Ask: **what changes inside the loop so it can stop?**
- Test with small examples first.
- Print debug values if a loop behaves strangely.

## Did You Know?

Many menu-driven programs and games use `while` loops to keep running until the user chooses to exit.

## Mini Summary

- `while` loops repeat while a condition is true.
- They are useful for condition-driven repetition.
- Always update something important inside the loop.
- A bad condition or missing update can cause an infinite loop.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 2,
        "xp_reward": 12,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_loops_d4",
        "planet_key": "python_loops",
        "title": "Loop Control: break, continue, and pass",
        "description": "Control loop behavior by stopping early, skipping work, or using placeholders safely.",
        "learning_objective": (
            "Use break, continue, and pass appropriately to control loop execution."
        ),
        "content_md": """
# Loop Control: `break`, `continue`, and `pass`

Sometimes you need more control inside a loop.

Python gives you three useful tools:

- `break`
- `continue`
- `pass`

## `break` — Stop the Loop Early

`break` ends the loop immediately.

```python
for number in range(1, 10):
    if number == 5:
        break
    print(number)
```

Output:

```python
1
2
3
4
```

When Python reaches 5, the loop stops.

## `continue` — Skip This Iteration

`continue` skips the rest of the current loop cycle and moves to the next one.

```python
for number in range(1, 6):
    if number == 3:
        continue
    print(number)
```

Output:

```python
1
2
4
5
```

The value 3 is skipped.

## `pass` — Do Nothing for Now

`pass` is a placeholder that tells Python:

> “I am intentionally leaving this block empty.”

```python
for number in range(3):
    pass
```

This loop runs, but does nothing visible.

## When `pass` Is Useful

You may use `pass` while planning code structure:

```python
if True:
    pass
```

It keeps the code syntactically valid while you think or build step by step.

## Flow Diagram

```text
Loop starts
  ↓
Check special condition
  ├─ break    → exit loop
  ├─ continue → skip to next cycle
  └─ pass     → do nothing, continue normally
```

## Real-World Analogy

Imagine students in a queue:

- `break` → close the line early
- `continue` → skip one student and move to the next
- `pass` → stand still and do nothing for the moment

## Common Mistakes

### Mistake 1: Using `break` when you only meant to skip one item

If you only want to skip one cycle, use `continue`, not `break`.

### Mistake 2: Using `pass` expecting visible output

`pass` does nothing by itself.

### Mistake 3: Putting `continue` before an important update in a `while` loop

That can accidentally prevent the loop from reaching its stopping condition.

## Tips

- Use `break` to stop searching once you found what you needed.
- Use `continue` to ignore unwanted cases.
- Use `pass` only when a real placeholder is needed.

## Did You Know?

Many search programs use `break` so they stop as soon as the target item is found, instead of wasting extra work.

## Mini Summary

- `break` exits a loop immediately
- `continue` skips the current iteration
- `pass` does nothing and acts as a placeholder
- These tools help you control loop behavior more precisely
""".strip(),
        "read_time_minutes": 8,
        "difficulty": 2,
        "xp_reward": 13,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_loops_d5",
        "planet_key": "python_loops",
        "title": "Nested Loops, Infinite Loops, and Best Practices",
        "description": "Use loops inside loops when needed and avoid dangerous repetition mistakes.",
        "learning_objective": (
            "Recognize nested loops, avoid infinite loops, and apply best practices when writing iterative code."
        ),
        "content_md": """
# Nested Loops, Infinite Loops, and Best Practices

Loops become even more powerful when one loop appears inside another.

But with power comes responsibility: bad loop design can create bugs or infinite repetition.

## Nested Loops

A **nested loop** is a loop inside another loop.

Example:

```python
for row in range(2):
    for col in range(3):
        print(row, col)
```

Output:

```python
0 0
0 1
0 2
1 0
1 1
1 2
```

The inner loop runs completely for each outer loop cycle.

## When Nested Loops Are Useful

Nested loops help with:

- grids
- tables
- patterns
- comparing pairs of values

## Infinite Loops

An **infinite loop** keeps running forever.

Example:

```python
while True:
    print("This never stops")
```

This is not always wrong, but beginners often create infinite loops by accident.

### Accidental Infinite Loop

```python
count = 1

while count <= 5:
    print(count)
```

This never stops because `count` is never updated.

## Best Practices

### 1. Make the stopping condition clear

A reader should quickly understand how the loop ends.

### 2. Use `for` when the repetition count is known

### 3. Use `while` when repetition depends on a changing condition

### 4. Avoid deep nesting unless it is truly needed

### 5. Use clear variable names

```python
for row in range(3):
    for column in range(2):
        print(row, column)
```

This is clearer than using vague names like `a` and `b`.

### 6. Test with small values first

If you are printing patterns or using nested loops, small test cases are easier to debug.

## Flow Diagram

```text
Outer loop starts
   ↓
Run inner loop completely
   ↓
Outer loop repeats
   ↓
All loops finish
```

## Real-World Analogy

Think of a classroom grid:

- outer loop = each row
- inner loop = each seat in that row

You finish one row before moving to the next.

## Common Mistakes

### Mistake 1: Forgetting updates in a while loop

This often creates infinite loops.

### Mistake 2: Writing nested loops when one loop is enough

### Mistake 3: Making the loop body too complicated

Simple loops are easier to test and maintain.

## Tips

- Use nested loops carefully and only when they match the problem.
- When debugging, print variable values to see how the loop changes.
- If a loop seems stuck, inspect the stopping condition.

## Did You Know?

Many visual programs, grid-based games, and table generators depend on nested loops to build repeated structures.

## Mini Summary

- Nested loops repeat a loop inside another loop
- Infinite loops happen when a stopping condition never becomes false
- Choose the loop type that best fits the problem
- Clear stopping logic and readable variables make loops safer and easier to maintain
""".strip(),
        "read_time_minutes": 10,
        "difficulty": 2,
        "xp_reward": 14,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_functions_d1",
        "planet_key": "python_functions",
        "title": "Why Functions Matter",
        "description": "Learn why functions help programmers avoid repetition and build clearer programs.",
        "learning_objective": (
            "Explain why functions are useful and identify repeated code that should be turned into reusable functions."
        ),
        "content_md": """
# Why Functions Matter

As programs grow, repeated code becomes a problem.

Imagine writing the same greeting logic again and again:

```python
print("Welcome, Ava!")
print("Welcome, Ravi!")
print("Welcome, Lina!")
```

That works, but it is not scalable.

A better idea is to write the behavior once and reuse it.

That is the purpose of **functions**.

## What Is a Function?

A **function** is a named block of code that performs a specific task.

Once defined, a function can be used whenever needed.

## Why Functions Are Important

Functions help you:

- reduce repeated code
- organize programs into smaller parts
- make code easier to test
- improve readability
- reuse logic in many places

## Real-World Analogy

Think of a function like a kitchen appliance.

A toaster has one clear job:
- put in bread
- run the process
- get toast

You do not rebuild the toaster every morning.
You use the same tool again and again.

Functions work like reusable tools in code.

## A Simple Example

```python
def say_hello():
    print("Hello!")
```

This creates a function named `say_hello`.

It will not run immediately.
It only runs when you call it.

## Flow Diagram

```text
Define function
      ↓
Store reusable instructions
      ↓
Call function later
      ↓
Run its code
```

## One Job Per Function

A good beginner rule is:

> each function should do one clear job

Example:

```python
def show_welcome():
    print("Welcome to AlgoLingo!")
```

That is easier to understand than one huge function doing many unrelated things.

## Common Mistakes

### Mistake 1: Thinking a function runs when it is defined

Defining a function only stores the instructions.

### Mistake 2: Writing repeated code instead of reusing logic

If the same action appears many times, a function may be a better choice.

### Mistake 3: Giving unclear names

A function name should explain its purpose.

Bad:

```python
def thing():
    print("Hello")
```

Better:

```python
def show_greeting():
    print("Hello")
```

## Tips

- Use functions for repeated tasks.
- Choose clear function names.
- Start with small functions that solve one problem.

## Did You Know?

Large software systems often contain hundreds or thousands of functions, each responsible for a small part of the overall program.

## Mini Summary

- Functions are reusable blocks of code.
- They help reduce repetition.
- They make code easier to organize and maintain.
- Good functions have clear names and focused responsibilities.
""".strip(),
        "read_time_minutes": 9,
        "difficulty": 1,
        "xp_reward": 16,
        "order_number": 1,
        "status": DiscoveryStatus.AVAILABLE,
        "prerequisites": [],
    },
    {
        "key": "python_functions_d2",
        "planet_key": "python_functions",
        "title": "Defining and Calling Functions",
        "description": "Create your own functions and run them by calling their names.",
        "learning_objective": (
            "Define basic functions with def and call them correctly in Python."
        ),
        "content_md": """
# Defining and Calling Functions

In Python, functions are created using the `def` keyword.

## Basic Syntax

```python
def function_name():
    # code block
```

Example:

```python
def greet():
    print("Hello, Explorer!")
```

This defines a function named `greet`.

## Calling a Function

To run the function, write its name followed by parentheses:

```python
greet()
```

Output:

```python
Hello, Explorer!
```

## What the Parentheses Mean

Parentheses tell Python:

> run this function now

Without the parentheses, you are only referring to the function itself.

## A Full Example

```python
def show_planet():
    print("Current planet: Functions")

show_planet()
show_planet()
```

Output:

```python
Current planet: Functions
Current planet: Functions
```

One function definition. Multiple uses.

## Flow Diagram

```text
Write def statement
      ↓
Store function instructions
      ↓
Call function with ()
      ↓
Python runs the function body
```

## Indentation Still Matters

Just like loops and conditionals, the function body must be indented.

Correct:

```python
def greet():
    print("Hi")
```

Incorrect:

```python
def greet():
print("Hi")
```

## Real-World Analogy

Imagine saving a phone number under a contact name.

- defining the function is like saving the contact
- calling the function is like tapping the contact to make the call

## Common Mistakes

### Mistake 1: Forgetting parentheses when calling

```python
greet
```

This does not call the function.

### Mistake 2: Calling before defining

Python needs to know the function first.

### Mistake 3: Bad indentation inside the function body

Python uses indentation to know which lines belong to the function.

## Tips

- Use `def` to define a function.
- Use `()` to call it.
- Keep first functions short and simple while learning.

## Did You Know?

A program can call the same function many times, which is one reason functions are so powerful.

## Mini Summary

- `def` creates a function.
- Function calls use parentheses.
- A function runs only when called.
- Correct indentation is essential.
""".strip(),
        "read_time_minutes": 10,
        "difficulty": 1,
        "xp_reward": 18,
        "order_number": 2,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_functions_d3",
        "planet_key": "python_functions",
        "title": "Parameters, Arguments, and Return Values",
        "description": "Pass information into functions and send useful results back out.",
        "learning_objective": (
            "Use parameters, arguments, and return values to make functions flexible and useful."
        ),
        "content_md": """
# Parameters, Arguments, and Return Values

Functions become much more useful when they can work with different inputs.

## Parameters and Arguments

A **parameter** is a variable inside the function definition.

An **argument** is the actual value you pass in when calling the function.

Example:

```python
def greet(name):
    print("Hello,", name)

greet("Ava")
```

Here:

- `name` is the parameter
- `"Ava"` is the argument

## Why Parameters Matter

Without parameters, a function always does the exact same thing.

With parameters, the same function can work with many values.

```python
def square(number):
    print(number * number)

square(3)
square(5)
```

## Returning Values

Some functions should give a result back.

Use `return` for that.

```python
def add(a, b):
    return a + b
```

Now you can store or print the result:

```python
result = add(4, 6)
print(result)
```

## Why return Is Better Than Only print

Compare these:

```python
def add_and_print(a, b):
    print(a + b)
```

versus

```python
def add(a, b):
    return a + b
```

The second version is more reusable because the result can be used later.

## Flow Diagram

```text
Call function
    ↓
Send arguments in
    ↓
Function works with parameters
    ↓
Return a result
    ↓
Use result outside
```

## Real-World Analogy

Think of ordering coffee:

- parameters are the options available: size, sugar, milk
- arguments are the actual choices: medium, 2 sugars, yes milk
- return value is the final drink you receive

## Common Mistakes

### Mistake 1: Confusing print with return

`print()` shows output.
`return` sends a value back.

### Mistake 2: Forgetting to use the returned value

```python
def add(a, b):
    return a + b
```

If you never use the result, the function still returns it—but your program does nothing with it.

### Mistake 3: Passing the wrong number of arguments

If a function expects two values, you must provide two unless defaults are defined.

## Tips

- Use parameters to make functions reusable.
- Use `return` when the result will be needed later.
- Use clear parameter names like `width`, `height`, or `student_name`.

## Did You Know?

Many of Python's built-in tools, such as `len()` and `sum()`, are functions that take arguments and return values.

## Mini Summary

- Parameters are placeholders in a function definition.
- Arguments are real values passed into a call.
- `return` sends a result back to the caller.
- Returned values make functions far more useful than print-only functions.
""".strip(),
        "read_time_minutes": 12,
        "difficulty": 2,
        "xp_reward": 20,
        "order_number": 3,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_functions_d4",
        "planet_key": "python_functions",
        "title": "Scope, Default Parameters, and Keyword Arguments",
        "description": "Control where variables are visible and make functions easier to call in flexible ways.",
        "learning_objective": (
            "Distinguish between local and global scope, use default parameters, and call functions with positional and keyword arguments."
        ),
        "content_md": """
# Scope, Default Parameters, and Keyword Arguments

As functions become more useful, you also need to understand where variables exist and how function calls can be customized.

## Local Scope

A variable created inside a function usually belongs only to that function.

```python
def show_score():
    score = 95
    print(score)
```

The variable `score` is local to `show_score`.

## Global Scope

A variable defined outside functions is global.

```python
planet_name = "Functions"

def show_planet():
    print(planet_name)
```

The function can read the global variable.

## Why Scope Matters

Scope helps prevent variables from interfering with each other.

It keeps function logic more organized.

## Default Parameters

A function parameter can have a default value.

```python
def greet(name="Explorer"):
    print("Hello,", name)
```

You can call it with or without an argument:

```python
greet()
greet("Ava")
```

## Positional Arguments

These are matched by order.

```python
def introduce(name, age):
    print(name, age)

introduce("Ava", 19)
```

## Keyword Arguments

These are matched by parameter name.

```python
introduce(age=19, name="Ava")
```

Keyword arguments can improve readability.

## Flow Diagram

```text
Define function
   ↓
Set parameters (some may have defaults)
   ↓
Call function
   ↓
Arguments matched by position or keyword
   ↓
Function runs using local variables
```

## Real-World Analogy

Imagine a restaurant order form:

- local scope = notes used only in the kitchen for this one order
- global scope = the restaurant name on the building
- default parameter = standard fries unless another side is chosen
- keyword argument = specifying exactly which option belongs to which field

## Common Mistakes

### Mistake 1: Expecting a local variable to exist outside the function

### Mistake 2: Putting a required parameter after a default one incorrectly

### Mistake 3: Mixing argument order carelessly

Keyword arguments help reduce confusion.

## Tips

- Prefer local variables for most function work.
- Use default values when a common option makes sense.
- Use keyword arguments when a function call would be clearer.

## Did You Know?

Many professional APIs use keyword arguments because they make code easier to read and reduce mistakes.

## Mini Summary

- Local variables belong to a function.
- Global variables exist outside functions.
- Default parameters provide fallback values.
- Positional arguments depend on order.
- Keyword arguments depend on parameter names.
""".strip(),
        "read_time_minutes": 13,
        "difficulty": 2,
        "xp_reward": 22,
        "order_number": 4,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
    {
        "key": "python_functions_d5",
        "planet_key": "python_functions",
        "title": "*args, **kwargs, Docstrings, and Function Best Practices",
        "description": "Get a beginner-friendly introduction to flexible function inputs and write cleaner, more professional functions.",
        "learning_objective": (
            "Understand the beginner use of *args and **kwargs, write docstrings, and apply function design best practices."
        ),
        "content_md": """
# `*args`, `**kwargs`, Docstrings, and Function Best Practices

By now, you know how to define and call functions with normal parameters.

This final discovery introduces more flexible function ideas and better coding habits.

## `*args`

`*args` lets a function receive many positional arguments.

```python
def add_all(*args):
    print(args)

add_all(1, 2, 3)
```

Output:

```python
(1, 2, 3)
```

Inside the function, `args` behaves like a tuple.

## `**kwargs`

`**kwargs` lets a function receive many keyword arguments.

```python
def show_profile(**kwargs):
    print(kwargs)

show_profile(name="Ava", age=19)
```

Output:

```python
{'name': 'Ava', 'age': 19}
```

Inside the function, `kwargs` behaves like a dictionary.

## Beginner Perspective

You do not need to master `*args` and `**kwargs` immediately.

For now, it is enough to understand:

- `*args` collects extra positional values
- `**kwargs` collects extra keyword values

## Docstrings

A **docstring** is a string written inside a function to explain what it does.

```python
def greet(name):
    \"\"\"Print a friendly greeting.\"\"\"
    print("Hello,", name)
```

Docstrings help humans understand the function later.

## Best Practices for Functions

### 1. Use clear names

```python
def calculate_area(width, height):
    return width * height
```

### 2. Keep one function focused on one job

### 3. Use parameters instead of hardcoding values

### 4. Return useful values when needed

### 5. Add docstrings for clarity

## Flow Diagram

```text
Define function
   ↓
Name it clearly
   ↓
Add parameters / optional flexibility
   ↓
Write focused logic
   ↓
Return or print result
   ↓
Document with a docstring
```

## Real-World Analogy

Think of functions as labeled tools in a toolbox:

- a clear label helps you choose the right tool
- a focused tool does one job well
- a flexible tool can handle a range of similar tasks

## Common Mistakes

### Mistake 1: Writing one huge function for everything

### Mistake 2: Using unclear names like `do_it` or `thing`

### Mistake 3: Forgetting that `*args` and `**kwargs` collect multiple values, not just one

### Mistake 4: Writing functions without explaining them

## Tips

- Use `*args` and `**kwargs` only when flexibility is really needed.
- Prefer clear normal parameters first.
- Write functions that another beginner could understand tomorrow.

## Did You Know?

Well-written functions make large programs easier to test, reuse, and improve over time.

## Mini Summary

- `*args` collects extra positional arguments
- `**kwargs` collects extra keyword arguments
- docstrings explain what a function does
- clean naming and focused design make functions more powerful
""".strip(),
        "read_time_minutes": 16,
        "difficulty": 2,
        "xp_reward": 24,
        "order_number": 5,
        "status": DiscoveryStatus.LOCKED,
        "prerequisites": [],
    },
)
