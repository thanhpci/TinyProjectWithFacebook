//program hello

using System;

class Program
{
    static void Main(string[] args)
    {
        con1 thanh = new con1();
        con2 minh = new con2();
        me bo = new me();

        
        if (thanh is con1) Console.WriteLine("true");
        else Console.WriteLine("false");
    }
}


class con1 : me
{
    int age = 1;
}

class con2 : me
{
    int age = 2;
}

class me
{
    int age = 4;
}
