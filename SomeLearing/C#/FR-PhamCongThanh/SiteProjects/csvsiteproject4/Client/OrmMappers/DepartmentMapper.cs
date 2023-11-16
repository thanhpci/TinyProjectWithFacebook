using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SiteProjectWeek4.Client.Entities;
using SiteProjectWeek4.CsvLib.Interfaces;
using SiteProjectWeek4.Client.OrmMappers;
using SiteProjectWeek4.CsvLib;

namespace SiteProjectWeek4.Client.OrmMappers
{
    //Implement IOrmMapper<Department>, convert ICsvLine object to Department entity object 
    class DepartmentMapper : IOrmMapper<Department>
    {
        

        T IOrmMapper<Department>.ToEntity<T>(ICsvLine line)
        {
            string[] values = line.Values;
            if (values.Length == 2)
            {
                int departmentId = int.Parse(values[0]);
                string name = values[1];
                Department department = new Department
                {
                    DepartmentId = departmentId,
                    Name = name
                };

                return (T)Convert.ChangeType(department, typeof(T));
            }
            return default(T);
        }

        ICsvLine IOrmMapper<Department>.ToCsvLine<T>(T entity)
        {
            Department department = entity as Department;
            if (department == null) return null;
            
            string[] values = { department.DepartmentId.ToString(),
                                    department.Name };
            return new CsvLine(values);           
        }
    }

}
