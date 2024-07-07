using System;

namespace ClipboardManager.Database
{
    public class ClipboardItemModel
    {
        public int Id { get; set; }
        public string Content { get; set; }
        public DateTime Timestamp { get; set; }
        public bool Pinned { get; set; }
    }
}
