/**
 * 🚀 Odd Even Linked List (Optimal Approach)
 *
 * 💡 Approach:
 * - Hum 2 pointers use karte hain:
 *   1. odd  -> odd position nodes (1st, 3rd, 5th...)
 *   2. even -> even position nodes (2nd, 4th, 6th...)
 *
 * - evenHead ko store karte hain taaki end me even list ko attach kar sakein
 *
 * 🔄 Steps:
 * 1. odd = head, even = head->next
 * 2. odd ko next odd se connect karo
 * 3. even ko next even se connect karo
 * 4. End me odd list ke last node ko evenHead se connect kar do
 *
 * ⚡ Time Complexity: O(N)
 * ⚡ Space Complexity: O(1)
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode* oddEvenList(ListNode* head) {

        // Edge case: empty list ya sirf 1 node
        if(head == NULL || head->next == NULL)
            return head;

        // Step 1: Initialize pointers
        ListNode* odd = head;            // odd nodes track karega
        ListNode* even = head->next;     // even nodes track karega
        ListNode* evenHead = even;       // even list ka start save

        // Step 2: Traverse and rearrange
        while(even != NULL && even->next != NULL) {

            // odd ko next odd node se connect karo
            odd->next = even->next;
            odd = odd->next;

            // even ko next even node se connect karo
            even->next = odd->next;
            even = even->next;
        }

        // Step 3: even list ko odd ke end me attach karo
        odd->next = evenHead;

        // Final head return
        return head;
    }
};
