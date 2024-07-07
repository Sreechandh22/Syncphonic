using System;

namespace ClipboardManager
{
    public class ClipboardItem
    {
        public int Id { get; set; }
        public string Content { get; set; }
        public bool Pinned { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
