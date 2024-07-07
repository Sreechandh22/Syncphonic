using System;
using System.Collections.Generic;
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

        public void AddClipboardItem(string content)
        {
            _clipboardDatabase.AddClipboardItem(content);
        }

        public List<ClipboardItemModel> GetClipboardItems()
        {
            return _clipboardDatabase.GetClipboardItems();
        }
    }
}
