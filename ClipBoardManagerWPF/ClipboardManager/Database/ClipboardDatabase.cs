using System;
using System.Collections.Generic;
using Microsoft.Data.Sqlite;

namespace ClipboardManager.Database
{
    public class ClipboardDatabase
    {
        private readonly string _connectionString;

        public ClipboardDatabase(string connectionString)
        {
            _connectionString = connectionString;
            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = new SqliteCommand("CREATE TABLE IF NOT EXISTS ClipboardItems (Id INTEGER PRIMARY KEY, Content TEXT, Timestamp DATETIME, Pinned BOOLEAN)", connection);
                command.ExecuteNonQuery();
            }
        }

        public void AddClipboardItem(string content)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = new SqliteCommand("INSERT INTO ClipboardItems (Content, Timestamp, Pinned) VALUES (@content, @timestamp, @pinned)", connection);
                command.Parameters.AddWithValue("@content", content);
                command.Parameters.AddWithValue("@timestamp", DateTime.Now);
                command.Parameters.AddWithValue("@pinned", false);
                command.ExecuteNonQuery();
            }
        }

        public List<ClipboardItemModel> GetClipboardItems()
        {
            var items = new List<ClipboardItemModel>();
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = new SqliteCommand("SELECT * FROM ClipboardItems ORDER BY Timestamp DESC", connection);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        items.Add(new ClipboardItemModel
                        {
                            Id = reader.GetInt32(0),
                            Content = reader.GetString(1),
                            Timestamp = reader.GetDateTime(2),
                            Pinned = reader.GetBoolean(3)
                        });
                    }
                }
            }
            return items;
        }

        public void UpdateClipboardItem(ClipboardItemModel item)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = new SqliteCommand("UPDATE ClipboardItems SET Pinned = @pinned WHERE Id = @id", connection);
                command.Parameters.AddWithValue("@pinned", item.Pinned);
                command.Parameters.AddWithValue("@id", item.Id);
                command.ExecuteNonQuery();
            }
        }
    }
}
