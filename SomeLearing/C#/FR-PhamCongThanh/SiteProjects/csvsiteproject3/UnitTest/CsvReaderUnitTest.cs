using SiteProjectWeek3.CsvLib;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace SiteProjectWeek3.UnitTest
{
    class CsvReaderUnitTest
    {
        #region TestReadFromFile

        public static string FileTest = DataTest.FileTest;
        public static bool TC_CsvReader_ReadFromFile_TestSuccess()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromFile(FileTest);
                return lines.Count() == 3;
            }
            catch
            {
                return false;
            }
        }
        public static bool TC_CsvReader_ReadFromFile_TestFileNotFound()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromFile(Guid.NewGuid().ToString());
                return lines.Count() == 0;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromFile_TestTrimDataTrue()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromFile(FileTest);
                return lines[2].Values[2].ToString() == lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromFile_TestTrimDataFalse()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = false;
                var lines = csvReader.ReadFromFile(FileTest);
                return lines[2].Values[2].ToString() != lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromFile_TestSkipLineCallback()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.ReadFromFile(FileTest);
                return line.Count < 10;
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromFile_TestEventSkippedLine()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.SkippedLine += (lineIndex) =>
                {
                    line.Add(lineIndex);
                };
                csvReader.ReadFromFile(FileTest);
                return line.Count > 0;
            }
            catch
            {
                return false;
            }
        }

        #endregion

        #region Test ReadFromCsvContent

        public static bool TC_CsvReader_ReadFromCsvContent_TestSuccess()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromString(DataTest.CsvContent);
                return lines.Count() == 3;
            }
            catch
            {
                return false;
            }
        }
        public static bool TC_CsvReader_ReadFromCsvContent_TestFileArgumentNull()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromString(null);
                return lines.Count() == 0;
            }         
            catch (Exception)
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromCsvContent_TestTrimDataTrue()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromString(DataTest.CsvContent);
                return lines[2].Values[2].ToString() == lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromCsvContent_TestTrimDataFalse()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = false;
                var lines = csvReader.ReadFromString(DataTest.CsvContent);
                return lines[2].Values[2].ToString() != lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromCsvContent_TestSkipLineCallback()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.ReadFromString(DataTest.CsvContent);
                return line.Count < 10;
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromCsvContent_TestEventSkippedLine()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.SkippedLine += (lineIndex) =>
                {
                    line.Add(lineIndex);
                };
                csvReader.ReadFromString(DataTest.CsvContent);
                return line.Count > 0;
            }
            catch
            {
                return false;
            }
        }

        #endregion

        #region Test ReadFromStream

        public static bool TC_CsvReader_ReadFromStream_TestSuccess()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromStream(DataTest.Stream);
                return lines.Count() == 3;
            }
            catch
            {
                return false;
            }
        }
        public static bool TC_CsvReader_ReadFromStream_TestArgumentNull()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromStream(null);
                return lines.Count() == 0;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromStream_TestTrimDataTrue()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = true;
                var lines = csvReader.ReadFromStream(DataTest.Stream);
                return lines[2].Values[2].ToString() == lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromStream_TestTrimDataFalse()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                csvReader.Configuration.TrimData = false;
                var lines = csvReader.ReadFromStream(DataTest.Stream);
                return lines[2].Values[2].ToString() != lines[2].Values[2].ToString().Trim();
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromStream_TestSkipLineCallback()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.ReadFromStream(DataTest.Stream);
                return line.Count < 10;
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CsvReader_ReadFromStream_TestEventSkippedLine()
        {
            try
            {
                CsvReader csvReader = new CsvReader();
                IList<int> line = new List<int>();
                csvReader.SkippedLine += (lineIndex) =>
                {
                    line.Add(lineIndex);
                };
                csvReader.ReadFromStream(DataTest.Stream);
                return line.Count > 0;
            }
            catch
            {
                return false;
            }
        }

        #endregion
    }
}
