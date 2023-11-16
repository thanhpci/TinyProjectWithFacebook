using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek3.CsvLib
{
    interface ICsvLine
    {
        string[] Values { get; set; }
        string Raw { get; }


        string ToString();
        
    }
}
