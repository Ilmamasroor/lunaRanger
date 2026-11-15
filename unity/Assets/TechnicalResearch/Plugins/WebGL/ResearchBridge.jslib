mergeInto(LibraryManager.library, {
  PublishResearchState: function (pointer) {
    window.dispatchEvent(new CustomEvent("unity-research-state", { detail: JSON.parse(UTF8ToString(pointer)) }));
  }
});
