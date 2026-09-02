"""
==================================================
Unit 3 DISCUSSION: List Operations (Insert, Delete, Search)
==================================================
INSTRUCTIONS:
This assignment focuses on understanding how lists behave when elements
are inserted, removed, and searched. You will analyze how Python lists
shift elements in memory and how different operations impact performance.

SCENARIO USED IN THIS SUBMISSION:
A deployment runbook. The list holds the ordered steps an engineer follows
to push a release. Order is the whole point of the structure - step 3 must
run after step 2 - so inserting a forgotten step in the middle has to push
every later step down by one position rather than overwrite anything.
"""


def show(label, lst):
    """Helper used throughout the demos to print a labelled list state."""
    print(f"  {label:<34} {lst}   (length = {len(lst)})")


def insert_at(lst, index, value):
    """
    TODO (Student):
    Insert a value into the list at the specified index.
    Requirements:
    - Use a list operation to insert the value.
    - Add comments explaining what happens to existing elements
      after an insertion occurs.
    - Use comments to explain how insertion performance may vary depending on
      where the insertion occurs.

    WHAT HAPPENS TO EXISTING ELEMENTS:
    A Python list stores its elements in one contiguous block of references.
    Inserting at position i does not overwrite anything - the element already
    at i, and every element after it, is SHIFTED one slot to the right to open
    a gap. Each shifted element therefore gets a new index: what was index 3
    becomes index 4, index 4 becomes index 5, and so on. The list grows by
    exactly one, and no existing value is lost.

    HOW PERFORMANCE VARIES BY POSITION:
    The cost is driven by how many elements have to move, which is (n - index).
      * Insert at the END   -> 0 elements shift  -> O(1) amortized
      * Insert in the MIDDLE-> n/2 elements shift-> O(n)
      * Insert at the BEGINNING -> all n shift   -> O(n), the worst case
    "Amortized" at the end because the list occasionally has to grow its
    underlying block and copy everything once; that one-time cost is spread
    across many cheap appends, so each append averages out to constant time.
    """
    lst.insert(index, value)
    return lst


def delete_at(lst, index):
    """
    TODO (Student):
    Remove and return the value at the specified index.
    Requirements:
    - Validate that the index exists.
    - Return the removed value.
    - Return None if the index is invalid.
    - Add comments explaining why index validation and safe deletion are important.

    WHY INDEX VALIDATION MATTERS:
    Calling lst.pop(i) with an out-of-range index raises IndexError, which
    terminates the program. Index values usually come from somewhere the code
    does not control - user input, a search result, a loop counter - so an
    invalid index is a normal runtime possibility rather than a rare bug. The
    guard below checks the index against the current length FIRST and returns
    None instead, so the caller can handle the miss without the program dying.

    WHY THE EMPTY-LIST CASE IS CHECKED SEPARATELY:
    An empty list has no valid index at all, so every deletion on it must fail.
    Checking len(lst) == 0 up front makes that intent explicit in the code.

    NOTE ON NEGATIVE INDEXES:
    Python accepts lst[-1] as "last element", so a stray -1 would silently
    delete from the end rather than error. That is rarely what a caller who
    passed a bad index meant, so this function treats negatives as invalid.

    WHAT HAPPENS TO THE REMAINING ELEMENTS:
    Deletion is the mirror image of insertion. Removing position i closes the
    gap by shifting every element after i one slot to the LEFT, so their
    indexes all decrease by one. Deleting from the front is O(n); deleting
    from the end shifts nothing and is O(1).
    """
    # Guard 1: nothing can be removed from an empty list.
    if len(lst) == 0:
        return None

    # Guard 2: reject negatives and anything at or past the end.
    # Valid indexes for a list of length n are 0 through n-1.
    if index < 0 or index >= len(lst):
        return None

    removed = lst.pop(index)  # safe now - the index is known to exist
    return removed


def search_value(lst, value):
    """
    TODO (Student):
    Search for a value within the list.
    Requirements:
    - Return the index if the value is found.
    - Return -1 if the value is not found.
    - Add comments explaining why this is a linear search and why it scans sequentially.

    WHY THIS IS A LINEAR SEARCH:
    The function walks the list one position at a time from index 0 and
    compares each element to the target. That sequential walk is what makes it
    "linear" - the work grows in a straight line with the number of elements.

    WHY IT MUST SCAN SEQUENTIALLY:
    An unsorted list carries no information about WHERE a value might be.
    Seeing "Build artifact" at index 0 tells you nothing about whether the
    target sits at index 1 or index 900, so no position can be ruled out
    without being examined. A binary search can skip half the list on every
    comparison only because a sorted list guarantees which half the target
    must be in. Without that ordering guarantee, every element is a candidate
    until it has been checked.

    PERFORMANCE:
      * Best case  - target is at index 0        -> 1 comparison, O(1)
      * Worst case - target is last or absent    -> n comparisons, O(n)
      * Average    - roughly n/2 comparisons     -> O(n)
    A miss is always the worst case, because the whole list must be exhausted
    before absence can be proven.

    The loop also returns the FIRST match. If a value appears more than once,
    the later copies are never reached.
    """
    for index in range(len(lst)):   # visit each position in order, 0 upward
        if lst[index] == value:     # compare the element at this position
            return index            # found - stop early, no need to look further
    return -1                       # the entire list was scanned without a match


def main():
    print("=== UNIT 3: LIST OPERATIONS ===")

    # ===============================
    # TODO (Student): INSERTION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Create a list containing several values.
    # 2. Display the original list.
    # 3. Test insertion at:
    #    - the beginning
    #    - the middle
    #    - the end
    # 4. Display the list after each insertion.
    # 5. Use comments to explain each step in the implementation.

    print("\n=== INSERTION TESTS ===")
    print("Scenario: a deployment runbook whose steps must stay in execution order.\n")

    # (1) and (2): build the starting runbook and show it.
    runbook = ["Pull latest code", "Run unit tests", "Build artifact", "Deploy to staging"]
    show("Original runbook:", runbook)

    # (3a) INSERT AT THE BEGINNING - index 0.
    # Every one of the 4 existing steps shifts right by one position.
    # "Pull latest code" moves from index 0 to index 1, and so on down the list.
    # This is the most expensive insertion because the maximum number of
    # elements have to move: O(n).
    insert_at(runbook, 0, "Notify the team")
    show("After insert at index 0:", runbook)
    print("     -> All 4 existing steps shifted RIGHT by one. 'Pull latest code' moved 0 -> 1.")
    print("     -> Worst case for insertion: every element moved, O(n).\n")

    # (3b) INSERT IN THE MIDDLE - index 3.
    # Only the elements from index 3 onward shift right. Everything before
    # index 3 keeps its position, so roughly half the list moves: O(n) but
    # with about half the work of a front insertion.
    insert_at(runbook, 3, "Scan for vulnerabilities")
    show("After insert at index 3:", runbook)
    print("     -> Only steps from index 3 onward shifted. Indexes 0-2 were untouched.")
    print("     -> A forgotten step was slotted in without overwriting anything.\n")

    # (3c) INSERT AT THE END - index len(runbook).
    # No element sits after this position, so nothing shifts at all. This is
    # the cheapest insertion: O(1) amortized.
    insert_at(runbook, len(runbook), "Smoke test staging")
    show("After insert at the end:", runbook)
    print("     -> Zero elements shifted, because nothing sits after the last index.")
    print("     -> Cheapest insertion: O(1) amortized.")

    # ===============================
    # TODO (Student): DELETION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Delete an item from:
    #    - the beginning
    #    - the middle
    #    - the end
    # 2. Display the removed value.
    # 3. Display the updated list after each deletion.
    # 4. Use comments to clearly explain what is happening in the output.

    print("\n=== DELETION TESTS ===")
    show("Starting list:", runbook)
    print()

    # (1a) DELETE FROM THE BEGINNING - index 0.
    # Removing the first element leaves a gap at index 0, so every remaining
    # element shifts LEFT by one to close it. Indexes all decrease by one.
    removed = delete_at(runbook, 0)
    print(f"  delete_at(index 0)   removed -> '{removed}'")
    show("List after deletion:", runbook)
    print("     -> All remaining steps shifted LEFT by one to close the gap: O(n).\n")

    # (1b) DELETE FROM THE MIDDLE - index 2.
    # Only the elements after index 2 shift left. The earlier ones are stable.
    removed = delete_at(runbook, 2)
    print(f"  delete_at(index 2)   removed -> '{removed}'")
    show("List after deletion:", runbook)
    print("     -> Only elements after index 2 moved; indexes 0-1 were unaffected.\n")

    # (1c) DELETE FROM THE END - the last valid index.
    # Nothing follows the last element, so no shifting occurs: O(1).
    last_index = len(runbook) - 1
    removed = delete_at(runbook, last_index)
    print(f"  delete_at(index {last_index})   removed -> '{removed}'")
    show("List after deletion:", runbook)
    print("     -> No elements shifted, because nothing followed the last index: O(1).")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for a value that exists.
    # 2. Search for a value that does not exist.
    # 3. Display the search results with clear explanations.
    # 4. Use comments to explain each step.

    print("\n=== SEARCH TESTS ===")
    show("List being searched:", runbook)
    print()

    # (1) SEARCH FOR A VALUE THAT EXISTS.
    # The scan starts at index 0 and stops the moment a match is found, so a
    # value near the front costs far fewer comparisons than one near the back.
    target = "Build artifact"
    result = search_value(runbook, target)
    print(f"  search_value('{target}') -> returned index {result}")
    print(f"     -> FOUND. The scan checked indexes 0 through {result} and stopped early.")
    print(f"     -> That is {result + 1} comparison(s), not a full pass over the list.\n")

    # A value at the very front is the best case: one comparison.
    first_item = runbook[0]
    result = search_value(runbook, first_item)
    print(f"  search_value('{first_item}') -> returned index {result}")
    print("     -> BEST CASE: matched on the very first comparison, O(1).\n")

    # (2) SEARCH FOR A VALUE THAT DOES NOT EXIST.
    # Absence cannot be proven early. Every element must be checked before the
    # function can safely conclude the value is missing, so a miss is always
    # the worst case: n comparisons.
    missing = "Roll back release"
    result = search_value(runbook, missing)
    print(f"  search_value('{missing}') -> returned {result}")
    print(f"     -> NOT FOUND. -1 signals absence, which is distinct from index 0.")
    print(f"     -> All {len(runbook)} elements were compared. A miss is always O(n),")
    print("        because absence can only be proven by exhausting the list.")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Delete using an invalid index
    # - Search for a missing value
    # - Insert into an empty list
    # - Delete from an empty list
    # - Use comments to explain each edge case.

    print("\n=== EDGE CASES ===")

    # EDGE CASE 1: delete using an index past the end of the list.
    # lst.pop(99) would raise IndexError and crash. The validation in
    # delete_at() catches it and returns None instead.
    print("\n  [1] Deleting with an index past the end of the list:")
    show("Current list:", runbook)
    result = delete_at(runbook, 99)
    print(f"      delete_at(index 99) -> returned {result}")
    print(f"      Valid indexes are 0 to {len(runbook) - 1}. The list is unchanged, no crash.")

    # EDGE CASE 2: delete using a negative index.
    # Python would interpret -1 as the last element and silently delete it.
    # That is almost never what a caller who passed a bad index intended, so
    # delete_at() rejects negatives outright.
    print("\n  [2] Deleting with a negative index:")
    result = delete_at(runbook, -1)
    print(f"      delete_at(index -1) -> returned {result}")
    show("List is unchanged:", runbook)
    print("      Python would have read -1 as 'last element' and deleted it silently.")
    print("      Rejecting negatives makes an accidental bad index visible instead.")

    # EDGE CASE 3: delete from an empty list.
    # There is no valid index at all, so every deletion must fail cleanly.
    print("\n  [3] Deleting from an empty list:")
    empty = []
    show("Empty list:", empty)
    result = delete_at(empty, 0)
    print(f"      delete_at(index 0) -> returned {result}")
    print("      Index 0 is valid on a list of length 5 but invalid on a list of length 0.")
    print("      Validity depends on the CURRENT length, not on the index looking reasonable.")

    # EDGE CASE 4: search an empty list.
    # The loop body never executes, so the function falls straight through to
    # the -1 return. No special case was needed for this - it works by design.
    print("\n  [4] Searching an empty list:")
    result = search_value(empty, "anything")
    print(f"      search_value('anything') -> returned {result}")
    print("      The loop never ran, so the function returned -1 with zero comparisons.")

    # EDGE CASE 5: insert into an empty list.
    # Insertion at index 0 of an empty list has nothing to shift and simply
    # becomes the first element.
    print("\n  [5] Inserting into an empty list:")
    insert_at(empty, 0, "First step")
    show("After insert at index 0:", empty)
    print("      Nothing existed to shift, so the value became index 0.")

    # EDGE CASE 6: insert with an index far past the end.
    # Unlike pop(), Python's list.insert() does NOT raise here - it clamps the
    # index to the end of the list. This is worth demonstrating because it is
    # a silent behavior that can hide a bug: the value still lands in the list,
    # just not where the caller asked.
    print("\n  [6] Inserting with an index far past the end:")
    insert_at(empty, 50, "Clamped step")
    show("After insert at index 50:", empty)
    print("      list.insert() does NOT raise on an out-of-range index - it CLAMPS")
    print("      to the end. The value landed at index 1, not 50. Silent behavior")
    print("      like this is worth knowing, since it hides a bad index rather")
    print("      than surfacing it the way pop() would.")

    print("\n=== SUMMARY ===")
    print("Insert and delete cost depends on POSITION, because elements shift:")
    print("  front  -> all n elements move  -> O(n)")
    print("  middle -> about n/2 move       -> O(n)")
    print("  end    -> nothing moves        -> O(1)")
    print("Search by value is always a sequential scan -> O(n); a miss is the worst case.")
    print("Access by index is the exception: it is O(1), because the position is")
    print("computed directly rather than searched for.")


if __name__ == "__main__":
    main()
