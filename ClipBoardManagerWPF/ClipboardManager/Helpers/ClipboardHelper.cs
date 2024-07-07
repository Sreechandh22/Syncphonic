using System.Windows;

namespace ClipboardManager.Helpers
{
    public static class ClipboardHelper
    {
        public static string GetClipboardText()
        {
            if (Clipboard.ContainsText())
            {
                return Clipboard.GetText();
            }
            return string.Empty;
        }

        public static void SetClipboardText(string text)
        {
            Clipboard.SetText(text);
        }
    }
}
