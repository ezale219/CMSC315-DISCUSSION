# Unit 4 Discussion: Binary Search Trees

## Overview

This assignment introduced Binary Search Trees (BSTs) and recursive tree operations through an employee record lookup system. Employee IDs were organized in a BST so that insertion, search, and sorted retrieval could be performed efficiently using the BST's left-smaller / right-larger ordering property.

## Learning Objectives

- Built a BST with recursive insertion and search
- Implemented in-order traversal to produce sorted output
- Demonstrated edge cases including empty trees, duplicate insertion, and sequential (degenerate) insertion
- Analyzed the performance difference between balanced and skewed BSTs

## What Was Implemented

### Node Class
Each `Node` stored a value and references to a left child and a right child, both initialized to `None`. Left children held smaller values; right children held larger values.

### BST.insert / _insert_recursive
Insertion compared the new value to each node encountered on the path from the root. Smaller values were directed left; larger values were directed right. When an empty position was found, a new `Node` was placed there. Duplicate values were silently ignored to preserve the BST ordering property.

### BST.search / _search_recursive
Search used the same left-smaller / right-larger rule to navigate the tree. At each node, one entire subtree was eliminated from consideration. In a balanced BST this gives O(log n) performance, compared to O(n) for a linear list scan.

### BST.inorder / _inorder_recursive
In-order traversal visited nodes in LEFT → CURRENT → RIGHT order. Because the BST property guarantees that smaller values are always to the left and larger values always to the right, this visitation order produces the entire sequence in ascending sorted order without any additional sort step.

### Edge Cases Demonstrated
- **Empty tree**: search and in-order on a tree with no root both returned safe defaults (False and []).
- **Duplicate insertion**: inserting a value already in the tree was silently ignored, leaving the tree unchanged.
- **Sequential insertion**: inserting IDs in ascending order (1001, 1002, 1003 …) produced a right-skewed chain identical to a linked list, degrading search to O(n).

## Tree Structure

Employee IDs were inserted starting from a middle value (1050) to distribute nodes across both subtrees:

```
              1050
           /        \
        1025          1075
       /    \        /    \
    1010    1040  1060    1090
    /    \      \
 1005  1015    1030
```

In-order traversal result: `[1005, 1010, 1015, 1025, 1030, 1040, 1050, 1060, 1075, 1090]`

## How to Run

```bash
python unit4_discussion.py
```

---

## Discussion Board Reflection

After completing the programming assignment, add this reflection to your initial discussion post in LEO.

Your reflection should be approximately 150–200 words and address the following questions:

1. What concepts or skills did you learn while completing this assignment?

Completing this assignment deepened my understanding of how the BST ordering property — smaller values left, larger values right — creates a structure where every comparison at a node eliminates one entire subtree from the search. Writing the recursive insertion and search methods made this concrete: each recursive call works on a strictly smaller subproblem, and the base cases (null node, value found) terminate the recursion cleanly. I also learned that in-order traversal produces sorted output for free in a BST, without requiring a separate sort — a consequence of the same ordering property that makes search efficient.

2. What challenges did you encounter, and how did you overcome them?

The hardest part was reasoning about the degenerate case. Inserting values in sequential order (1001, 1002, 1003…) produces a right-leaning chain that looks like a linked list — every new node becomes the right child of the previous one, and search degrades to O(n). Visualizing the resulting tree structure made the problem clear and motivated the solution: starting insertion from a middle value (1050) ensures that roughly half the subsequent values go left and half go right, keeping the tree balanced.

3. Explain BST behavior and compare to how ordering works to create efficiency as compared to other data structures.

A BST achieves O(log n) search on a balanced tree because each comparison at a node halves the remaining search space. A flat list offers O(n) linear search because there is no ordering structure to exploit — every element must be checked in the worst case. A sorted array offers O(log n) binary search, which matches BST search performance, but requires O(n) time to insert a new element (shifting elements to maintain order). A BST achieves O(log n) for both search AND insertion on a balanced tree, making it superior to a sorted array for workloads that mix frequent insertions with frequent searches. The tradeoff is that a BST can degrade to O(n) when insertions arrive in sorted order, producing a skewed tree — a problem that self-balancing variants such as AVL and Red-Black trees address automatically.
