using Grpc.Core;
using Microsoft.EntityFrameworkCore;
using DataAccess = GrpcService1.DataAccess;


namespace GrpcService1.Services
{

    public class EmployeeCRUDService : EmployeeCRUD.EmployeeCRUDBase
    {
        private DataAccess.AppDbContext db = null;

        public EmployeeCRUDService(DataAccess.AppDbContext db)
        {
            this.db = db;
        }


        public override Task<Employees> SelectAll(Empty requestData, ServerCallContext context)
        {
            Employees responseData = new Employees();
            var query = from emp in db.Employees
                        select new Employee()
                        {
                            EmployeeID = emp.EmployeeID,
                            FirstName = emp.FirstName,
                            LastName = emp.LastName
                        };
            responseData.Items.AddRange(query.ToArray());
            return Task.FromResult(responseData);
        }


        public override Task<Employee> SelectByID(EmployeeFilter requestData, ServerCallContext context)
        {
            var data = db.Employees.Find(requestData.EmployeeID);
            Employee emp = new Employee()
            {
                EmployeeID = data.EmployeeID,
                FirstName = data.FirstName,
                LastName = data.LastName
            };
            return Task.FromResult(emp);
        }

        public override Task<Empty> Insert(Employee requestData, ServerCallContext context)
        {
            db.Employees.Add(new DataAccess.Employee()
            {
                EmployeeID = requestData.EmployeeID,
                FirstName = requestData.FirstName,
                LastName = requestData.LastName
            });
            db.SaveChanges();
            return Task.FromResult(new Empty());
        }

        public override Task<Empty>Update(Employee requestData, ServerCallContext context)
        {
            db.Employees.Update(new DataAccess.Employee()
            {
                EmployeeID = requestData.EmployeeID,
                FirstName = requestData.FirstName,
                LastName = requestData.LastName
            });
            db.SaveChanges();
            return Task.FromResult(new Empty());
        }


        public override Task<Empty> Delete(EmployeeFilter requestData, ServerCallContext context)
        {
            var data = db.Employees.Find(requestData.EmployeeID);
            db.Entry(data).State = EntityState.Detached;
            db.Employees.Remove(new DataAccess.Employee()
            {
                EmployeeID = data.EmployeeID,
                FirstName = data.FirstName,
                LastName = data.LastName
            });
            db.SaveChanges();
            return Task.FromResult(new Empty());
        }

    }
}
