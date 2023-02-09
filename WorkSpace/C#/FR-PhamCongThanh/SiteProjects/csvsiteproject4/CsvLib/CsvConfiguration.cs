namespace SiteProjectWeek4.CsvLib
{
    public class CsvConfiguration
    {
        /// <summary>
        /// Gets or sets a function to skip the current row based on its raw string value or 1-based index.
        /// Skips empty rows and rows starting with # by default.
        /// </summary>
        public SkipLineDelegate SkipLineCallback { get; set; } = (idx, row) => string.IsNullOrEmpty(row) || row.StartsWith("#");

        // <summary>
        /// Gets or sets whether data should be trimmed when accessed.
        /// </summary>
        public bool TrimData { get; set; } = true;

    }
}
