#include<iostream>
#include<algorithm>
using namespace std;
void solve(){
    long long  n;
    int count2=0;
    int count3=0;
    cin>>n;
    while(n%2==0){
        count2++;
        n/=2;
    }
    while(n%3==0){
        count3++;
        n/=3;
    }
if(n!=1||count2>count3)
    cout<<"-1"<<endl;
else
    cout<<(2*count3-count2)<<endl;
}
int main(){
    int t;
    cin>>t;
    while(t--){
        solve();
        
    }
    return 0;
}