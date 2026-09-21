#include<iostream>
#include<algorithm>
#include<vector>
#include<string>
using namespace std;
int main(){
int t;
cin>>t;
while(t--){
    
    int n ;
    cin>>n;
    string s;
    cin>>s;
 
 
int minl=1;
int currl=1;
 
for(int i=1;i<n;i++){
    if(s[i]==s[i-1]){
        currl++;
        
    }
    else{
        currl=1;
    }
    minl=max(minl,currl);
}
cout<<minl+1<<"
";
 
}
 
 
 
 
 
    return 0;
    
}