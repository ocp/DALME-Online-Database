window.CustomUtils.userSelectState = {
  store: {
    baseApiUrl: "/api/public/user/",
    placeholder: "",
    handleFormFields: false,
    avatarUrl: "",
    photoChooser: null,
    selectEl: null,
    nameField:null,
    iconPlaceholder: '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>',
    getAvatarHTML: (url) => `<div class="avatar-bg" style="background: center/cover url(${url});"></div>`,
    getFormattedItem: (item) => {
      const store = window.CustomUtils.userSelectState.store;
      const avatar = item.avatar ? store.getAvatarHTML(item.avatar) : store.iconPlaceholder;
      return `<div class="user-option">${avatar}<div class="user-label"><span>${item.name}</span> <span class="user-username">${item.username}</span></div></div>`;
    },
    getIdList: (val) => {
      let result = JSON.parse(val.replaceAll(`'`, `"`));
      if (typeof result == "object") {
        result = result.filter((x) => x.trim() != "");
      }
      return result;
    },
    fetchResults: (url, callback) => {
      const results = [];
      const store = window.CustomUtils.userSelectState.store;
      fetch(url)
      .then(response => response.json())
      .then(data => {
          data.forEach((item) => {
            results.push({
              id: `${item.id}`,
              text: store.getFormattedItem(item),
              item: item,
            });
          });
          callback(results);
      });
    },
    togglePreview: () => {
      const store = window.CustomUtils.userSelectState.store;
      if (store.selectEl) {
        const value = store.selectEl.select2("data");
        store.photoChooser.querySelector(".chooser__image").src = value.item.avatar ? value.item.avatar : "#";
        if (!store.photoChooser.classList.contains("blank") || value.item.avatar) {
          store.photoChooser.classList.toggle("blank");
        }
      }
    },
    toggleForm: () => {
      const store = window.CustomUtils.userSelectState.store;
      const value = store.selectEl.select2("data");
      if (value) {
        store.nameField.value = value.item.name;
      } else {
        store.nameField.value = "";
      }
      store.togglePreview();
    },
  },
  queryAPI: (options) => {
    const store = window.CustomUtils.userSelectState.store;
    const url = options.term ? `${store.baseApiUrl}?name=${options.term}` : store.baseApiUrl;
    store.fetchResults(url, (results) => {
      options.callback({
        results: results,
        more: false,
        context: null,
      });
    });
  },
  initialFormatter: (el, callback) => {
    const store = window.CustomUtils.userSelectState.store;
    const id_list = store.getIdList(el.val());
    if (id_list.length) {
      el.val(id_list);
      store.fetchResults(`${store.baseApiUrl}?id__in=${id_list}`, (results) => {
        callback(el.data("multiple") !== "undefined" ? results : results[0]);
        store.togglePreview();
      });
    }
  },
  connectCallback: (selectEl) => {
    const store = window.CustomUtils.userSelectState.store;
    store.handleFormFields = typeof selectEl.data("handle-form-fields") !== "undefined";
    if (store.handleFormFields) {
      store.selectEl = selectEl;
      store.photoChooser = document.getElementById("id_photo-chooser");
      store.nameField = document.getElementById("id_name");
      selectEl.on("change", store.toggleForm);
    }
  },
  disconnectCallback: (selectEl) => {
    delete window.CustomUtils.userSelectState;
  },
}
