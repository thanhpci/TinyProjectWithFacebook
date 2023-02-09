using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Cau_truc_lenh_co_ban
{

    internal class Program
    {
        static long CalcNumSum(int[] arr)
        {
            int result = 0;
            for (int i = 0; i < arr.Length; i++)
            {
                if (check(arr[i], arr, i)) result++;
            }
            return result;
        }

        static bool check(int n, int[] arr, int k)
        {
            for (int i = 0; i < arr.Length; i++)
            {
                if (i == k) continue;
                for (int j = 0; j < arr.Length; j++)
                {
                    if (j == k || j == i) continue;
                    if (n == arr[i] + arr[j]) return true;
                }
            }
            return false;
        }

        static void Main(string[] args)
        {
            int[] Array = { 1, 3, 5, 7, 8, 12, 15 };
            Console.WriteLine(value: CalcNumSum(Array));
            Console.ReadKey();
        }
    }
}
