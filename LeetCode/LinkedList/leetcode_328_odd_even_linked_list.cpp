/**
 * LeetCode 328 - Odd Even Linked List
 *
 * Approach: Brute Force (Array Based)
 *
 * Steps:
 * 1. Convert Linked List into Array
 * 2. Store odd index elements and even index elements separately
 * 3. Merge both arrays (odd first, then even)
 * 4. Convert the final array back to Linked List
 *
 * Note:
 * - This is not the optimal solution (uses extra space O(n))
 * - Optimal solution (O(1) space using pointers) will be implemented later
 *
 * Status:
 * - Brute Force done today
 * - Optimal approach will be added tomorrow
 */

class Solution {
public:
    ListNode* oddEvenList(ListNode* head) {
        if(head == NULL) return NULL;

        vector<int> nums;

        // Linked List -> Array
        ListNode* temp = head;
        while(temp != NULL) {
            nums.push_back(temp->val);
            temp = temp->next;
        }

        vector<int> even, odd;

        int n = nums.size();

        // Separate indices
        for(int i = 0; i < n; i++) {
            if(i % 2 == 0) {
                even.push_back(nums[i]); // odd positions (1-based)
            } else {
                odd.push_back(nums[i]);
            }
        }

        vector<int> ans;

        // Merge
        for(int i = 0; i
