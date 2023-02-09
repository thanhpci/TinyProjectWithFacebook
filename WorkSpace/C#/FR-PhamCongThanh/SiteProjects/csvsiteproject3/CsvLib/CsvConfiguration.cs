    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Claims;
    using System.Text;
    using System.Threading.Tasks;
    using static SiteProjectWeek3.CsvLib.Delegates;



    namespace SiteProjectWeek3.CsvLib
    {
        internal class CsvConfiguration
        {
 
           public CsvConfiguration() { }
            public SkipLineDelegate SkipLineCallback()
            {
                return (index, row) =>
                {
                    if (row.Length == 0 || row.StartsWith("#")) return true;
                    else return false;
                };
            }


            public bool TrimData { get; set; } = true;
        
        
        }
    }