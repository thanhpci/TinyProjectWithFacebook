using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Cau_truc_lenh_co_ban
{

    
    internal class Bai3
    {
        bool PalindromeString(string s)
        {
            double length = s.Length;

            for (int i = 0; i < length / 2; i++)
            {
                if (!s[i].Equals(s[s.Length - 1 - i]))
                {
                    return false;
                }
            }

            return true;
        }
    }
}
