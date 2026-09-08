"""
=========================================================
UNIT 4 DISCUSSION: BINARY SEARCH TREES (BST)
=========================================================

INSTRUCTIONS:
This assignment focuses on understanding and implementing a
Binary Search Tree (BST).

You will complete and modify the provided code while explaining
key concepts in your own words using comments and output.

Application scenario: Employee Record Lookup System
Employee IDs are stored in a BST so that search, insertion,
and sorted retrieval can be performed more efficiently than
with a flat list or sequential scan.
"""


class Node:
    def __init__(self, value):
        # TODO (Student):
        # Store the node's value and initialize references
        # to the left and right child nodes.

        # Store the employee ID (or any comparable value) at this node.
        self.value = value

        # Left child holds values SMALLER than this node's value.
        # Initialized to None because a new node has no children yet.
        self.left = None

        # Right child holds values LARGER than this node's value.
        # Initialized to None for the same reason.
        self.right = None


class BST:
    def __init__(self):
        # TODO (Student):
        # Initialize an empty Binary Search Tree.

        # The root is None when the tree is first created (empty tree).
        # All insertions will update this reference as the tree grows.
        self.root = None

    def insert(self, value):
        """
        TODO (Student):
        Insert a value into the BST.

        Requirements:
        - Use the recursive helper method.
        - Add comments explaining why insertion depends on
          whether a value is smaller or larger than the
          current node.

        BST insertion works by comparing the new value to each node
        encountered on the way down the tree:
          - Smaller  → go LEFT  (left subtree holds smaller values)
          - Larger   → go RIGHT (right subtree holds larger values)
          - Equal    → ignore   (duplicates are silently skipped to
                                 preserve the BST ordering property)
        This comparison at each step keeps the tree organized and is
        what makes future searches efficient.
        """
        if self.root is None:
            # Tree is empty — the new value becomes the root node.
            self.root = Node(value)
        else:
            # Tree is non-empty — delegate to recursive helper
            # starting from the root.
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST insertion.

        Requirements:
        - Create a new node when a position is found.
        - Insert smaller values into the left subtree.
        - Insert larger values into the right subtree.
        - Return the updated node reference.

        At each recursive call, one comparison eliminates either
        the left or the right subtree from consideration.
        This is why insertion runs in O(log n) on a balanced tree.
        """
        if value < node.value:
            # New value is smaller → it belongs in the left subtree.
            if node.left is None:
                # Found an empty slot — place the new node here.
                node.left = Node(value)
            else:
                # Left child exists — recurse deeper into the left subtree.
                self._insert_recursive(node.left, value)
        elif value > node.value:
            # New value is larger → it belongs in the right subtree.
            if node.right is None:
                # Found an empty slot — place the new node here.
                node.right = Node(value)
            else:
                # Right child exists — recurse deeper into the right subtree.
                self._insert_recursive(node.right, value)
        else:
            # value == node.value → duplicate detected.
            # Duplicates are silently ignored to preserve BST ordering.
            # Allowing duplicates would require an additional rule
            # (e.g., always go right) and complicate search logic.
            pass

        return node

    def search(self, value):
        """
        TODO (Student):
        Search for a value in the BST.

        Requirements:
        - Return True if found.
        - Return False if not found.
        - Add comments explaining why BST search is often
          more efficient than linear search.

        BST search efficiency:
        At each node, the comparison eliminates one entire subtree.
        In a balanced BST with n nodes, this halves the remaining
        search space at every step — giving O(log n) performance,
        the same as binary search on a sorted array, but without
        the need to shift elements on insert/delete.

        Compare this to a plain list: a linear search must examine
        every element in the worst case — O(n).
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST search.

        Base case 1: node is None — we have gone past a leaf,
                     so the value is not in the tree → return False.
        Base case 2: node.value matches — value found → return True.
        Recursive case: compare and descend into the appropriate subtree.
        """
        # Base case 1: reached a null position — value is absent.
        if node is None:
            return False

        # Base case 2: current node holds the target value.
        if value == node.value:
            return True

        # Recursive case: BST ordering tells us exactly which subtree to search.
        if value < node.value:
            # Target is smaller — can only exist in the left subtree.
            return self._search_recursive(node.left, value)
        else:
            # Target is larger — can only exist in the right subtree.
            return self._search_recursive(node.right, value)

    def inorder(self):
        """
        TODO (Student):
        Return a list containing the values from an
        in-order traversal.
        """
        values = []
        self._inorder_recursive(self.root, values)
        return values

    def _inorder_recursive(self, node, values):
        """
        TODO (Student):
        Implement in-order traversal.

        Requirements:
        - Visit the left subtree.
        - Visit the current node.
        - Visit the right subtree.
        - Add comments explaining why this traversal
          produces sorted output in a BST.

        Why in-order traversal produces sorted output:
        The BST property guarantees that every value in the LEFT
        subtree is SMALLER than the current node, and every value
        in the RIGHT subtree is LARGER.

        By visiting left → current → right, we always process
        smaller values before the current node, and the current
        node before larger values.  Applying this rule recursively
        at every node produces the entire sequence in ascending order.
        This property makes in-order traversal the natural way to
        produce a sorted listing from a BST without any additional
        sorting algorithm.
        """
        if node is None:
            # Base case: reached a null node — nothing to visit.
            return

        # Step 1: Recurse into the LEFT subtree (smaller values first).
        self._inorder_recursive(node.left, values)

        # Step 2: Visit the CURRENT node (middle value).
        values.append(node.value)

        # Step 3: Recurse into the RIGHT subtree (larger values last).
        self._inorder_recursive(node.right, values)


def main():
    print("=== UNIT 4: BINARY SEARCH TREES ===")

    # ===============================
    # TODO (Student): BUILD A TREE
    # ===============================
    #
    # Requirements:
    # 1. Create a BST object.
    # 2. Insert at least 7 values.
    # 3. Include values that go into both left
    #    and right subtrees.
    # 4. Display the values inserted.
    # 5. Use comments to explain why a BST is efficient at reducing search space for each step.

    print("\n=== TREE CONSTRUCTION ===")

    # Create the employee record BST.
    # Employee IDs are used as keys. The root (1050) represents a middle
    # value so that insertions flow into both left and right subtrees,
    # producing a roughly balanced tree rather than a degenerate chain.
    bst = BST()

    # Inserting in this order deliberately avoids a sequential pattern.
    # Starting with 1050 (a middle value) ensures that lower IDs go left
    # and higher IDs go right, distributing the tree evenly.
    employee_ids = [1050, 1025, 1075, 1010, 1040, 1060, 1090, 1005, 1015, 1030]

    print("Inserting employee IDs:")
    for eid in employee_ids:
        bst.insert(eid)
        print(f"  Inserted {eid}")

    # Resulting tree structure (approximate):
    #
    #              1050          ← root
    #           /        \
    #        1025          1075
    #       /    \        /    \
    #    1010    1040  1060    1090
    #    /    \      \
    # 1005  1015    1030
    #
    # Each level halves the remaining search space, giving O(log n) search.

    # ===============================
    # TODO (Student): IN-ORDER TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Perform an in-order traversal.
    # 2. Display the traversal results.
    # 3. Use comments to explain why the traversal produces
    #    sorted output in a BST.

    print("\n=== IN-ORDER TRAVERSAL ===")

    sorted_ids = bst.inorder()

    # In-order traversal visits LEFT → CURRENT → RIGHT at every node.
    # Because the BST property guarantees smaller values are always to
    # the left and larger values always to the right, this order of
    # visitation produces the entire sequence in ascending sorted order
    # without any additional sorting step.
    print(f"In-order result (sorted): {sorted_ids}")
    print("Observation: In-order traversal always produces sorted output")
    print("             because BST structure enforces left < root < right.")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for at least two values that exist.
    # 2. Search for at least two values that do not exist.
    # 3. Use comments to clearly explain the results.

    print("\n=== SEARCH TESTS ===")

    # Search for IDs that ARE in the tree.
    # Each search starts at the root and follows the BST ordering rule:
    # go left if smaller, go right if larger.
    # At each step, one entire subtree is eliminated, giving O(log n) performance.
    found_tests = [1040, 1090]
    for eid in found_tests:
        result = bst.search(eid)
        print(f"  Search {eid}: {'FOUND' if result else 'NOT FOUND'}")

    # Search for IDs that are NOT in the tree.
    # The search will follow the BST path until it reaches a None node,
    # at which point it returns False without scanning the entire tree.
    missing_tests = [1055, 1100]
    for eid in missing_tests:
        result = bst.search(eid)
        print(f"  Search {eid}: {'FOUND' if result else 'NOT FOUND'}")

    print("Note: BST search eliminates one subtree at each node,")
    print("      making it O(log n) on a balanced tree vs O(n) for a list.")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least one edge case.
    #
    # Example ideas:
    # - Traverse an empty tree
    # - Search an empty tree
    # - Insert duplicate values
    # - Create a tree with only one node
    #
    # Use comments to explain what happens and why.

    print("\n=== EDGE CASES ===")

    # Edge case 1: Empty tree — search and traversal on an empty BST.
    empty_bst = BST()
    print("Edge case 1 — Empty tree:")
    print(f"  Search 1050 in empty tree: {empty_bst.search(1050)}")
    print(f"  In-order of empty tree:    {empty_bst.inorder()}")
    # When root is None, _search_recursive immediately returns False
    # and _inorder_recursive immediately returns without appending anything.
    print("  Explanation: root is None, so both operations hit the base")
    print("               case immediately and return safe default values.")

    # Edge case 2: Duplicate insertion.
    print("\nEdge case 2 — Duplicate insertion:")
    bst.insert(1050)   # 1050 is already the root
    bst.insert(1040)   # 1040 is already in the tree
    print(f"  After inserting duplicates 1050 and 1040, size via in-order: "
          f"{len(bst.inorder())} elements")
    print(f"  In-order (unchanged): {bst.inorder()}")
    # Duplicates are silently ignored in _insert_recursive (the else: pass branch).
    # This preserves the BST ordering property — allowing duplicates would
    # require an extra rule for every search and traversal operation.
    print("  Explanation: BST insertion ignores duplicates to keep the")
    print("               ordering property unambiguous.")

    # Edge case 3: Sequential insertion (degenerate / skewed tree).
    print("\nEdge case 3 — Sequential insertion (skewed tree):")
    skewed_bst = BST()
    sequential_ids = [1001, 1002, 1003, 1004, 1005]
    for eid in sequential_ids:
        skewed_bst.insert(eid)
    print(f"  Inserted in order: {sequential_ids}")
    print(f"  In-order result:   {skewed_bst.inorder()}")
    print("  Explanation: inserting IDs in ascending order causes every new")
    print("               node to go to the RIGHT of the previous one, forming")
    print("               a chain identical to a linked list. Search becomes")
    print("               O(n) in the worst case instead of O(log n).")
    print("  Solution: insert starting from a middle value or use a self-")
    print("            balancing tree (AVL or Red-Black) to maintain O(log n).")


if __name__ == "__main__":
    main()
