using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek4.CsvLib
{
    public delegate bool SkipLineDelegate(int lineIndex, string lineText);
    public delegate void SkippedLineEventHandler(int lineIndex);
}
