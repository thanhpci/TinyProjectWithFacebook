using System;
using System.Linq;
using System.Reflection;

namespace SiteProjectWeek2
{
    class Program
    {
        static void Main(string[] args)
        {
            RunAllTests();
            Console.ReadLine();
        }

        #region RunAllTests method

        public static void RunAllTests()
        {
            MethodInfo[] allTestCases = typeof(FileSystemUnitTest)
                                            .GetMethods()
                                            .Where(m => m.Name.StartsWith("TC_")).ToArray();

            Console.WriteLine("Unit Test result:");
            Console.WriteLine("-----------------------------------------------------");

            foreach (MethodInfo testCase in allTestCases)
            {
                bool isPassed = (bool)testCase.Invoke(null, null);
                WriteTestCaseResult(testCase.Name, isPassed);
            }

            Console.WriteLine("-----------------------------------------------------");
        }

        static void WriteTestCaseResult(string testCaseName, bool isPassed)
        {
            ConsoleColor color = Console.ForegroundColor;

            Console.Write($"{testCaseName}\t\t");

            if (isPassed)
            {
                Console.ForegroundColor = ConsoleColor.Blue;
                Console.WriteLine("Passed");
                Console.ForegroundColor = color;
            }
            else
            {

                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Failed");
                Console.ForegroundColor = color;
            }
        }

        #endregion RunAllTests method
    }
}
