using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek3.CsvLib
{
    internal class CsvWriter
    {
        //Read from an ICsvLine array then save it to a csv file.
        public bool WriteToFile(string filePath, ICsvLine[] lines)
        {
            try
            {
                if (lines == null)
                    return false;
                using (StreamWriter writer = new StreamWriter(filePath))
                {
                    foreach (ICsvLine line in lines)
                    {
                        writer.WriteLine(line.ToString());
                    }
                }
                return true;
            }
            catch
            {
                return false;
            }
        }

    }
}
