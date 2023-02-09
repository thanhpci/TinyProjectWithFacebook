

using System;

namespace Delegate
{
    public delegate void ShowLog(string message);



    class Program
    {

        static void Info(string s) 
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine(s);
            Console.ResetColor();
        }

        static void Warning(string s) 
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine(s);
            Console.ResetColor();
        }
        

        static void tong(int a, int b, ShowLog showLog){
            int kq = a + b;
            showLog?.Invoke($"tong la {kq}");

        }
        static int hieu(int a, int b) => a-b;


        static void Main(string[] args)
        {
            tong(4, 5, Warning);

        }
    }
}