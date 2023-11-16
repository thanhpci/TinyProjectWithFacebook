using System;
using System.IO;
using System.Linq;

namespace SiteProjectWeek4.CsvLib
{
    class CsvWriter
    {
        public bool WriteToFile(string filePath, ICsvLine[] lines)
        {
            try
            {
                string str = string.Join(Environment.NewLine, lines.Select(l => l.ToString()));
                File.WriteAllText(filePath, str);
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
