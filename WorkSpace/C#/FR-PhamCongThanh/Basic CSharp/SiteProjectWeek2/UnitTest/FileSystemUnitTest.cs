namespace SiteProjectWeek2
{
    class FileSystemUnitTest
    {
        #region Testcases for class File

        #region TC_File_Constructor testcases

        public static bool TC_File_ConstructorTest_NameOnly()
        {
            string expectedName = "test.txt";
            long expectSize = 0L;

            File file = new File(expectedName);

            return (file.Name == expectedName) && (file.GetStorageSize() == expectSize);
        }

        public static bool TC_File_ConstructorTest_NameAndSize()
        {
            string expectedName = "test.txt";
            long expectSize = 1000L;

            File file = new File(expectedName, expectSize);

            return (file.Name == expectedName) && (file.GetStorageSize() == expectSize);
        }

        #endregion

        #region TC_File_List testcases
        public static bool TC_File_ListTest()
        {
            string expectedName = "test.txt";
            long expectSize = 1000L;
            string expectListReturnValue = expectedName;

            File file = new File(expectedName, expectSize);

            return (file.List() == expectListReturnValue);
        }
        #endregion

        #region TC_File_Rename testcases
        public static bool TC_File_RenameTest_InputNull()
        {
            string expectedName = "test.txt";

            File file = new File(expectedName);
            file.Rename(null);

            return (file.Name == expectedName);
        }

        public static bool TC_File_RenameTest_InputEmpty()
        {
            string expectedName = "test.txt";

            File file = new File(expectedName);
            file.Rename(string.Empty);

            return (file.Name == expectedName);
        }

        public static bool TC_File_RenameTest_InputWhitespaces()
        {
            string expectedName = "test.txt";

            File file = new File(expectedName);
            file.Rename("           ");

            return (file.Name == expectedName);
        }

        public static bool TC_File_RenameTest_InputValidName()
        {
            string initialName = "test.txt";
            string expectedName = "test2.txt";

            File file = new File(initialName);
            file.Rename(expectedName);

            return (file.Name == expectedName);
        }
        #endregion

        #endregion Testcases for class File

        #region Testcases for class Folder

        #region Prepare TC_Folder testcases data
        static Folder InitFolderWith2Levels()
        {
            /*
             * Folder structure:
             * MyMusics
             *   |___ File1.mp3
             *   |___ File2.mp3
             *   |___ File3.mp3
             *   |___ Folder1
             *          |___ Fd1_File1.mp3
             *          |___ Fd1_File2.mp3
             *   |___ Folder2
             *          |___ Fd2_File1.mp3
             *          |___ Fd2_File2.mp3
             */

            Folder folder = new Folder("MyMusics");
            folder.AddChildItem(new File("File1.mp3", 1000L));
            folder.AddChildItem(new File("File2.mp3", 2000L));
            folder.AddChildItem(new File("File3.mp3", 3000L));

            Folder subFolder1 = new Folder("Folder1");
            subFolder1.AddChildItem(new File("Fd1_File1.mp3", 1000L));
            subFolder1.AddChildItem(new File("Fd1_File2.mp3", 2000L));
            folder.AddChildItem(subFolder1);

            Folder subFolder2 = new Folder("Folder2");
            subFolder2.AddChildItem(new File("Fd2_File1.mp3", 1000L));
            subFolder2.AddChildItem(new File("Fd2_File2.mp3", 2000L));
            folder.AddChildItem(subFolder2);

            return folder;
        }

        static Folder InitFolderWith3Levels()
        {
            /*
            * Folder structure:
            * MyMusics
            *   |___ File1.mp3
            *   |___ File2.mp3
            *   |___ File3.mp3
            *   |___ Folder1
            *          |___ Fd1_File1.mp3
            *          |___ Fd1_File2.mp3
            *          |___ Folder11
            *                  |___ Fd11_File1.mp3
            *                  |___ Fd11_File2.mp3
            *   |___ Folder2
            *          |___ Fd2_File1.mp3
            *          |___ Fd2_File2.mp3
            */

            Folder folder = new Folder("MyMusics");
            folder.AddChildItem(new File("File1.mp3", 1000L));
            folder.AddChildItem(new File("File2.mp3", 2000L));
            folder.AddChildItem(new File("File3.mp3", 3000L));

            Folder subFolder1 = new Folder("Folder1");
            subFolder1.AddChildItem(new File("Fd1_File1.mp3", 1000L));
            subFolder1.AddChildItem(new File("Fd1_File2.mp3", 2000L));

            Folder subFolder11 = new Folder("Folder11");
            subFolder11.AddChildItem(new File("Fd11_File1.mp3", 1000L));
            subFolder11.AddChildItem(new File("Fd11_File2.mp3", 2000L));
            subFolder1.AddChildItem(subFolder11);
            folder.AddChildItem(subFolder1);

            Folder subFolder2 = new Folder("Folder2");
            subFolder2.AddChildItem(new File("Fd2_File1.mp3", 1000L));
            subFolder2.AddChildItem(new File("Fd2_File2.mp3", 2000L));
            folder.AddChildItem(subFolder2);

            return folder;
        }
        #endregion  Prepare testcase data

        #region TC_Folder_Constructor
        public static bool TC_Folder_ConstructorTest_Name()
        {
            string expectedName = "MyMusics";

            Folder folder = new Folder(expectedName);

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_ConstructorTest_NoFile()
        {
            string expectedName = "MyMusics";

            Folder folder = new Folder(expectedName);

            return (folder.GetFiles().Length == 0);
        }

        public static bool TC_Folder_ConstructorTest_NoSubFolder()
        {
            string expectedName = "MyMusics";

            Folder folder = new Folder(expectedName);

            return (folder.GetFolders().Length == 0);
        }

        public static bool TC_Folder_ConstructorTest_Size0()
        {
            string expectedName = "MyMusics";

            Folder folder = new Folder(expectedName);

            return (folder.GetStorageSize() == 0);
        } 
        #endregion

        #region TC_Folder_List testcases
        public static bool TC_Folder_ListTest_FolderEmpty()
        {
            string expectedName = "MyMusics";
            string expectedValue = "MyMusics";

            Folder folder = new Folder(expectedName);

            return (folder.List() == expectedValue);
        }

        public static bool TC_Folder_ListTest_ContainsFilesOnly()
        {
            /*
             * Folder structure:
             * MyMusics
             *   |___ File1.mp3
             *   |___ File2.mp3
             *   |___ File3.mp3
             */
            string expectedValue =
@"MyMusics
File1.mp3
File2.mp3
File3.mp3";

            Folder folder = new Folder("MyMusics");
            folder.AddChildItem(new File("File1.mp3"));
            folder.AddChildItem(new File("File2.mp3"));
            folder.AddChildItem(new File("File3.mp3"));

            return (folder.List() == expectedValue);
        }

        public static bool TC_Folder_ListTest_2FolderLevels()
        {
            /*
             * Folder structure:
             * MyMusics
             *   |___ File1.mp3
             *   |___ File2.mp3
             *   |___ File3.mp3
             *   |___ Folder1
             *          |___ Fd1_File1.mp3
             *          |___ Fd1_File2.mp3
             *   |___ Folder2
             *          |___ Fd2_File1.mp3
             *          |___ Fd2_File2.mp3
             */
            string expectedValue =
@"MyMusics
File1.mp3
File2.mp3
File3.mp3
Folder1
Fd1_File1.mp3
Fd1_File2.mp3
Folder2
Fd2_File1.mp3
Fd2_File2.mp3";

            Folder folder = InitFolderWith2Levels();

            return (folder.List() == expectedValue);
        }


        public static bool TC_Folder_ListTest_MultiSubFolderLevels()
        {
            /*
             * Folder structure:
             * MyMusics
             *   |___ File1.mp3
             *   |___ File2.mp3
             *   |___ File3.mp3
             *   |___ Folder1
             *          |___ Fd1_File1.mp3
             *          |___ Fd1_File2.mp3
             *          |___ Folder11
             *                  |___ Fd11_File1.mp3
             *                  |___ Fd11_File2.mp3
             *   |___ Folder2
             *          |___ Fd2_File1.mp3
             *          |___ Fd2_File2.mp3
             */
            string expectedValue =
@"MyMusics
File1.mp3
File2.mp3
File3.mp3
Folder1
Fd1_File1.mp3
Fd1_File2.mp3
Folder11
Fd11_File1.mp3
Fd11_File2.mp3
Folder2
Fd2_File1.mp3
Fd2_File2.mp3";

            Folder folder = InitFolderWith3Levels();
            return (folder.List() == expectedValue);
        }

        #endregion

        #region TC_Folder_Rename testcases
        public static bool TC_Folder_RenameTest_InputNull()
        {
            string expectedName = "test";

            Folder folder = new Folder(expectedName);
            folder.Rename(null);

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_RenameTest_InputEmpty()
        {
            string expectedName = "test";

            Folder folder = new Folder(expectedName);
            folder.Rename(string.Empty);

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_RenameTest_InputAllWhitespaces()
        {
            string expectedName = "test";

            Folder folder = new Folder(expectedName);
            folder.Rename("       ");

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_RenameTest_InputStartWhitespaces()
        {
            string initialName = "test";
            string newName = "          test2";
            string expectedName = newName.Trim();

            Folder folder = new Folder(initialName);
            folder.Rename(newName);

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_RenameTest_InputEndWhitespaces()
        {
            string initialName = "test";
            string newName = "test2          ";
            string expectedName = newName.Trim();

            Folder folder = new Folder(initialName);
            folder.Rename(newName);

            return (folder.Name == expectedName);
        }

        public static bool TC_Folder_RenameTest_InputValidName()
        {
            string initialName = "test";
            string expectedName = "test2";

            Folder folder = new Folder(initialName);
            folder.Rename(expectedName);

            return (folder.Name == expectedName);
        }
        #endregion

        #region TC_Folder_AddChildItem testcases
        public static bool TC_Folder_AddChildItemTest_AddNull()
        {
            Folder rootFolder = new Folder("MyMusics");
            rootFolder.AddChildItem(null);

            return (rootFolder.GetFiles().Length + rootFolder.GetFolders().Length == 0);
        }

        public static bool TC_Folder_AddChildItemTest_AddSingleFile()
        {
            Folder rootFolder = new Folder("MyMusics");

            rootFolder.AddChildItem(new File("Only love - Trademark.mp3"));

            return (rootFolder.GetFiles().Length == 1);
        }

        public static bool TC_Folder_AddChildItemTest_AddMultiFiles()
        {
            Folder rootFolder = new Folder("MyMusics");
            int fileCount = 10;

            for (int i = 0; i < fileCount; i++)
            {
                rootFolder.AddChildItem(new File($"Only love {i} - Trademark.mp3"));
            }

            return (rootFolder.GetFiles().Length == fileCount);
        }

        public static bool TC_Folder_AddChildItemTest_AddSingleFolder()
        {
            Folder rootFolder = new Folder("MyMusics");

            rootFolder.AddChildItem(new Folder("Micheal Jackson"));

            return (rootFolder.GetFolders().Length == 1);
        }

        public static bool TC_Folder_AddChildItemTest_AddMultiFolders()
        {
            Folder rootFolder = new Folder("MyMusics");
            int subFolderCount = 5;

            for (int i = 0; i < subFolderCount; i++)
            {
                rootFolder.AddChildItem(new Folder($"Micheal Jackson {i}"));
            }

            return (rootFolder.GetFolders().Length == subFolderCount);
        }

        public static bool TC_Folder_AddChildItemTest_AddFilesAndFolders()
        {
            Folder rootFolder = new Folder("MyMusics");
            int fileCount = 10;
            int subFolderCount = 5;

            for (int i = 0; i < fileCount; i++)
            {
                rootFolder.AddChildItem(new File($"Only love {i} - Trademark.mp3"));
            }

            for (int i = 0; i < subFolderCount; i++)
            {
                rootFolder.AddChildItem(new Folder($"Micheal Jackson {i}"));
            }

            return (rootFolder.GetFiles().Length == fileCount)
                    && (rootFolder.GetFolders().Length == subFolderCount);
        }
        #endregion

        #region TC_Folder_GetFiles testcases

        public static bool TC_Folder_GetFilesTest()
        {
            /*
            * Folder structure:
            * MyMusics
            *   |___ File1.mp3
            *   |___ File2.mp3
            *   |___ File3.mp3
            *   |___ Folder1
            *          |___ Fd1_File1.mp3
            *          |___ Fd1_File2.mp3
            *          |___ Folder11
            *                  |___ Fd11_File1.mp3
            *                  |___ Fd11_File2.mp3
            *   |___ Folder2
            *          |___ Fd2_File1.mp3
            *          |___ Fd2_File2.mp3
            */

            Folder folder = InitFolderWith3Levels();
            Folder[] subFolders = folder.GetFolders();

            return (folder.GetFiles().Length == 3)
                    && (subFolders[0].GetFiles().Length == 2)
                    && (subFolders[1].GetFiles().Length == 2);
        }

        public static bool TC_Folder_GetFoldersTest()
        {
            /*
            * Folder structure:
            * MyMusics
            *   |___ File1.mp3
            *   |___ File2.mp3
            *   |___ File3.mp3
            *   |___ Folder1
            *          |___ Fd1_File1.mp3
            *          |___ Fd1_File2.mp3
            *          |___ Folder11
            *                  |___ Fd11_File1.mp3
            *                  |___ Fd11_File2.mp3
            *   |___ Folder2
            *          |___ Fd2_File1.mp3
            *          |___ Fd2_File2.mp3
            */

            Folder folder = InitFolderWith3Levels();
            Folder[] subFolders = folder.GetFolders();

            return (subFolders.Length == 2)
                    && (subFolders[0].GetFolders().Length == 1)
                    && (subFolders[1].GetFolders().Length == 0);
        }

        #endregion

        #region TC_Folder_GetStorageSize testcases

        public static bool TC_Folder_GetStorageSizeTest_FolderEmpty()
        {
            Folder folder = new Folder("test");

            return (folder.GetStorageSize() == 0L);
        }

        public static bool TC_Folder_GetStorageSizeTest_NoSubFolders()
        {
            Folder folder = new Folder("MyMusics");
            folder.AddChildItem(new File("File1.mp3", 1000L));
            folder.AddChildItem(new File("File2.mp3", 2000L));
            folder.AddChildItem(new File("File3.mp3", 3000L));

            return (folder.GetStorageSize() == (1000L + 2000L + 3000L));
        }

        public static bool TC_Folder_GetStorageSizeTest_HasSubFolders()
        {
            /*
            * Folder structure:
            * MyMusics
            *   |___ File1.mp3
            *   |___ File2.mp3
            *   |___ File3.mp3
            *   |___ Folder1
            *          |___ Fd1_File1.mp3
            *          |___ Fd1_File2.mp3
            *          |___ Folder11
            *                  |___ Fd11_File1.mp3
            *                  |___ Fd11_File2.mp3
            *   |___ Folder2
            *          |___ Fd2_File1.mp3
            *          |___ Fd2_File2.mp3
            */

            Folder folder = InitFolderWith3Levels();

            return (folder.GetStorageSize()
                     == 
                     (
                        (1000L + 2000L + 3000L) 
                        + (1000L + 2000L)
                        + (1000L + 2000L)
                        + (1000L + 2000L)
                     ));
        }

        #endregion

        #region TC_Folder_ContainsFile testcases
        public static bool TC_Folder_ContainsFileTest_NotFound()
        {
            Folder folder = InitFolderWith3Levels();

            return (folder.ContainsFile("File4.mp3") == false);
        }

        public static bool TC_Folder_ContainsFileTest_Found_InRootFolder()
        {
            /*
           * Folder structure:
           * MyMusics
           *   |___ File1.mp3
           *   |___ File2.mp3
           *   |___ File3.mp3
           *   |___ Folder1
           *          |___ Fd1_File1.mp3
           *          |___ Fd1_File2.mp3
           *          |___ Folder11
           *                  |___ Fd11_File1.mp3
           *                  |___ Fd11_File2.mp3
           *   |___ Folder2
           *          |___ Fd2_File1.mp3
           *          |___ Fd2_File2.mp3
           */

            Folder folder = new Folder("MyMusics");
            folder.AddChildItem(new File("File1.mp3"));
            folder.AddChildItem(new File("File2.mp3"));
            folder.AddChildItem(new File("File3.mp3"));

            Folder subFolder1 = new Folder("Folder1");
            subFolder1.AddChildItem(new File("Fd1_File1.mp3"));
            subFolder1.AddChildItem(new File("Fd1_File2.mp3"));

            Folder subFolder11 = new Folder("Folder11");
            subFolder11.AddChildItem(new File("Fd11_File1.mp3"));
            subFolder11.AddChildItem(new File("Fd11_File2.mp3"));
            subFolder1.AddChildItem(subFolder11);
            folder.AddChildItem(subFolder1);

            Folder subFolder2 = new Folder("Folder2");
            subFolder2.AddChildItem(new File("Fd2_File1.mp3"));
            subFolder2.AddChildItem(new File("Fd2_File2.mp3"));
            folder.AddChildItem(subFolder2);

            return (folder.ContainsFile("File3.mp3") == true);
        }

        public static bool TC_Folder_ContainsFileTest_Found_InSubFolderLevel1()
        {
            Folder folder = InitFolderWith3Levels();

            return (folder.ContainsFile("Fd2_File1.mp3") == true);
        }

        public static bool TC_Folder_ContainsFileTest_Found_InSubFolderLevel2()
        {
            Folder folder = InitFolderWith3Levels();

            return (folder.ContainsFile("Fd11_File2.mp3") == true);
        }
        #endregion

        #endregion Testcases for class Folder
    }
}
