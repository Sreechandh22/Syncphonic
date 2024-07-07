using System.Data.SQLite;

namespace ClipboardManager.Database
{
    public class ClipboardDatabase
    {
        private readonly string _connectionString = "Data Source=clipboard.db;Version=3;";

        public void InitializeDatabase()
        {
            using (var connection = new SQLiteConnection(_connectionString))
            {
                connection.Open();
                var command = new SQLiteCommand(
                    "CREATE TABLE IF NOT EXISTS ClipboardItems (Id INTEGER PRIMARY KEY, Content TEXT, Timestamp DATETIME, IsStarred BOOLEAN)",
                    connection);
                command.ExecuteNonQuery();
            }
        }

        public void AddItem(ClipboardItemModel item)
        {
            using (var connection = new SQLiteConnection(_connectionString))
            {
                connection.Open();
                var command = new SQLiteCommand(
                    "INSERT INTO ClipboardItems (Content, Timestamp, IsStarred) VALUES (@Content, @Timestamp, @IsStarred)",
                    connection);
                command.Parameters.AddWithValue("@Content", item.Content);
                command.Parameters.AddWithValue("@Timestamp", item.Timestamp);
                command.Parameters.AddWithValue("@IsStarred", item.IsStarred);
                command.ExecuteNonQuery();
            }
        }

        public List<ClipboardItemModel> GetItems()
        {
            var items = new List<ClipboardItemModel>();
            using (var connection = new SQLiteConnection(_connectionString))
            {
                connection.Open();
                var command = new SQLiteCommand("SELECT * FROM ClipboardItems ORDER BY IsStarred DESC, Timestamp DESC", connection);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        items.Add(new ClipboardItemModel
                        {
                            Id = reader.GetInt32(0),
                            Content = reader.GetString(1),
                            Timestamp = reader.GetDateTime(2),
                            IsStarred = reader.GetBoolean(3)
                        });
                    }
                }
            }
            return items;
        }
    }
}
