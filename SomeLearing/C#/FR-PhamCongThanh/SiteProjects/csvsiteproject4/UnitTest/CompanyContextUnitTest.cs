using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SiteProjectWeek4.Client;
using SiteProjectWeek4.Client.Entities;
using SiteProjectWeek4.Client.OrmMappers;
using SiteProjectWeek4.CsvLib;
using SiteProjectWeek4.CsvLib.Orm;

namespace SiteProjectWeek4.UnitTest
{
    class CompanyContextUnitTest
    {
        public static bool TC_CompanyContext_Constructor_TestEmployeesFalse()
        {
            try
            {
                CompanyContext companyContext = new CompanyContext(null, DataTest.EmployeeCsvFile);
                return false;
            }
            catch (ArgumentNullException)
            {
                return true;
            }
            catch
            {
                return false;
            }

        }

        public static bool TC_CompanyContext_Constructor_TestDepartmentalse()
        {
            try
            {
                CompanyContext companyContext = new CompanyContext(DataTest.EmployeeCsvFile, null);
                return false;
            }
            catch (ArgumentNullException)
            {
                return true;
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_SaveEmployees_TestSuccess()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                companyContext.SaveFilteredEmployees(DataTest.FilePathEmployee, companyContext.Employees.ToList());
                return Compare(DataTest.FilePathEmployee, companyContext.Employees.ToList());
            }
            catch (Exception ex)
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_SaveDepartments_TestSuccess()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                companyContext.SaveFilteredDepartments(DataTest.FilePathDepartment, companyContext.Departments.ToList());
                return Compare(DataTest.FilePathEmployee, companyContext.Employees.ToList());
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_SaveEmployees_TestFalse()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                return !companyContext.SaveFilteredEmployees(DataTest.FilePathEmployee, null);
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_SaveDepartments_TestFalse()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                return !companyContext.SaveFilteredDepartments(DataTest.FilePathDepartment, null);
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_LoadEmployee_Test()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                return Compare(DataTest.FilePathEmployee, companyContext.Employees.ToList());
            }
            catch
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_LoadDepartment_Test()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                return Compare(DataTest.FilePathDepartment, companyContext.Departments.ToList());
            }
            catch(Exception ex)
            {
                return false;
            }
        }

        public static bool TC_CompanyContext_GetEmployeeByID_Test()
        {
            try
            {
                CompanyContext companyContext = CreateCompanyContext();
                var employee = companyContext.GetEmployeeByID(1);
                var employee2 = companyContext.GetEmployeeByID(2);
                return employee2 == null && employee != null && employee.EmployeeId == 1;
            }
            catch 
            {
                return false;
            }
        }
     

        private static CompanyContext CreateCompanyContext()
        {
            return new CompanyContext(DataTest.DepartmentCsvFile, DataTest.EmployeeCsvFile);
        }


        #region Compare

        public static bool Compare<T>(string destFilePath, IList<T> departments) where T : class
        {
            var item = new CsvReader().ReadFromFile(destFilePath);
            return Compare(item, departments);
        }

        public static bool Compare<T>(IList<ICsvLine> iCsvLines, IList<T> departments) where T : class
        {
            if (iCsvLines.Count() != departments.Count())
            {
                return false;
            }
            for (int i = 0; i < iCsvLines.Count(); i++)
            {
                if (!Compare(iCsvLines[i], departments[i]))
                {
                    return false;
                }
            }
            return true;
        }

        public static bool Compare<T>(ICsvLine csvLine, T entity) where T : class
        {
            IOrmMapper<T> iOrmMapper;
            int propertiesCount = 0;
            if (entity is Employee)
            {
                iOrmMapper = (IOrmMapper<T>)new EmployeeMapper();
                propertiesCount = 4;
            }
            else
            {
                iOrmMapper = (IOrmMapper<T>)new DepartmentMapper();
                propertiesCount = 2;
            }

            var tLine = iOrmMapper.ToCsvLine(entity);
            for (int i = 0; i < propertiesCount; i++)
            {
                if (tLine.Values[i] != csvLine.Values[i])
                {
                    return false;
                }
            }
            return true;
        }

        #endregion
    }
}
