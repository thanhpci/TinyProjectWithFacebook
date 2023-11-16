using SiteProjectWeek4.Client.Entities;
using SiteProjectWeek4.Client.OrmMappers;
using SiteProjectWeek4.CsvLib;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace SiteProjectWeek4.UnitTest
{
    class CsvWriteUnitTest
    {
        public static bool TC_CsvWriter_WriteToFile_TestSuccess()
        {
            try
            {
                CsvWriter csvWriter = new CsvWriter();
                return csvWriter.WriteToFile(DataTest.FilePathTestWeek3, DataTest.WriteLines.ToArray());
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvWriter_WriteToFile_TestFalse()
        {
            try
            {
                CsvWriter csvWriter = new CsvWriter();
                return !csvWriter.WriteToFile(DataTest.FilePathTestWeek3, null);
            }
            catch
            {
                return false;
            }
        }
    }

    #region GeneratorCsvFile

    class DataTest
    {
        public static void GenerateDataTest()
        {
            GenerateDataTestWeek3();
            GenerateDataTestWeek4();
        }

        #region DatatestWeek3

        public static string FilePathTestWeek3 = "test.csv";
        public static string CsvContent { get; private set; }
        public static IList<MockCsvLine> WriteLines { get; private set; } = new List<MockCsvLine>();

        public static Stream Stream
        {
            get
            {
                byte[] byteArray = Encoding.UTF8.GetBytes(DataTest.CsvContent);
                return new MemoryStream(byteArray);
            }
        }

        private static void GenerateDataTestWeek3()
        {
            // GenerateDataTest
            for (int i = 0; i < 10; i++)
            {
                if (i % 2 == 0)
                {
                    string[] Values = new string[20];
                    for (int j = 0; j < 20; j++)
                    {
                        if (i % 4 == 0)
                        {
                            Values[j] = Guid.NewGuid() + " ";
                        }
                        else
                        {
                            Values[j] = Guid.NewGuid().ToString();
                        }

                    }
                    if (i % 3 == 0)
                    {
                        Values[0] = "#";
                    }
                    WriteLines.Add(new MockCsvLine() { Values = Values });
                }
                else
                {
                    WriteLines.Add(new MockCsvLine() { Values = new string[1] });
                }
            }

            CsvContent = string.Join(Environment.NewLine, WriteLines.Select(l => l.ToString()));

            // Write test
            File.WriteAllText(DataTest.FilePathTestWeek3, CsvContent);
        }

        #endregion

        #region DataTestWeek4

        public static string FilePathEmployee = "Employees.csv";
        public static string FilePathDepartment = "Departments.csv";

#if False
        public static List<Employee> Employees { get; private set; } = new List<Employee>();
        public static List<Department> Departments { get; private set; } = new List<Department>();

        private static void GenerateDataTestWeek4()
        {
            var random = new Random();
            for (int i = 0; i < 10; i++)
            {
                Departments.Add(new Department()
                {
                    DepartmentId = i,
                    Name = "Department " + i.ToString()
                });
                var item = random.Next(4, 10);
                for (int j = 0; j < 20; j++)
                {
                    Employees.Add(new Employee()
                    {
                        EmployeeId = j,
                        DepartmentId = i,
                        Name = "Employee Name " + j.ToString() + " of Department " + i.ToString(),
                        DateOfBirth = new DateTime(random.Next(1984, 1997), random.Next(1, 12), random.Next(1, 28))
                    });
                }
            }
        }
#endif
        public static string EmployeeCsvFile
        {
            get
            {
                return employeeCsvFile.ToString();
            }
        }
        public static string DepartmentCsvFile
        {
            get
            {
                return deepartmentCsvFile.ToString();
            }
        }

        private static StringBuilder employeeCsvFile { get;  set; } = new StringBuilder();
        private static StringBuilder deepartmentCsvFile { get;  set; } = new StringBuilder();     
        public static int NumberDepartmentValid { get; private set; }  
        public static int NumberEmployeeValid { get; private set; }

        private static void GenerateDataTestWeek4()
        {
            // GenerateDataTest
            var random = new Random();
            for (int i = 0; i <= 10; i++)
            {                   
                var departmentLine = i + ",Department " + i.ToString();
                NumberDepartmentValid++;
                deepartmentCsvFile.AppendLine(departmentLine);
                if (i % 2 == 0)
                {
                    var item = random.Next(4, 20);
                    for (int j = 0; j <= item; j++)
                    {
                        if (j % 2 == 0)
                        {
                            employeeCsvFile.AppendLine();
                        }
                        else
                        {
                            employeeCsvFile.AppendLine(j + "," + i + "," + "Employee Name " + j.ToString() + " of Department " + i.ToString() + "," +
                                new DateTime(random.Next(1984, 1997), random.Next(1, 12), random.Next(1, 28)).ToString("dd/MM/yyyy"));
                            NumberEmployeeValid++;
                        }
                    }
                }
            }

            // Write test
            File.WriteAllText(DataTest.FilePathEmployee, employeeCsvFile.ToString());
            File.WriteAllText(DataTest.FilePathDepartment, deepartmentCsvFile.ToString());
        }

        #endregion

        public class MockCsvLine : ICsvLine
        {
            public string[] Values { get; set; }

            public string Raw => throw new NotImplementedException();

            public override string ToString()
            {
                StringBuilder stringBuilder = new StringBuilder();
                for (int i = 0; i < Values.Length - 1; i++)
                {
                    stringBuilder.Append(Values[i]);
                    stringBuilder.Append(",");
                }
                stringBuilder.Append(Values[Values.Length - 1]);
                return stringBuilder.ToString();
            }
        }
    }

    #endregion
}
