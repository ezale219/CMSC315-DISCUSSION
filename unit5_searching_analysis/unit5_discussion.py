"""
=====================================================
UNIT 5 DISCUSSION: SEARCH ALGORITHMS (LINEAR vs BINARY)
=====================================================

INSTRUCTIONS:
In this assignment, you will implement and analyze two
fundamental search algorithms: linear search and binary search.

You will demonstrate your understanding by modifying the
provided code, running experiments on different dataset sizes,
and clearly explaining your results through code comments
and program output.

Application scenario: Music Streaming Library Search System
Song IDs are stored in a sorted list. Two search strategies are
compared to find a specific song by its ID number.
"""

import time


def linear_search(lst, target):
    """
    TODO (Student):
    Implement a linear search algorithm.

    Requirements:
    - Search the list from beginning to end.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining why linear search
      has O(n) time complexity.

    Why linear search is O(n):
    Linear search makes no assumption about the order of the list.
    It checks every element one at a time, starting from index 0.
    In the worst case — target absent or at the very last position —
    every single element must be examined. As the list grows by n
    elements, the number of comparisons also grows by n, which is
    the definition of O(n) (linear) time complexity.
    """
    # Scan every element from the beginning to the end of the list.
    # There is no shortcut: each element must be compared individually
    # because we cannot assume the list is ordered.
    for i in range(len(lst)):
        # Compare the current element to the target.
        # This is the only comparison linear search can make — it has
        # no information about where the target might be relative to
        # the current position.
        if lst[i] == target:
            # Target found — return its index immediately.
            # Returning here avoids unnecessary comparisons on the
            # remaining elements.
            return i

    # Target was not found after checking every element.
    # -1 is the standard sentinel value for "not found."
    return -1


def binary_search(lst, target):
    """
    TODO (Student):
    Implement a binary search algorithm.

    Requirements:
    - Assume the list is already sorted.
    - Repeatedly reduce the search space by half.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining how each iteration
      reduces the search space.

    How binary search reduces the search space:
    At each step, the algorithm compares the target to the MIDDLE
    element of the current range. If the target equals the middle,
    the search is complete. If the target is larger, the entire left
    half is discarded (all elements smaller than the middle cannot
    contain the target). If smaller, the entire right half is discarded.
    This halving at every step gives O(log n) time complexity:
    1,000,000 elements requires at most 20 comparisons.
    """
    # low and high define the boundaries of the active search range.
    # Both are inclusive. The entire list is in range at the start.
    low = 0
    high = len(lst) - 1
    # For an empty list, high = -1, so the loop never executes
    # and -1 is returned safely without any list access.

    while low <= high:
        # Calculate the midpoint of the current search range.
        # Integer division (//) automatically floors the result.
        mid = (low + high) // 2

        # Iteration 1 reduces the search space from n to n/2.
        # Iteration 2 reduces it from n/2 to n/4.
        # After k iterations, at most n / 2^k elements remain.
        # The loop terminates when the range is empty (low > high).

        if lst[mid] == target:
            # Found the target at the midpoint — return its index.
            return mid

        elif lst[mid] < target:
            # Middle element is too small.
            # The target must be in the RIGHT half of the current range.
            # Discard the left half by moving low past the midpoint.
            # +1 ensures mid itself is excluded (already checked).
            low = mid + 1

        else:
            # Middle element is too large.
            # The target must be in the LEFT half of the current range.
            # Discard the right half by moving high before the midpoint.
            # -1 ensures mid itself is excluded (already checked).
            high = mid - 1

    # Search range is now empty — target is not in the list.
    return -1


def main():
    print("=== UNIT 5: SEARCH ALGORITHMS ===")

    # ===============================
    # TODO (Student): SMALL DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a small sorted dataset.
    # 2. Test both linear search and binary search.
    # 3. Search for:
    #    - a value that exists
    #    - a value that does not exist
    # 4. Use comments to clearly explain the results.

    print("\n=== SMALL DATASET TEST ===")

    # A small sorted list of 10 song IDs from a music streaming library.
    # Both algorithms will find the same results; the difference is HOW
    # many comparisons each one makes to get there.
    small_songs = [1003, 1012, 1025, 1041, 1058, 1067, 1074, 1089, 1095, 1100]

    print(f"Dataset ({len(small_songs)} song IDs): {small_songs}")
    target_found    = 1058   # Song ID that EXISTS in the list (index 4)
    target_missing  = 1050   # Song ID that does NOT exist in the list

    # --- Search for an existing value ---
    print(f"\nSearching for song ID {target_found} (exists in list):")

    lin_result = linear_search(small_songs, target_found)
    print(f"  Linear search  -> index {lin_result}"
          f"  (checked up to {lin_result + 1} element(s) to find it)")
    # Linear search had to check indices 0-4 to reach the target.
    # On a 10-element list this is acceptable; on 10 million it is not.

    bin_result = binary_search(small_songs, target_found)
    print(f"  Binary search  -> index {bin_result}"
          f"  (eliminated half the list at each of ~3 comparisons)")
    # Binary search: mid of [0,9]=4 → lst[4]=1058 == target. Found in 1 step.

    # --- Search for a missing value ---
    print(f"\nSearching for song ID {target_missing} (not in list):")

    lin_result = linear_search(small_songs, target_missing)
    print(f"  Linear search  -> {lin_result}  (checked all {len(small_songs)} elements)")
    # Every element was checked before confirming the value is absent.

    bin_result = binary_search(small_songs, target_missing)
    print(f"  Binary search  -> {bin_result}  (range narrowed until empty, ~4 comparisons)")
    # Binary search narrowed: [0,9]→[0,3]→[0,1]→[1,1]→empty. Done in 4 steps.

    # ===============================
    # TODO (Student): LARGE DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a much larger sorted dataset.
    # 2. Test both search algorithms.
    # 3. Compare the results.
    # 4. Use comments to explain why binary search becomes more
    #    efficient as datasets grow larger.

    print("\n=== LARGE DATASET TEST ===")

    # A large sorted list of 1,000,000 even-numbered song IDs.
    # This simulates a music platform with a million-track library.
    large_songs = list(range(0, 2_000_000, 2))   # [0, 2, 4, ..., 1999998]
    target_large_found   = 1_456_782   # Exists (even number, near the end)
    target_large_missing = 1_456_783   # Does not exist (odd number)

    print(f"Dataset size: {len(large_songs):,} song IDs")
    print(f"Searching for ID {target_large_found:,} (exists) "
          f"and {target_large_missing:,} (missing)")

    # --- Linear search on large dataset (timing) ---
    start = time.perf_counter()
    lin_large = linear_search(large_songs, target_large_found)
    lin_time  = time.perf_counter() - start
    print(f"\n  Linear search  -> index {lin_large:,}  "
          f"time: {lin_time:.6f}s")
    # Linear search had to scan ~728,000 elements to reach this index.
    # At O(n), time grows proportionally with dataset size.

    # --- Binary search on large dataset (timing) ---
    start = time.perf_counter()
    bin_large = binary_search(large_songs, target_large_found)
    bin_time  = time.perf_counter() - start
    print(f"  Binary search  -> index {bin_large:,}  "
          f"time: {bin_time:.6f}s")
    # Binary search needed at most log2(1,000,000) ≈ 20 comparisons.
    # At O(log n), time grows logarithmically — nearly constant at scale.

    if lin_time > 0 and bin_time > 0:
        speedup = lin_time / bin_time
        print(f"\n  Binary search was approximately {speedup:.0f}x faster on this dataset.")
    print("  Why: each binary search comparison eliminates HALF the remaining")
    print("  elements. Linear search eliminates only ONE element per step.")
    print(f"  For {len(large_songs):,} elements: linear O(n) = up to 1,000,000 steps;")
    print(f"  binary O(log n) ≈ 20 steps.")

    # --- Missing value on large dataset ---
    bin_missing = binary_search(large_songs, target_large_missing)
    print(f"\n  Binary search for missing {target_large_missing:,} -> {bin_missing}  "
          f"(same ~20 steps, range collapsed to empty)")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Single-element list
    # - Value not present
    # - Value at the first position
    # - Value at the last position
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")

    # Edge case 1: Empty list
    print("\nEdge case 1 — Empty list:")
    empty = []
    print(f"  Linear search  on []: {linear_search(empty, 42)}")
    print(f"  Binary search  on []: {binary_search(empty, 42)}")
    # Linear: the for loop does not execute → returns -1 immediately.
    # Binary: high = len([]) - 1 = -1; while (0 <= -1) is False → returns -1.
    # Both handle empty input safely without exceptions.
    print("  Explanation: no elements to examine, both return -1 safely.")

    # Edge case 2: Single-element list — target found
    print("\nEdge case 2 — Single-element list, target present:")
    single = [1042]
    print(f"  Dataset: {single}")
    print(f"  Linear search for 1042: {linear_search(single, 1042)}")
    print(f"  Binary search for 1042: {binary_search(single, 1042)}")
    # Both check exactly one element and return index 0 immediately.
    print("  Explanation: one comparison, both algorithms agree: index 0.")

    # Edge case 3: Single-element list — target missing
    print("\nEdge case 3 — Single-element list, target absent:")
    print(f"  Linear search for 9999: {linear_search(single, 9999)}")
    print(f"  Binary search for 9999: {binary_search(single, 9999)}")
    # Linear: one comparison fails → returns -1.
    # Binary: mid = 0; 1042 < 9999 → low = 1; now low > high → returns -1.
    print("  Explanation: one comparison confirms absence, both return -1.")

    # Edge case 4: Target at the first position (best case for linear)
    print("\nEdge case 4 — Target at index 0 (first element):")
    data = [1003, 1012, 1025, 1041, 1058]
    print(f"  Dataset: {data}")
    print(f"  Linear search for 1003: {linear_search(data, 1003)}")
    print(f"  Binary search for 1003: {binary_search(data, 1003)}")
    # Linear: match on the very first comparison → O(1) best case.
    # Binary: mid = 2 → 1025 > 1003 → high = 1 → mid = 0 → found. 2 steps.
    print("  Explanation: linear search is O(1) at position 0 (best case).")
    print("               Binary search still needs ~2 comparisons.")

    # Edge case 5: Target at the last position (worst case for linear)
    print("\nEdge case 5 — Target at the last position (worst case for linear):")
    print(f"  Dataset: {data}")
    print(f"  Linear search for 1058: {linear_search(data, 1058)}")
    print(f"  Binary search for 1058: {binary_search(data, 1058)}")
    # Linear: must check all 5 elements before finding the last one → O(n) worst case.
    # Binary: mid=2→low=3→mid=4→found. Only 2 comparisons.
    print("  Explanation: linear search checks every element before the last.")
    print("               Binary search still needs only ~2 comparisons.")


if __name__ == "__main__":
    main()
