using System;
using System.Text;

namespace SiteProjectWeek4.CsvLib
{
    internal sealed class CsvLine : ICsvLine
    {
        public CsvLine(string[] values, string raw)
        {
            Values = values;
            Raw = raw;
        }

        public string[] Values { get; }

        public string Raw { get; }

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
