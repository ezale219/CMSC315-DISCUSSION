# Unit 3 Discussion: List Operations (Insert, Delete, Search)

## Overview

This assignment examined how Python lists behave when elements are inserted, removed, and
searched, with particular attention to element shifting and how operation cost changes depending
on **where** in the list the operation happens.

Three functions were completed in `unit3_lists.py` — `insert_at()`, `delete_at()`, and
`search_value()` — and demonstrated through a deployment runbook scenario in which the order of
elements carries real meaning.

## How to Run

```bash
python unit3_lists.py
```

No external packages were required.

## Application Scenario

A deployment runbook was used as the working example: an ordered list of the steps an engineer
follows to push a release. Order is the entire point of the structure, since step 3 must run
after step 2. That made the shifting behavior meaningful rather than abstract — inserting a
forgotten security scan in the middle had to push every later step down by one position, and
deleting a step had to pull the rest back up, because a runbook with a gap or an overwritten
step would be wrong.

## What Was Implemented

### `insert_at(lst, index, value)`

A Python list holds its elements in one contiguous block of references, so insertion never
overwrites. The element already at the target index, and every element after it, was shifted one
slot to the right to open a gap, and each of those elements received a new index.

The cost was driven by how many elements had to move, which is `(n - index)`:

| Insertion point | Elements shifted | Cost |
|---|---|---|
| Beginning (index 0) | all `n` | O(n) — worst case |
| Middle | about `n/2` | O(n) |
| End | none | O(1) amortized |

"Amortized" applies at the end because the list occasionally grows its underlying block and
copies everything once; that one-time cost spreads across many cheap appends.

### `delete_at(lst, index)`

Deletion was implemented as the mirror image of insertion — removing position `i` closed the gap
by shifting every later element one slot to the **left**, decreasing their indexes by one.

Two guards were added before any removal took place:

1. An empty list was rejected outright, since it has no valid index at all.
2. Negative indexes and indexes at or past the length were rejected, returning `None`.

Index validation mattered because index values typically originate outside the function's
control — user input, a search result, a loop counter — so an invalid index is a normal runtime
possibility rather than a rare bug. Without the guard, `lst.pop(99)` would raise `IndexError` and
terminate the program.

Negatives were treated as invalid deliberately. Python reads `-1` as "last element", so a stray
negative would have silently deleted from the end rather than signalling a problem, which is
almost never what a caller who passed a bad index intended.

### `search_value(lst, value)`

A linear search was implemented: the function walked the list one position at a time from index 0
and compared each element to the target, returning the first matching index or `-1` if the value
was absent.

The scan had to be sequential because an unsorted list carries no information about where a value
might be. Finding `"Build artifact"` at index 2 says nothing about whether another target sits at
index 3 or index 900, so no position could be ruled out without being examined. Binary search can
discard half the list per comparison only because a sorted list guarantees which half the target
must occupy; without that ordering guarantee, every element remained a candidate until checked.

| Case | Comparisons | Cost |
|---|---|---|
| Target at index 0 | 1 | O(1) |
| Target in the middle | about `n/2` | O(n) |
| Target absent | `n` | O(n) — always the worst case |

A miss was always the worst case, since absence can only be proven by exhausting the list.

## Demonstrations Completed

**Insertion.** A four-step runbook was created and displayed, then insertions were performed at
the beginning, the middle, and the end, with the list displayed after each and the number of
shifted elements explained.

**Deletion.** Steps were removed from the beginning, the middle, and the end. Each removed value
was displayed alongside the updated list, showing the leftward shift closing the gap.

**Search.** Three searches were run: a value in the middle (stopped early at index 2), a value at
the front (best case, one comparison), and a value that did not exist (full scan, returned `-1`).

## Edge Cases Tested

| Case | Result |
|---|---|
| `delete_at()` with index 99 on a 4-item list | Returned `None`; list unchanged, no crash |
| `delete_at()` with index `-1` | Returned `None`; rejected rather than silently deleting the last item |
| `delete_at()` on an empty list | Returned `None`; no valid index exists at length 0 |
| `search_value()` on an empty list | Returned `-1` with zero comparisons; the loop never ran |
| `insert_at()` into an empty list | Value became index 0; nothing existed to shift |
| `insert_at()` with index 50 on a 1-item list | Value landed at index 1 — `list.insert()` **clamps** instead of raising |

That last case was the most interesting result. `list.insert()` and `list.pop()` disagree about
out-of-range indexes: `pop()` raises `IndexError`, while `insert()` silently clamps to the nearest
valid position. The value still enters the list, just not where the caller asked, which means a
bad index can pass through unnoticed.

## Reflection

The clearest lesson from this assignment was that a list operation has no single cost — the cost
depends on position. Inserting at the end shifts nothing and is effectively free, while inserting
at the front moves every element in the structure. Both are one line of code and look identical
in a diff, but on a large list one is instant and the other is the bottleneck. Writing the
shifting explanations into the comments forced me to think about what physically happens to the
underlying block rather than treating `insert()` and `pop()` as opaque built-ins.

The second lesson concerned validation. My first version of `delete_at()` only checked the upper
bound, which let a negative index through — and Python happily interpreted `-1` as the last
element and deleted it. Nothing raised, nothing looked wrong, and the list was quietly incorrect.
That was a better argument for defensive checks than any error message would have been, because
the failure was silent. Discovering that `insert()` clamps out-of-range indexes rather than
raising reinforced the same point: built-in behavior is not uniformly strict, so the boundaries
have to be defined by the code that wraps it.

The performance picture also explains why real applications lean on different structures.
Array-based lists are excellent at indexed access and appending, which suits a timeline, a
playlist, or a runbook that is mostly read and appended to. But queues that constantly remove
from the front, or structures needing frequent mid-sequence insertion, pay an O(n) shifting cost
every time — which is exactly the situation a linked list is built for, since it re-points a
reference instead of moving data.

## Files

* `unit3_lists.py` — completed implementation, demonstrations, and edge cases
* `README.md` — this documentation and reflection
