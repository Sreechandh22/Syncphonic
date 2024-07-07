using System.Collections.ObjectModel;
using ClipboardManager.Database;
using ClipboardManager.Helpers;

namespace ClipboardManager.ViewModels
{
    public class ClipboardHistoryViewModel
    {
        private readonly ClipboardDatabase _clipboardDatabase;
        public ObservableCollection<ClipboardItemViewModel> ClipboardItems { get; set; }
        public RelayCommand PinCommand { get; set; }

        public ClipboardHistoryViewModel()
        {
            _clipboardDatabase = new ClipboardDatabase("ClipboardDatabase.db");
            ClipboardItems = new ObservableCollection<ClipboardItemViewModel>();

            LoadClipboardHistory();

            PinCommand = new RelayCommand(OnPinItem);
        }

        private void LoadClipboardHistory()
        {
            var items = _clipboardDatabase.GetClipboardItems();
            foreach (var item in items)
            {
                ClipboardItems.Add(new ClipboardItemViewModel(item));
            }
        }

        private void OnPinItem(object parameter)
        {
            if (parameter is ClipboardItemViewModel item)
            {
                item.Pinned = !item.Pinned;
                _clipboardDatabase.UpdateClipboardItem(item.ToModel());
            }
        }
    }
}
