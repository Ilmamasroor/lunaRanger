mergeInto(LibraryManager.library, {
  PublishAirlockEvent: function (type) {
    window.dispatchEvent(new CustomEvent('unity-airlock', { detail: UTF8ToString(type) }));
  }
});
