using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SiteProjectWeek4.CsvLib.Interfaces;
using SiteProjectWeek4.Client.Entities;
using SiteProjectWeek4.Client.OrmMappers;
using SiteProjectWeek4.CsvLib;



namespace SiteProjectWeek4.Client
{
    class CompanyContext
    {
        private readonly List<Department> departments;
        private readonly List<Employee> employees;
        private readonly DepartmentMapper departmentMapper;
        private readonly EmployeeMapper employeeMapper;

        public IReadOnlyList<Department> Departments { get { return departments; } }
        public IReadOnlyList<Employee> Employees { get { return employees; } }

        public CompanyContext(string departmentCsvFile, string employeesCsvFile) {
            if (departmentCsvFile == null || employeesCsvFile == null)
                throw new ArgumentNullException();
            
            LoadDepartments(departmentCsvFile);
            LoadEmployees(employeesCsvFile);
        }

        public void LoadDepartments(string departmentCsvFile) {
           

        }

        public void LoadEmployees(string employeesCsvFile) {

        }
        
        public bool SaveFilteredDepartments(string csvPathFile, IList<Department> departments) {
            return true;
        }

        public bool SaveFilteredEmployees(string csvPathFile, IList<Employee> employees) {
            return true;
        }

        public Employee GetEmployeeByID(int employeeId) {
            return null;
        }

        public Employee GetEmployees(int skip, int take) {
            return null;
        }

        public IEnumerable<Employee> GetEmployeesByDepartmentName(string departmentName) {
            return null;
        }

        public IEnumerable<Employee> GetOrderedEmployeesByAge() {
            return null;
        }

        public IEnumerable<Department> GetEmptyDepartments(){
            return null;
        }

    } 
}
