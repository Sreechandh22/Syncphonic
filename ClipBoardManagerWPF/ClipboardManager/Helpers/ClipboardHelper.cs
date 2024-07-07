using System.Windows;

namespace ClipboardManager.Helpers
{
    public static class ClipboardHelper
    {
        public static void SetText(string text)
        {
            Clipboard.SetText(text);
        }

        public static string GetText()
        {
            return Clipboard.ContainsText() ? Clipboard.GetText() : string.Empty;
        }

        // Additional helper methods
    }
}
