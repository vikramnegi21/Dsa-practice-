// LeetCode 237: Delete Node in a Linked List

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 * };
 */

class Solution {
public:
    void deleteNode(ListNode* node) {
        // Copy next node's value into current node
        node->val = node->next->val;

        // Skip the next node
        node->next = node->next->next;
    }
};
