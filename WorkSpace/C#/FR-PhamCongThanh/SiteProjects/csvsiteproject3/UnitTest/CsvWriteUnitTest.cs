using SiteProjectWeek3.CsvLib;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace SiteProjectWeek3.UnitTest
{
    class CsvWriteUnitTest
    {
        public static bool TC_CsvWriter_WriteToFile_TestSuccess()
        {
            try
            {
                CsvWriter csvWriter = new CsvWriter();
                return csvWriter.WriteToFile(DataTest.FileTest, DataTest.GeneratorCsvLine());
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
                return !csvWriter.WriteToFile(DataTest.FileTest, null);
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
        public static string FileTest = "test.csv";
        public static string CsvContent;

        public static Stream Stream
        {
            get
            {
                byte[] byteArray = Encoding.UTF8.GetBytes(DataTest.CsvContent);
                return new MemoryStream(byteArray);
            }
        }

        public static ICsvLine[] GeneratorCsvLine()
        {
            IList<MockCsvLine> writeLines = new List<MockCsvLine>();

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
                    writeLines.Add(new MockCsvLine() { Values = Values });
                }
                else
                {
                    writeLines.Add(new MockCsvLine() { Values = new string[1] });
                }
            }

            CsvContent = string.Join(Environment.NewLine, writeLines.Select(l => l.ToString()));
            return writeLines.ToArray();
        }

        class MockCsvLine : ICsvLine
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
