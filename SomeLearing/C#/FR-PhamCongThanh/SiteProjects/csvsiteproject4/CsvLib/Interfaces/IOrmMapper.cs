using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek4.CsvLib.Interfaces
{
    interface IOrmMapper<T>
    {
        //Mapping from 1 ICsvLine to Entity object
        T ToEntity<T>(ICsvLine line);

        //Mapping form 1 Entity to 1 CsvLine. 
        ICsvLine ToCsvLine<T>(T entity); 
    
    }
}
