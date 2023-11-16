using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace SiteProjectWeek4.CsvLib
{
    class CsvReader
    {
        public CsvConfiguration Configuration { get; set; } = new CsvConfiguration();
        public event SkippedLineEventHandler SkippedLine;

        public ICsvLine[] ReadFromFile(string filePath)
        {
            if (!File.Exists(filePath))
            {
                return new ICsvLine[0];
            }

            string fileContent = File.ReadAllText(filePath);
            return ReadFromString(fileContent);
        }

        public ICsvLine[] ReadFromStream(Stream stream)
        {
            if(stream == null || !stream.CanRead)
            {
                return new ICsvLine[0];
            }
            using (var reader = new StreamReader(stream))
            {
                return ReadFromTextReader(reader);
            }
        }

        public ICsvLine[] ReadFromString(string csvContent)
        {
            if(string.IsNullOrEmpty(csvContent))
            {
                return new ICsvLine[0];
            }
            using (var reader = new StringReader(csvContent))
            {
                return ReadFromTextReader(reader);
            }
        }

        private ICsvLine[] ReadFromTextReader(TextReader reader)
        {
            var index = 0;
            string line;
            IList<CsvLine> readLines = new List<CsvLine>();
            while ((line = reader.ReadLine()) != null)
            {
                index++;
                if (Configuration.SkipLineCallback?.Invoke(index, line) == true)
                {
                    SkippedLine?.Invoke(index);
                    continue;
                }
                readLines.Add(new CsvLine(SplitLine(line), line));
            }
            return readLines.ToArray();
        }

        private string[] GetHeaders(string line)
        {
            return SplitLine(line);
        }

        private string[] SplitLine(string line)
        {
            return Configuration.TrimData ? line.Split(',').Select(p => p.Trim()).ToArray() : line.Split(',');
        }

        //private bool ShouldSkipLine(int index, string text)
        //{
        //    return (index == 0)
        //            || string.IsNullOrWhiteSpace(text)
        //            || text.StartsWith("#");
        //}
    }
}
