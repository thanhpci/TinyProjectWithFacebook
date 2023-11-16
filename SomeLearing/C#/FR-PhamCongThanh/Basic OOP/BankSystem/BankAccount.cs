using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

//Class Bank Account
public class BankAccount
{
    private int id;
    private decimal balance;

    public BankAccount() {}


    public BankAccount(int id, decimal balance)
    {
        this.id = id;
        this.balance = balance;
    }

    public int Id
    {
        get { return this.id; }
        set { this.id = value; }
    }

    public decimal Balance
    {
        get { return this.balance; }
        set { this.balance = value; }
    }
    public void Deposit(decimal amount)
    {
        this.Balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount > this.Balance)
        {
            Console.WriteLine("Insufficient funds");
        } else {
            this.Balance -= amount;
        }

    }



    public override String ToString()
    {
        return $"Account ID: {this.Id}, Balance: {this.z:F2}"; 
    }

}