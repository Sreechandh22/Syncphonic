using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
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
                Debug.WriteLine("Database initialized.");
            }
        }

        public async Task AddClipboardItemAsync(string content)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                await connection.OpenAsync();
                var command = new SqliteCommand("INSERT INTO ClipboardItems (Content, Timestamp, Pinned) VALUES (@content, @timestamp, @pinned)", connection);
                command.Parameters.AddWithValue("@content", content);
                command.Parameters.AddWithValue("@timestamp", DateTime.Now);
                command.Parameters.AddWithValue("@pinned", false);
                await command.ExecuteNonQueryAsync();
                Debug.WriteLine($"Inserted item: {content}");
            }
        }

        public async Task<List<ClipboardItemModel>> GetClipboardItemsAsync()
        {
            var items = new List<ClipboardItemModel>();
            using (var connection = new SqliteConnection(_connectionString))
            {
                await connection.OpenAsync();
                var command = new SqliteCommand("SELECT * FROM ClipboardItems ORDER BY Timestamp DESC", connection);
                using (var reader = await command.ExecuteReaderAsync())
                {
                    while (await reader.ReadAsync())
                    {
                        items.Add(new ClipboardItemModel
                        {
                            Id = reader.GetInt32(0),
                            Content = reader.GetString(1),
                            Timestamp = reader.GetDateTime(2),
                            Pinned = reader.GetBoolean(3)
                        });
                        Debug.WriteLine($"Retrieved item: {reader.GetString(1)}");
                    }
                }
            }
            return items;
        }

        public async Task UpdateClipboardItemAsync(ClipboardItemModel item)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                await connection.OpenAsync();
                var command = new SqliteCommand("UPDATE ClipboardItems SET Pinned = @pinned WHERE Id = @id", connection);
                command.Parameters.AddWithValue("@pinned", item.Pinned);
                command.Parameters.AddWithValue("@id", item.Id);
                await command.ExecuteNonQueryAsync();
                Debug.WriteLine($"Updated item: {item.Content}");
            }
        }
    }
}
