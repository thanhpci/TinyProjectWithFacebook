using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Cau_truc_lenh_co_ban
{
    internal class Bai5
    {
        int SumOfLongestArithmeticSequence(int[] sequence)
        {
            int maxSum = 0;
            for (int i = 0; i < sequence.Length - 2; i++)
            {
                for (int j = i + 1; j < sequence.Length; j++)
                {
                    int distance = sequence[j] - sequence[i];
                    int currentSum = SumOfArithmeticSequence(sequence[i], i, distance, sequence);
                    if (currentSum > maxSum) maxSum = currentSum;
                }
            }

            return maxSum;
        }

        int SumOfArithmeticSequence(int firstNumber, int index, int distance, int [] arr)
        {
            int count = 1;
            int sum = firstNumber;

            for (int i = index + 1; i < arr.Length; i++)
            {
                if (distance != 0 && (arr[i] == arr[i - 1])) continue;
                if ((arr[i] - firstNumber) % distance == 0)
                {
                    count++;
                    sum += arr[i];
                }
            }

            if (count < 3) return 0;
            return sum;
        }


            
       

      
    }
}
