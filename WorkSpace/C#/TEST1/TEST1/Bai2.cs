using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Cau_truc_lenh_co_ban
{
    internal class Bai2
    {
        int SumPrimeInMatrix(int[][] a)
        {
            int sum = 0;
            for (int i = 0; i < a.Length; i++)
            {
                for (int j = 0; j < a[i].Length; j++)
                {
                    if (CheckPrime(a[i][j])) sum += a[i][j]; 
                }
            }

            return sum;

        }


        bool CheckPrime(int n)
        {
            if (n < 2) return false;
            if (n == 2) return true;
            if (n > 2)
            {
                for (int i = 2; i <= Math.Sqrt(n); i++)
                {
                    if (n % i == 0) return false;
                }
            }
            return true;
        }
    }


}
