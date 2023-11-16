using System;

namespace Event
{
    public delegate void SuKienNhapSo(int x);


    //Publisher
    class UserInput
    {
        public SuKienNhapSo sukiennhapso { get; set; }
        public void Input()
        {
            do
            {   
                Console.WriteLine("Nhap so: ");
                string s = Console.ReadLine();
                int i = Int32.Parse(s);
                sukiennhapso?.Invoke(i);
            } while (true);
        }
    }



    class TinhCan
    {
        public void Sub(UserInput input)
        {
            input.sukiennhapso = Can;
        }
        public void Can(int i)
        {
            Console.WriteLine($"Can bac 2 cua so {i} la {Math.Sqrt(i)}");
        }
    }

    class program
    {
        static void Main(string[] args)
        {
            UserInput userinput = new UserInput();
            TinhCan tinhcan = new TinhCan();
            tinhcan.Sub(userinput);



            userinput.Input();

        }
    }
}
