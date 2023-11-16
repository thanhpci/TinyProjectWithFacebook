namespace BankSystem
{
    internal class Program
    {
        static void Main(string[] args)
        {
            BankAccount tcb = new BankAccount(1, 555);

           Console.WriteLine(tcb.ToString);
        }
    }
}