using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek2
{
    internal class File : FileSystemInfo
    {
        private long _size;
        public File(string name)
        {
            this.Name = name;
        }


        public File(String name, long size)
        {
            this.Name = name;
            this._size = size;
        }

        public override long GetStorageSize()
        {
            return _size;
        }
    }
}
