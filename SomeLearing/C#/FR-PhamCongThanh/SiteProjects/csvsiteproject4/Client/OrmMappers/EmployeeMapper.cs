using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SiteProjectWeek4.Client.Entities;
using SiteProjectWeek4.Client.OrmMappers;
using SiteProjectWeek4.CsvLib;
using SiteProjectWeek4.CsvLib.Interfaces;

namespace SiteProjectWeek4.Client.OrmMappers
{
    //Implement IOrmMapper<Employee>, to convert ICsvLine object to Employee entity object
    class EmployeeMapper : IOrmMapper<Employee>
    {

        public T ToEntity<T>(ICsvLine line)
        {
            string[] values = line.Values;
            if (values.Length == 4)
            {
                int employeeId = int.Parse(values[0]);
                int departmentId = int.Parse(values[1]);
                string name = values[2];
                DateTime dateOfBirth = DateTime.Parse(values[3]);
                Employee employee = new Employee
                {
                    EmployeeId = employeeId,
                    DepartmentId = departmentId,
                    Name = name,
                    DateOfBirth = dateOfBirth
                };

                return (T)Convert.ChangeType(employee, typeof(T));
            }
            return default(T);
        }

        ICsvLine IOrmMapper<Employee>.ToCsvLine<T>(T entity)
        {
            Employee employee = entity as Employee;
            if (employee == null) return null;
            
            string[] values = { employee.EmployeeId.ToString(),
                                employee.DepartmentId.ToString(),
                                employee.Name,
                                employee.DateOfBirth.ToString() };

            return new CsvLine(values);
            
        }
    }

}
