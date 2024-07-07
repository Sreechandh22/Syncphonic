using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Threading.Tasks;
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

            Debug.WriteLine("ClipboardHistoryViewModel initialized.");

            // Await the call to LoadClipboardHistoryAsync
            LoadClipboardHistoryAsync().ConfigureAwait(false);

            PinCommand = new RelayCommand(async (param) => await OnPinItem(param));
        }

        private async Task LoadClipboardHistoryAsync()
        {
            var items = await _clipboardDatabase.GetClipboardItemsAsync();
            foreach (var item in items)
            {
                Debug.WriteLine($"Loaded item: {item.Content}");
                ClipboardItems.Add(new ClipboardItemViewModel(item));
            }
        }

        private async Task OnPinItem(object parameter)
        {
            if (parameter is ClipboardItemViewModel item)
            {
                item.Pinned = !item.Pinned;
                await _clipboardDatabase.UpdateClipboardItemAsync(item.ToModel());
                Debug.WriteLine($"Item pinned: {item.Content}");
            }
        }
    }
}
