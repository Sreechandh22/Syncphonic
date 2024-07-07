using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows.Input;
using ClipboardManager.Helpers;

namespace ClipboardManager.ViewModels
{
    public class ClipboardHistoryViewModel : INotifyPropertyChanged
    {
        private readonly ClipboardService _clipboardService;
        public ObservableCollection<ClipboardItem> ClipboardItems { get; set; } = new ObservableCollection<ClipboardItem>();

        public ICommand StarItemCommand { get; }
        public ICommand LoadMoreCommand { get; }

        public ClipboardHistoryViewModel()
        {
            _clipboardService = new ClipboardService();
            LoadClipboardHistory();

            StarItemCommand = new RelayCommand(StarItem);
            LoadMoreCommand = new RelayCommand(LoadMore);
        }

        private void LoadClipboardHistory()
        {
            ClipboardItems.Clear();
            var items = _clipboardService.GetClipboardHistory();
            foreach (var item in items)
            {
                ClipboardItems.Add(item);
            }
        }

        private void StarItem(object parameter)
        {
            if (parameter is ClipboardItem item)
            {
                _clipboardService.StarItem(item.Id);
                LoadClipboardHistory();
            }
        }

        private void LoadMore(object parameter)
        {
            // Implement logic to load more items if required
        }

        public event PropertyChangedEventHandler PropertyChanged;
    }
}
