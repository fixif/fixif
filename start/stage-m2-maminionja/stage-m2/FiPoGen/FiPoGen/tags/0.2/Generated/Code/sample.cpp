#include <iostream>
#include <iomanip>
#include <fstream>
#include "ac_fixed.h"

using namespace std;

float RandomFloat(int beta)
{
    float a = pow(2,beta-2)+1;
    float b = pow(2,beta-1)-1;
    float random = ((float) rand()) / (float) RAND_MAX;
    float diff = b - a;
    float r = random * diff;
    return (pow(-1,rand()%2))*(a + r);
}


int main()
{
    srand ( time(NULL) );
    ofstream fichier("test.txt", ios::out | ios::trunc);
    if(fichier)
    {
        //Dec_Float
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;
		fichier<<setprecision(10)<<RandomFloat(16)<<endl;

        fichier.close();
    }
    else
        cerr << "Impossible d'ouvrir le fichier !" << endl;
    return 0;
}
