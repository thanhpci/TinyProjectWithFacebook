using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Cau_truc_lenh_co_ban
{
    internal class Bai4
    {
      



        bool CheckPasswordPolicy(string password)
        {
            if (password.Length < 6) return false;
            
            if (!checkOneUpper(password)) return false;

            if (!checkOneLower(password)) return false;

            if (!checkOneNumber(password)) return false;



            return true;
        }


        bool checkOneUpper(String password)
        {
            for (int i = 0; i < password.Length; i++)
            {
                int n = (int)password[i];
                if (n >= 65 && n <= 90) return true;
            }

            return false;

        }

        bool checkOneLower(String password)
        {
            for (int i = 0; i < password.Length; i++)
            {
                int n = (int)password[i];
                if (n >= 97 && n <= 122) return true;
            }

            return false;
        }

        bool checkOneNumber(String password)
        {
            for (int i = 0; i < password.Length; i++)
            {
                int n = (int)password[i];
                if (n >= 0 && n <= 9) return true;
            }

            return false;
        }



    }
}
