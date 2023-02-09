using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek3.CsvLib
{
    interface ICsvLine
    {
        string[] Values { get; }

        /// <summary>
        /// Chuỗi CSV đọc từ nguồn (file, string)
        /// </summary>
        string Raw { get; }

        /// <summary>
        /// Chuỗi CSV tương ứng với giá trị của mảng Values
        /// </summary>
        /// <returns></returns>
        string ToString();
    }
}
