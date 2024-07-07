using System;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;

namespace ClipboardManager.Helpers
{
    public static class ClipboardNotification
    {
        public static event EventHandler ClipboardUpdate;

        private static HwndSource _source;

        public static void Start()
        {
            var window = new Window();
            window.SourceInitialized += delegate
            {
                _source = PresentationSource.FromVisual(window) as HwndSource;
                _source.AddHook(WndProc);
                NativeMethods.AddClipboardFormatListener(_source.Handle);
            };
            window.Show();
            window.Hide();
        }

        private static IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
        {
            if (msg == NativeMethods.WM_CLIPBOARDUPDATE)
            {
                ClipboardUpdate?.Invoke(null, EventArgs.Empty);
            }
            return IntPtr.Zero;
        }
    }

    internal static class NativeMethods
    {
        public const int WM_CLIPBOARDUPDATE = 0x031D;
        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool AddClipboardFormatListener(IntPtr hwnd);
        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool RemoveClipboardFormatListener(IntPtr hwnd);
    }
}
