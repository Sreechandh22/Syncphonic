using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Interop;

namespace ClipboardManager.Helpers
{
    public class ClipboardNotification
    {
        public event EventHandler ClipboardChanged;

        public ClipboardNotification()
        {
            var window = new Window();
            var hwndSource = HwndSource.FromHwnd(new WindowInteropHelper(window).Handle);
            hwndSource.AddHook(WndProc);
            Debug.WriteLine("ClipboardNotification initialized.");
        }

        private IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
        {
            const int WM_CLIPBOARDUPDATE = 0x031D;

            if (msg == WM_CLIPBOARDUPDATE)
            {
                Debug.WriteLine("Clipboard content changed.");
                OnClipboardChanged();
            }

            return IntPtr.Zero;
        }

        protected virtual void OnClipboardChanged()
        {
            ClipboardChanged?.Invoke(this, EventArgs.Empty);
        }
    }
}
