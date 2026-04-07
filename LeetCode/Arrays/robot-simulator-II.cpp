/*
🔹 Problem: LeetCode 2069 - Robot Simulator II

🔹 Approach (Array / Precomputation)

1. Hum robot ke pure boundary path ko ek array (vector) me store karte hain.
   - Har element me {x, y, direction} store hota hai.
   - Direction encoding:
        0 = East, 1 = North, 2 = West, 3 = South

2. Boundary traversal order (clockwise):
   - Bottom row → East
   - Right column → North
   - Top row → West
   - Left column → South

3. Robot ko simulate karne ki jagah:
   - Hum ek index (idx) maintain karte hain
   - Move operation:
        idx = (idx + steps) % pos.size()
   - Isse circular movement handle ho jata hai

4. Special Case:
   - Starting point (0,0) ka direction South set karna padta hai
   - Aur jab tak move call nahi hota → direction East return karte hain

🔹 Time Complexity:
   - step(): O(1)
   - Space: O(perimeter)

🔹 Key Idea:
   - Simulation avoid karke circular array use kiya for efficient movement
*/

class Robot {
public:
    vector<vector<int>> pos; // {x, y, dir}
    int idx = 0;
    bool moved = false;

    Robot(int width, int height) {

        // Bottom row (East)
        for (int i = 0; i < width; i++) {
            pos.push_back({i, 0, 0});
        }

        // Right column (North)
        for (int i = 1; i < height; i++) {
            pos.push_back({width - 1, i, 1});
        }

        // Top row (West)
        for (int i = width - 2; i >= 0; i--) {
            pos.push_back({i, height - 1, 2});
        }

        // Left column (South)
        for (int i = height - 2; i > 0; i--) {
            pos.push_back({0, i, 3});
        }

        // Fix direction at (0,0)
        pos[0][2] = 3;

        idx = 0;
        moved = false;
    }

    void step(int num) {
        moved = true;
        idx = (idx + num) % pos.size();
    }

    vector<int> getPos() {
        return {pos[idx][0], pos[idx][1]};
    }

    string getDir() {
        if (!moved) return "East";

        int d = pos[idx][2];

        if (d == 0) return "East";
        else if (d == 1) return "North";
        else if (d == 2) return "West";
        return "South";
    }
};
