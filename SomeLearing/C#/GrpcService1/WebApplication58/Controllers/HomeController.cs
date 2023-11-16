using Grpc.Net.Client;
using GrpcService1;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using WebApplication58.Models;

namespace WebApplication58.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            var channel = GrpcChannel.ForAddress("https://localhost:7076");
            var client = new EmployeeCRUD.EmployeeCRUDClient(channel);
                   

            Employees employees = client.SelectAll(new Empty());
            
            return View(employees);
        }

        public IActionResult Delete(string id)
        {
            var channel = GrpcChannel.ForAddress("https://localhost:7076");
            var client = new EmployeeCRUD.EmployeeCRUDClient(channel);

            var empId = new EmployeeFilter();
            empId.EmployeeID = Convert.ToInt32(id);
            var emp = client.Delete(empId);

            return RedirectToAction("Index");
        }


        







        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}