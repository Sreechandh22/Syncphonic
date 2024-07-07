using System.Collections.Generic;
using System.Threading.Tasks;
using ClipboardManager.Database;

namespace ClipboardManager
{
    public class ClipboardService
    {
        private readonly ClipboardDatabase _clipboardDatabase;

        public ClipboardService(string connectionString)
        {
            _clipboardDatabase = new ClipboardDatabase(connectionString);
        }

        public async Task AddClipboardItemAsync(string content)
        {
            await _clipboardDatabase.AddClipboardItemAsync(content);
        }

        public async Task<List<ClipboardItemModel>> GetClipboardItemsAsync()
        {
            return await _clipboardDatabase.GetClipboardItemsAsync();
        }
    }
}
