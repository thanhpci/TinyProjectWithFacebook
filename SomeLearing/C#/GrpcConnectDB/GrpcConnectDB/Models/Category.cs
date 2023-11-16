using System;
using System.Collections.Generic;

namespace GrpcConnectDB.Models
{
    public partial class Category
    {
        public Category()
        {
            Products = new HashSet<Product>();
        }

        public int Id { get; set; }
        public string? Name { get; set; }
        public string? TagName { get; set; }
        public bool? Active { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime UpdatedDate { get; set; }

        public virtual ICollection<Product> Products { get; set; }
    }
}
