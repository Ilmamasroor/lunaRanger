mergeInto(LibraryManager.library, {
  PublishCampaignState: function (json) {
    window.dispatchEvent(new CustomEvent("lunarangers-campaign", {
      detail: JSON.parse(UTF8ToString(json))
    }));
  },
  RequestCampaignSpacewalk: function (token, day) {
    window.dispatchEvent(new CustomEvent("lunarangers-spacewalk", {
      detail: { token: token, day: day }
    }));
  }
});
