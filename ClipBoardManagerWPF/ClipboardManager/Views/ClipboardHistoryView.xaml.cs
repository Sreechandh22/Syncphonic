using System.Windows;

namespace ClipboardManager.Views
{
    public partial class ClipboardHistoryView : Window
    {
        public ClipboardHistoryView()
        {
            InitializeComponent();
            DataContext = new ViewModels.ClipboardHistoryViewModel();
        }
    }
}
