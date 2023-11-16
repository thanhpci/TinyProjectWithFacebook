using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek3.CsvLib.Orm
{
    class OrmHelper
    {
        private IDictionary<Type, IOrmMapper> ormMappers = new Dictionary<Type, IOrmMapper>();
        public T ToEntity<T>(ICsvLine line)
            where T : class
        {
            return null;
        }

        public ICsvLine ToCsvLine<T>(T entity)
            where T : class
        {
            return null;
        }
    }
}
