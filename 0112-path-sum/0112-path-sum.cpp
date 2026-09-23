class Solution {
public:

    bool solve(TreeNode* curr, int targetSum, int sum) {

        while(curr != NULL) {

            sum += curr->val;

            
            if(curr->left == NULL && curr->right == NULL) {
                if(sum == targetSum)
                    return true;

                return false;
            }

            if(solve(curr->left, targetSum, sum))
                return true;

            curr = curr->right;
        }

        return false;
    }

    bool hasPathSum(TreeNode* root, int targetSum) {

        int sum = 0;

        return solve(root, targetSum, sum);
    }
};