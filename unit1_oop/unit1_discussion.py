"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.
"""


from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.
#
# Replace the pass statement with your implementation.

class Course:
    """
    Represents a university course.
    Serves as the parent class for all course types.
    """

    # Class variable: shared across ALL Course instances
    institution = "University of Maryland Global Campus"

    def __init__(self, course_code, course_name, credits):
        """
        Initialize a Course object.

        Args:
            course_code (str): Identifier such as 'CMSC 315'
            course_name (str): Full name of the course
            credits (int):     Number of credit hours
        """
        # Instance variables: unique to each Course object
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.enrolled_students = []   # Nested mutable data — used in TODO 4

    def enroll_student(self, student_name):
        """Add a student to the roster with basic error handling."""
        # Edge case: reject empty or whitespace-only names
        if not student_name or not student_name.strip():
            print(f"  [ERROR] Student name cannot be empty — enrollment rejected.")
            return
        self.enrolled_students.append(student_name.strip())
        print(f"  Enrolled '{student_name.strip()}' in {self.course_code}.")

    def display_info(self):
        """Display all information about this course."""
        print(f"  Institution : {Course.institution}")
        print(f"  Course Code : {self.course_code}")
        print(f"  Course Name : {self.course_name}")
        print(f"  Credits     : {self.credits}")
        roster = self.enrolled_students if self.enrolled_students else ["(none)"]
        print(f"  Roster      : {roster}")

    def __str__(self):
        return f"Course({self.course_code} | {self.course_name} | {self.credits} cr)"

    def __repr__(self):
        return (f"Course(course_code={self.course_code!r}, "
                f"course_name={self.course_name!r}, credits={self.credits})")


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class OnlineCourse(Course):
    """
    Extends Course with attributes and behavior specific to online delivery.
    Demonstrates inheritance, method overriding, and super() usage.
    """

    # New class variable: applies to every OnlineCourse instance
    delivery_mode = "Online / Asynchronous"

    def __init__(self, course_code, course_name, credits, platform, meeting_schedule):
        """
        Initialize an OnlineCourse, building on the parent constructor.

        Args:
            course_code      (str): Identifier such as 'CMSC 315'
            course_name      (str): Full name of the course
            credits          (int): Number of credit hours
            platform         (str): LMS or video platform (e.g., 'LEO', 'Zoom')
            meeting_schedule (str): When synchronous sessions occur, if any
        """
        # Delegate shared initialization to the parent class
        super().__init__(course_code, course_name, credits)

        # New instance variables added by the child class
        self.platform = platform
        self.meeting_schedule = meeting_schedule

    def get_access_instructions(self):
        """New method: return a formatted access string for this online course."""
        return (f"  Log in to {self.platform} to access {self.course_code}. "
                f"Schedule: {self.meeting_schedule}.")

    def display_info(self):
        """
        Override parent display_info to include online-specific details.
        Calls super() first to avoid duplicating shared logic.
        """
        super().display_info()   # Print the inherited fields
        print(f"  Delivery    : {OnlineCourse.delivery_mode}")
        print(f"  Platform    : {self.platform}")
        print(f"  Schedule    : {self.meeting_schedule}")

    def __str__(self):
        return (f"OnlineCourse({self.course_code} | {self.course_name} | "
                f"{self.credits} cr | via {self.platform})")


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")

    # Create two OnlineCourse objects
    course1 = OnlineCourse(
        "CMSC 315", "Data Structures and Algorithms", 3,
        "LEO Portal", "Asynchronous"
    )
    course2 = OnlineCourse(
        "CMSC 320", "Software Engineering", 3,
        "Zoom", "Tuesdays 7-9 PM ET"
    )

    # Access class variable through the CLASS itself
    print("\n[Accessing class variables via the class]")
    print(f"  Course.institution         : {Course.institution}")
    print(f"  OnlineCourse.delivery_mode : {OnlineCourse.delivery_mode}")

    # Access the same class variable through an INSTANCE
    # Python checks instance __dict__ first, then falls back to the class
    print("\n[Accessing class variables via an instance]")
    print(f"  course1.institution        : {course1.institution}")
    print(f"  course1.delivery_mode      : {course1.delivery_mode}")

    # Add a new attribute to ONLY course1 after creation
    # This writes into course1's instance namespace and does not affect course2
    course1.instructor = "Dr. Smith"
    print("\n[Dynamic attribute added to course1 only]")
    print(f"  course1.instructor         : {course1.instructor}")
    print(f"  course2 has 'instructor'?  : {'instructor' in course2.__dict__}")

    # Display instance namespaces (__dict__ holds only instance-level attributes)
    print("\n[course1.__dict__]  <-- includes dynamic 'instructor' key")
    for key, val in course1.__dict__.items():
        print(f"    {key}: {val}")

    print("\n[course2.__dict__]  <-- no 'instructor' key")
    for key, val in course2.__dict__.items():
        print(f"    {key}: {val}")

    # Display class namespace (class variables and methods, no dunder keys)
    print("\n[OnlineCourse class namespace (non-dunder keys)]")
    class_keys = [k for k in OnlineCourse.__dict__ if not k.startswith("__")]
    print(f"  {class_keys}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")

    # Create an original Course with a nested mutable list (enrolled_students)
    original = Course("CMSC 401", "Algorithm Analysis", 3)
    original.enroll_student("Alice Johnson")
    original.enroll_student("Bob Martinez")

    # SHALLOW COPY: copy() creates a new object, but nested objects
    # (like the enrolled_students list) are NOT duplicated — both the
    # original and the shallow copy point to the SAME list in memory.
    shallow = copy(original)

    # DEEP COPY: deepcopy() creates a fully independent clone, including
    # recursive copies of all nested mutable objects. Changes to the
    # original's list will NOT affect the deep copy.
    deep = deepcopy(original)

    print("\n[Before modification]")
    print(f"  original.enrolled_students : {original.enrolled_students}")
    print(f"  shallow.enrolled_students  : {shallow.enrolled_students}")
    print(f"  deep.enrolled_students     : {deep.enrolled_students}")

    print(f"\n  original list IS shallow list? "
          f"{original.enrolled_students is shallow.enrolled_students}  "
          f"<-- same object in memory")
    print(f"  original list IS deep list?   "
          f"{original.enrolled_students is deep.enrolled_students}  "
          f"<-- independent copy")

    # Mutate the original's nested list
    original.enroll_student("Carol White")

    print("\n[After adding 'Carol White' to original only]")
    print(f"  original.enrolled_students : {original.enrolled_students}")
    print(f"  shallow.enrolled_students  : {shallow.enrolled_students}"
          f"  <-- also changed (shared reference)")
    print(f"  deep.enrolled_students     : {deep.enrolled_students}"
          f"  <-- unchanged (deep copy is independent)")


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    # --- Parent class object ---
    print("\n--- Parent Class: Course ---")
    parent_course = Course("CMSC 100", "Introduction to Computing", 3)
    parent_course.enroll_student("Ermiyes Alemayehu")
    parent_course.display_info()
    print(f"  __str__ : {parent_course}")

    # Edge case: enroll with an empty name
    print("\n[Edge case: empty student name]")
    parent_course.enroll_student("")
    parent_course.enroll_student("   ")

    # --- Child class object ---
    print("\n--- Child Class: OnlineCourse (inherits from Course) ---")
    child_course = OnlineCourse(
        "CMSC 315", "Data Structures and Algorithms", 3,
        "LEO Portal", "Asynchronous with optional Zoom Q&A on Thursdays"
    )
    child_course.enroll_student("Ermiyes Alemayehu")
    child_course.enroll_student("Jordan Lee")

    # Demonstrates inheritance: overridden display_info calls super()
    print("\n[display_info() — overridden method calling super()]")
    child_course.display_info()

    # New method available only on OnlineCourse
    print("\n[get_access_instructions() — child-only method]")
    print(child_course.get_access_instructions())

    # Confirm inheritance relationship
    print(f"\n  isinstance(child_course, Course)       : {isinstance(child_course, Course)}")
    print(f"  isinstance(child_course, OnlineCourse) : {isinstance(child_course, OnlineCourse)}")
    print(f"  isinstance(parent_course, OnlineCourse): {isinstance(parent_course, OnlineCourse)}")

    demonstrate_namespaces()
    demonstrate_copying()


if __name__ == "__main__":
    main()
