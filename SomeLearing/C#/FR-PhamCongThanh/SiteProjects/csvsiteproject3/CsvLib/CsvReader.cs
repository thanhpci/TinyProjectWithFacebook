using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using SiteProjectWeek3.CsvLib;
using static System.Net.WebRequestMethods;
using static SiteProjectWeek3.CsvLib.Delegates;

namespace SiteProjectWeek3.CsvLib
{
    internal class CsvReader
    {
        public CsvConfiguration Configuration = new CsvConfiguration();
        public SkippedLineEventHandler SkippedLine { get; set; }



        public ICsvLine[] ReadFromFile(string pathFile)
        {
            List<ICsvLine> lines = new List<ICsvLine>();
            string[] linesFile = System.IO.File.ReadAllLines(pathFile);
            foreach (string line in linesFile)
            {
                ICsvLine csvLine = new CsvLine();

                csvLine.Values = line.Split(',');
                //Trim spaces of each element of the array.
                if (Configuration.TrimData)
                {
                    for (int i = 0; i < csvLine.Values.Length; i++)
                    {
                        csvLine.Values[i] = csvLine.Values[i].Trim();
                    }
                }


                lines.Add(csvLine);
            }
            return lines.ToArray();
        }
        

        public ICsvLine[] ReadFromStream(Stream stream)
        {
            List<ICsvLine> lines = new List<ICsvLine>();
            string[] linesFile = System.IO.File.ReadAllLines(stream);
            foreach (string line in linesFile)
            {
                ICsvLine csvLine = new CsvLine();

                csvLine.Values = line.Split(',');
                //Trim spaces of each element of the array.
                if (Configuration.TrimData)
                {
                    for (int i = 0; i < csvLine.Values.Length; i++)
                    {
                        csvLine.Values[i] = csvLine.Values[i].Trim();
                    }
                }
            }
            return lines.ToArray();
        }


        public ICsvLine[] ReadFromString(string csvContent)
        {
            List<ICsvLine> lines = new List<ICsvLine>();
            string[] linesFile = csvContent.Split(Environment.NewLine);
            foreach (string line in linesFile)
            {
                ICsvLine csvLine = new CsvLine();

                csvLine.Values = line.Split(',');
                //Trim spaces of each element of the array.
                if (Configuration.TrimData)
                {
                    for (int i = 0; i < csvLine.Values.Length; i++)
                    {
                        csvLine.Values[i] = csvLine.Values[i].Trim();
                    }
                }
            }
            return lines.ToArray();
        }
    }
}
