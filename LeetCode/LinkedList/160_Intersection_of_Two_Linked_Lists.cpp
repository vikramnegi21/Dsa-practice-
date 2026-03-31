/**
 * 🚀 Intersection of Two Linked Lists (Optimal Approach)
 *
 * 💡 Approach (Two Pointer Technique):
 * - Hum 2 pointers use karte hain:
 *   1. ptrA -> headA se start karega
 *   2. ptrB -> headB se start karega
 *
 * 🧠 Idea:
 * - Jab ptrA list A khatam karega, usko headB pe bhej do
 * - Jab ptrB list B khatam karega, usko headA pe bhej do
 *
 * - Isse dono pointers equal length traverse karenge:
 *   (lengthA + lengthB)
 *
 * - Agar intersection hoga:
 *   → dono pointers same node pe milenge
 *
 * - Agar intersection nahi hoga:
 *   → dono NULL pe milenge
 *
 * 🔄 Steps:
 * 1. ptrA = headA, ptrB = headB
 * 2. Jab tak ptrA != ptrB:
 *      - ptrA = (ptrA == NULL) ? headB : ptrA->next
 *      - ptrB = (ptrB == NULL) ? headA : ptrB->next
 * 3. Return ptrA (ya ptrB)
 *
 * ⚡ Time Complexity: O(N + M)
 * ⚡ Space Complexity: O(1)
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {

        // Edge case: agar koi list empty hai
        if(headA == NULL || headB == NULL)
            return NULL;

        // Step 1: initialize pointers
        ListNode* ptrA = headA;
        ListNode* ptrB = headB;

        // Step 2: traverse both lists
        while(ptrA != ptrB) {

            // agar A khatam ho gaya toh B se start karo
            ptrA = (ptrA == NULL) ? headB : ptrA->next;

            // agar B khatam ho gaya toh A se start karo
            ptrB = (ptrB == NULL) ? headA : ptrB->next;
        }

        // Step 3: ya toh intersection node milega ya NULL
        return ptrA;
    }
};
