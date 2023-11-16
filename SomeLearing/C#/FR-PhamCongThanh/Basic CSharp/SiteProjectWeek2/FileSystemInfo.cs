using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek2
{
    internal abstract class FileSystemInfo
    {
        public string Name { get; set; }
        public abstract long GetStorageSize();


        public virtual string List()
        {
            return this.Name;
        }


        public void Rename(string newName)
        {
            if (newName != null)
            {
                string s = newName;

                s = s.TrimStart(' ');
                s = s.TrimEnd(' ');
                if (s.Length != 0)
                {
                    this.Name = s;
                }
            }
        }
        


    }
}
