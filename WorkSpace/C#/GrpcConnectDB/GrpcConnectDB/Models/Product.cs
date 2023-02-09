using System;
using System.Collections.Generic;

namespace GrpcConnectDB.Models
{
    public partial class Product
    {
        public Product()
        {
            ProductDetails = new HashSet<ProductDetail>();
        }

        public int Id { get; set; }
        public string? Name { get; set; }
        public string? TagName { get; set; }
        public bool? Active { get; set; }
        public int CategoryId { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime UpdatedDate { get; set; }

        public virtual Category Category { get; set; } = null!;
        public virtual ICollection<ProductDetail> ProductDetails { get; set; }
    }
}
