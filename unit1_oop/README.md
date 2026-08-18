# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

This assignment explored object-oriented programming (OOP) concepts in Python,
including class inheritance, instance and class namespaces, and the distinction
between shallow and deep copying. A **university course management** scenario was
used as the modeling context throughout.

---

## Implementation Summary

### Class Design

**`Course` (Parent Class — TODO 1)**

The `Course` class was designed to represent a generic university course.

- A class variable `institution` was defined to store a value shared by all
  `Course` instances, demonstrating that class-level data lives outside any
  individual object.
- Three instance variables were initialized in `__init__`: `course_code`,
  `course_name`, and `credits`. A fourth, `enrolled_students`, was included
  as a mutable list to support the copying demonstration in TODO 4.
- The `display_info()` method was implemented to print all course attributes
  in a labeled format.
- The `enroll_student()` method included input validation to reject empty or
  whitespace-only names, demonstrating edge case handling.
- `__str__` and `__repr__` special methods were implemented for readable
  string output.

**`OnlineCourse` (Child Class — TODO 2)**

The `OnlineCourse` class inherited from `Course` using `super().__init__()`
to reuse all parent initialization logic.

- A new class variable `delivery_mode` was added to mark all online courses
  as asynchronous.
- Two new instance variables were added: `platform` (the LMS or video tool)
  and `meeting_schedule`.
- A new method `get_access_instructions()` was implemented, providing
  platform-specific login guidance.
- `display_info()` was overridden to extend the parent's output with
  online-specific fields, using `super().display_info()` to avoid code
  duplication.

---

### Namespace Demonstration (TODO 3)

Two `OnlineCourse` objects were created. The class variable `institution` was
accessed both through the class itself (`Course.institution`) and through an
instance (`course1.institution`), demonstrating Python's attribute lookup chain.

A dynamic attribute `instructor` was added to `course1` after creation, which
wrote directly into `course1.__dict__` and had no effect on `course2`. The
`__dict__` of both objects was printed to make this difference visible. The
class namespace was inspected using `OnlineCourse.__dict__`, showing only
class-level attributes and methods rather than instance data.

---

### Shallow vs. Deep Copying (TODO 4)

A `Course` object with a nested mutable list (`enrolled_students`) was used
to demonstrate copying behavior.

- **Shallow copy (`copy()`):** Created a new `Course` object, but both the
  original and the shallow copy shared the same `enrolled_students` list
  object in memory. Appending a student to the original also appeared in the
  shallow copy.
- **Deep copy (`deepcopy()`):** Created a fully independent `Course` object
  with its own copy of the list. Modifying the original's roster had no effect
  on the deep copy.

The identity check `is` was used to confirm whether the nested list was the
same object in memory, making the distinction concrete and verifiable.

---

### Edge Cases Handled

- An empty string and a whitespace-only string were passed to `enroll_student()`
  to verify that the guard clause prevented invalid data from entering the roster.
- `isinstance()` was used to confirm that a child object is recognized as an
  instance of both the child class and the parent class, while the parent object
  is correctly rejected as an instance of the child class.

---

## Real-World Use Case

University course management systems rely on OOP principles at every layer.
Each course is an independent object with its own roster, yet all share
institution-level metadata through class variables. Inheritance allows
specialized course types — online, hybrid, in-person — to extend a shared
base without rewriting common logic. The shallow vs. deep copy distinction
is directly relevant to systems that clone configuration objects or session
data, where shared references can introduce subtle bugs that are difficult
to trace in production.

---

## How to Run

```bash
python unit1_discussion.py
```

No external dependencies are required beyond Python's standard library.

---

## Reflection

Completing this assignment deepened my understanding of how Python manages
data at both the class and instance levels. One of the most valuable
realizations was how Python resolves attribute lookups — checking the
instance namespace first before falling back to the class — and how this
means a class variable can appear accessible from an instance without
actually living in that instance's `__dict__`.

The shallow versus deep copy distinction was initially non-obvious, but
working through the list mutation example made it concrete: a shallow copy
shares references to nested objects, while a deep copy creates a fully
independent structure. This distinction matters significantly in real
applications where data is passed between components and unintended mutation
can cause hard-to-trace bugs.

Compared to procedural programming, OOP organizes code around objects rather
than around functions that act on raw data. This makes it easier to model
real-world entities, encapsulate behavior alongside the data it operates on,
and extend functionality through inheritance without modifying existing code.
The reusability benefit was directly visible in this assignment: `OnlineCourse`
gained all of `Course`'s functionality for free and only needed to define what
was genuinely different. In larger systems, this kind of modularity reduces
duplication, lowers the risk of inconsistency across a codebase, and allows
teams to build and maintain components independently.
