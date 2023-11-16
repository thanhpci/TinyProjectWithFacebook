using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek4.Client.Entities
{
    class Employee
    {
        public int EmployeeId{ get; set; }
        public int DepartmentId { get; set; }
        public string Name { get; set; }
        public DateTime DateOfBirth { get; set; }
    }
}
