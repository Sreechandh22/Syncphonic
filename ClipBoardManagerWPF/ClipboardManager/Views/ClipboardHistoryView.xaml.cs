using System.Windows.Controls;

namespace ClipboardManager.Views
{
    public partial class ClipboardHistoryView : UserControl
    {
        public ClipboardHistoryView()
        {
            InitializeComponent();
            DataContext = new ClipboardHistoryViewModel();
        }
    }
}
