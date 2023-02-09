using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SiteProjectWeek2
{
    internal class Folder : FileSystemInfo
    {

        private FileSystemInfo[] _childItems;

        public Folder(string name)
        {
            this.Name = name;
            _childItems = new FileSystemInfo[0];
        }

        public void AddChildItem(FileSystemInfo item)
        {
            if (item != null)
            {
                FileSystemInfo[] newChildItems = new FileSystemInfo[_childItems.Length + 1];
                for (int i = 0; i < _childItems.Length; i++)
                {
                    newChildItems[i] = _childItems[i];
                }
                newChildItems[_childItems.Length] = item;
                _childItems = newChildItems;
            }
        }

        public File[] GetFiles()
        {

            int j = 0;
            File[] files = new File[_childItems.Length];
            for (int i = 0; i < _childItems.Length; i++)
            {
                if (_childItems[i] is File)
                {
                    files[j++] = _childItems[i] as File;
                }
            }
            File[] result = new File[j];
            for (int i = 0; i < result.Length; i++)
            {
                result[i] = files[i];
            }
            return result;
        }



        public Folder[] GetFolders()
        {
            int j = 0;
            Folder[] folders = new Folder[_childItems.Length];
            for (int i = 0; i<_childItems.Length; i++)
            {
                if (_childItems[i] is Folder)
                {
                    folders[j++] = _childItems[i] as Folder;
                }
            }
            Folder[] result = new Folder[j];
            for (int i = 0; i < result.Length; i++)
            {
                result[i] = folders[i];
            }
            return result;
        }
        

        public override long GetStorageSize()
        {
            long size = 0;
            foreach (FileSystemInfo item in _childItems)
            {
                size += item.GetStorageSize();
            }
            return size;
        }
        

        public override string List()
        {
            string result = this.Name;
            foreach (FileSystemInfo item in _childItems)
            {
                result += Environment.NewLine + item.List();
            }
            return result;
        }



        public bool ContainsFile(string fileName)
        {
            bool includeSubFolder = true;
            foreach (FileSystemInfo item in _childItems)
            {
                if (item is File)
                {
                    if (item.Name == fileName)
                    {
                        return true;
                    }
                }
                else
                {
                    if (includeSubFolder)
                    {
                        Folder folder = item as Folder;
                        if (folder.ContainsFile(fileName))
                        {
                            return true;
                        }
                    }
                }
            }
            return false;
        }
    }
}
