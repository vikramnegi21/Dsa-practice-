class Solution {
public:
    int maxNumberOfFamilies(int n, vector<vector<int>>& reservedSeats) {
        unordered_map<int,unordered_set<int>>mp;
        for(auto&s: reservedSeats){

            int row=s[0];
            int seat=s[1];
            mp[row].insert(seat);
        }
         int result=(n-mp.size())*2;
         for(auto &[row,bookedseats]:mp){
            auto isAvaliable=[&](int seat){
                return bookedseats.find(seat)==bookedseats.end();
            };
            bool groupA =isAvaliable(2)&&isAvaliable(3)&&isAvaliable(4)&&isAvaliable(5);
             bool groupB =isAvaliable(4)&&isAvaliable(5)&&isAvaliable(6)&&isAvaliable(7);
              bool groupC =isAvaliable(6)&&isAvaliable(7)&&isAvaliable(8)&&isAvaliable(9);
              if(groupA &&groupC){
                result+=2;
              }
              else if(groupA ||groupB||groupC){
                result+=1;
              }
              else{
                result+=0;
              }
              

         }
         return result;
    }
};