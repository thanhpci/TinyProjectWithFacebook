using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek3.CsvLib
{
    internal class CsvLine : ICsvLine
    {
        public string[] Values { get; set; }
        public string Raw { get; set; }
        public override string ToString()
        {
            string result = "";
            if (Values != null && Values.Length != 0)
            {
                foreach(string value in Values)
                {
                    result += value + ",";
                }
            } else
            {
                result = Raw;
            }


             return result;
        }   
    }
}
