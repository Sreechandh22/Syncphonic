using System.Windows;

namespace ClipboardManager
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void OpenClipboardHistory_Click(object sender, RoutedEventArgs e)
        {
            var clipboardHistoryView = new Views.ClipboardHistoryView();
            clipboardHistoryView.Show();
        }
    }
}
