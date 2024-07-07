using System.ComponentModel;
using ClipboardManager.Database;

namespace ClipboardManager.ViewModels
{
    public class ClipboardItemViewModel : INotifyPropertyChanged
    {
        private ClipboardItemModel _clipboardItem;

        public ClipboardItemViewModel(ClipboardItemModel clipboardItem)
        {
            _clipboardItem = clipboardItem;
        }

        public int Id => _clipboardItem.Id;
        public string Content => _clipboardItem.Content;
        public bool Pinned
        {
            get => _clipboardItem.Pinned;
            set
            {
                if (_clipboardItem.Pinned != value)
                {
                    _clipboardItem.Pinned = value;
                    OnPropertyChanged(nameof(Pinned));
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public ClipboardItemModel ToModel()
        {
            return _clipboardItem;
        }
    }
}
